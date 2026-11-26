"""API do projeto. No vídeo 1 ela só tem o /health; as rotas de RAG entram no vídeo 7."""
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app import config
from app.generation.answer import generate_answer
from app.ingestion.indexer import index_documents
from app.retrieval.search import search
from app.retrieval.vectorstore import get_vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    for attempt in range(10):
        try:
            get_vector_store()
            break
        except RuntimeError:
            break
        except Exception:
            if attempt == 9:
                raise
            time.sleep(2)

    yield

app = FastAPI(title="Assistente de documentos (RAG)", lifespan=lifespan)

class IndexRequest(BaseModel):
    chunk_size: int | None = Field(default=None, gt=0)
    chunk_overlap: int | None = Field(default=None, ge=0)
    reset: bool = True

class AskRequest(BaseModel):
    question: str = Field(min_length=3)
    k: int = Field(default=config.TOP_K, ge=1, le=10)
    
class Source(BaseModel):
    source: str
    chunk_id: str
    score: float
    content: str

class AskResponse(BaseModel):
    answer: str
    sources: list[Source]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/index")
def index(body: IndexRequest | None = None):
    body = body or IndexRequest()

    try:
        return index_documents(
            chunk_size=body.chunk_size,
            chunk_overlap=body.chunk_overlap,
            reset=body.reset,
        )
    except (ValueError, FileNotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=AskResponse)
def ask(body: AskRequest):

    try:
        chunks = search(body.question, body.k)
        answer = generate_answer(body.question, chunks)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return AskResponse(
        answer=answer,
        sources=[
            Source(
                source=h.source,
                chunk_id=h.chunk_id,
                score=h.score,
                content=h.content
            )
            for h in chunks
        ]
    )

"""API do projeto. No vídeo 1 ela só tem o /health; as rotas de RAG entram no vídeo 7."""
from fastapi import FastAPI

app = FastAPI(title="Assistente de documentos (RAG)")


@app.get("/health")
def health():
    return {"status": "ok"}

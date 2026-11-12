"""Configuração central. Tudo vem de variáveis de ambiente (ou do arquivo .env)."""
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
JUDGE_MODEL = os.getenv("JUDGE_MODEL", CHAT_MODEL)  # modelo que avalia as respostas (DeepEval)

# O LangChain usa SQLAlchemy, por isso o prefixo "postgresql+psycopg".
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://rag:rag@localhost:5432/rag")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "nimbus_docs")

# Pasta com os documentos que serão indexados (.md, .txt e .pdf).
DOCS_DIR = os.getenv("DOCS_DIR", "data/docs")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
TOP_K = int(os.getenv("TOP_K", "4"))


def require_openai_key() -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY não definida. Copie .env.example para .env e preencha a chave."
        )
    return OPENAI_API_KEY

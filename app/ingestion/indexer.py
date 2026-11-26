from app import config
from app.ingestion.chunking import chunk_documents
from app.ingestion.loader import load_documents
from app.retrieval.vectorstore import get_vector_store


def index_documents(
    directory: str | None = None,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
    reset: bool = True,
) -> dict:
    directory = directory or config.DOCS_DIR
    chunk_size = chunk_size or config.CHUNK_SIZE
    chunk_overlap = config.CHUNK_OVERLAP if chunk_overlap is None else chunk_overlap
    
    documents = load_documents(directory)
    chunks = chunk_documents(documents, chunk_size, chunk_overlap)
    
    store = get_vector_store(reset=reset)
    store.add_documents(chunks, ids=[c.metadata["chunk_id"] for c in chunks])
    
    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
    }
    
if __name__ == "__main__":
    print(index_documents())


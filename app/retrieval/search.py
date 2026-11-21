from dataclasses import dataclass

from app import config
from app.retrieval.vectorstore import get_vector_store


@dataclass
class Hit:
    source: str
    chunk_index: int
    chunk_id: str
    content: str
    score: float
    
def search(
    query: str,
    k: int | None = None
) -> list[Hit]:
    k = k or config.TOP_K
    
    results = get_vector_store().similarity_search_with_score(query, k=k)
    
    return [
        Hit(
            source=doc.metadata["source"],
            chunk_index=doc.metadata["chunk_index"],
            chunk_id=doc.metadata["chunk_id"],
            content=doc.page_content,
            score=1 - distance,
        )
        for doc, distance in results
    ]
    
if __name__ == "__main__":
    import sys
    
    question = "Quantos dias de férias posso converter em dinheiro?"
    
    for hit in search(question):
        print(f"[{hit.score:.3f}] {hit.chunk_id}\n{hit.content}\n")
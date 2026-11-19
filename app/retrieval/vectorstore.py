import psycopg
from langchain_postgres import PGVector

from app import config
from app.retrieval import embeddings

def get_vector_store(reset: bool = False) -> PGVector:
    return PGVector(
        embeddings=embeddings.get_embeddings(),
        collection_name=config.COLLECTION_NAME,
        connection=config.DATABASE_URL,
        use_jsonb=True,
        pre_delete_collection=reset,
    )
    
def list_indexed_chunks() -> list[dict]:
    url = config.DATABASE_URL.replace("postgresql+psycopg", "postgresql", 1)
    
    with psycopg.connect(url) as conn:
        rows = conn.execute(
            """
            SELECT e.cmetadata->>'chunk_id', e.cmetadata->>'source', e.document
            FROM langchain_pg_embedding e
            JOIN langchain_pg_collection c ON c.uuid = e.collection_id
            WHERE c.name = %s
            ORDER BY e.cmetadata->>'source', (e.cmetadata->>'chunk_index')::int
            """,
            (config.COLLECTION_NAME,),
        ).fetchall()
    return [{"chunk_id": r[0], "source": r[1], "content": r[2]} for r in rows]
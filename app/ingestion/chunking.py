from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 100
) -> list[Document]:
    if chunk_size <= 0:
        raise ValueError("chunk_size deve ser >= 0 e menor que chunk_size")
    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError("chunk_overlap deve ser >= 0 e menor que chunk_size")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(documents)
    
    counters: dict[str, int] = {} #ex.: "home_office:2"
    
    for chunk in chunks:
        source = chunk.metadata["source"]
        index = counters.get(source, 0)
        counters[source] = index + 1
        chunk.metadata["chunk_index"] = index
        chunk.metadata["chunk_id"] = f"{source}:{index}" #ex.: "home_office:2"
    return chunks

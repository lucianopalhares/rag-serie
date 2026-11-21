from pathlib import Path 

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

SUPPORTED = {".md", ".txt", ".pdf"}

def load_file(path: Path) -> list[Document]:
    if path.suffix.lower() == ".pdf":
        return PyPDFLoader(str(path)).load()
    return TextLoader(str(path), encoding="utf-8").load()

def load_documents(directory: str | Path) -> list[Document]:
    directory = Path(directory)
    if not directory.is_dir():
        raise FileNotFoundError(f"Pasta de documentos não encontrada: {directory}")
    
    documents = []
    
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue
        for doc in load_file(path):
            doc.page_content = doc.page_content.strip()
            
            if doc.page_content:
                doc.metadata["source"] = path.stem
                documents.append(doc)
    return documents
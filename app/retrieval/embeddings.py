from langchain_openai import OpenAIEmbeddings

from app import config


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        api_key=config.require_openai_key()
    )
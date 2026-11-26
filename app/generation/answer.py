from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app import config
from app.retrieval.search import Hit

SYSTEM_PROMPT = """
Você é um assistente que responde perguntas sobre documentos internos de uma empresa.

Regras:
- Responda SOMENTE com base nos trechos fornecidos em CONTEXTO.
- Cite as fontes no formato [1], [2], conforme a numeração dos trechos.
- Se o contexto não contém a resposta, diga exatamente: "Não encontrei essa informação nos documentos."
- Seja direto e responda em português.
"""

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "CONTEXTO:\n{context}\n\nPERGUNTA: {question}"),
    ]
)

def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=config.CHAT_MODEL,
        temperature=0,
        api_key=config.require_openai_key()
    )
    
def build_context(hits: list[Hit]) -> str:
    return "\n\n".join(f"[{i}] (fonte: {h.source})\n{h.content}" for i, h in
enumerate(hits, start=1))

def generate_answer(question: str, hits: list[Hit]) -> str:
    chain = PROMPT | get_llm() | StrOutputParser()
    
    return chain.invoke(
        {
            "context": build_context(hits),
            "question": question
        }
    ).strip()
    
if __name__ == "__main__":
    import sys

    from app.retrieval.search import search
    
    question = " Quantos dias de férias posso converter em dinheiro?"
    
    hits = search(question)
    
    print(generate_answer(question, hits))
    print("\nFontes:", ", ".join(h.chunk_id for h in hits))


# Assistente de documentos com RAG (Python + FastAPI + LangChain + pgvector)

Projeto da série de vídeos. Vamos construir, passo a passo, um assistente que responde perguntas sobre documentos internos de uma empresa fictícia (a "Nimbus Tecnologia"), citando as fontes.

**Stack:** Python 3.12, FastAPI, LangChain, OpenAI, Postgres com pgvector. Avaliação: `ranx` e DeepEval.

## Como acompanhar a série

Cada vídeo tem uma tag no Git com o código **no final** daquele vídeo:

```bash
git clone https://github.com/lucianopalhares/rag-serie.git
cd rag-serie
```

## Como rodar

Pré-requisitos: Docker e uma chave da OpenAI (a chave só é usada depois em videos futuros).

```bash
cp .env.example .env        # edite e coloque sua OPENAI_API_KEY
docker compose up --build   # sobe o Postgres (pgvector) e a API
curl localhost:8562/health  # {"status":"ok"}
```

## Roteiro da série

| Vídeo | Tema |
|---|---|
| 1 | Setup (este ponto de partida) |
| 2 | Ingestão de documentos |
| 3 | Chunking |
| 4 | Embeddings e banco vetorial |
| 5 | Busca semântica |
| 6 | Geração da resposta |
| 7 | Expondo na API |
| 8 | Evaluation do retriever (ranx) |
| 9 | Evaluation da resposta (DeepEval) |

Os documentos em `data/docs/` são fictícios e foram escritos só para este exemplo.

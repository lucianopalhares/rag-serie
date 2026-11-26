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

## Debug da API no Docker Compose

O serviço `api` já inicia o `debugpy` na porta `5678` e mantém o código local
montado em `/code/app` dentro do container. A API não fica bloqueada enquanto
o debugger não estiver conectado.

1. Suba os serviços:

   ```bash
   docker compose up --build
   ```

2. No VS Code, abra **Run and Debug** e selecione `Python: Attach na API (Docker Compose)`.

3. Coloque um breakpoint em qualquer arquivo Python dentro de `app/` e faça
   uma requisição, por exemplo:

   ```bash
   curl http://localhost:8562/health
   ```

O debugger pode ser conectado antes ou depois da requisição. Para encerrar,
use `Ctrl+C` no terminal do Compose.

## Roteiro da série

### Siga as tags abaixo para acompanhar cada video

| Tag | Tema |
|---|---|
| video-0 | Setup (este ponto de partida) |
| video-1 | Ingestão de documentos |
| video-2 | Chunking |
| video-3 | Embeddings e banco vetorial |
| video-4 | Busca semântica |
| video-5 | Geração da resposta |
| video-6 | Expondo na API |
| video-7 | Evaluation do retriever (ranx) |
| video-8 | Evaluation da resposta (DeepEval) |

- Exemplo assistir o video 1 com a aplicação base:

   ```bash
   git checkout video-0
   ```
- Exemplo assistir o video 2 com a aplicação já implementado o video-1:

   ```bash
   git checkout video-1
   ```

Os documentos na pasta `data/docs/` são fictícios e foram escritos só para este exemplo.

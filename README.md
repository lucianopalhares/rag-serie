# RAG do zero: construa e meça (Python + FastAPI + LangChain + pgvector)

Este repositório é o código do **curso gratuito "RAG do zero + Avaliação de Qualidade"**, ministrado no YouTube no canal **Alquimia da Web**.

> ▶ **Assista ao curso:** https://www.youtube.com/watch?v=b7ThWeBPWDc&list=PLbi5DUXOKEuc

**Por Luciano Palhares**, engenheiro de IA: RAG, avaliação de retriever e de resposta, LLM como juiz e integração de IA em APIs.

No curso, construímos passo a passo um assistente que responde perguntas sobre documentos internos de uma empresa fictícia, a **Nimbus Tecnologia**, citando as fontes. Depois de construir, **medimos a qualidade**: primeiro a busca, depois a resposta.

**Stack:** Python 3.12, FastAPI, LangChain, OpenAI, Postgres com pgvector, Docker. **Avaliação:** `ranx` (busca) e DeepEval (resposta).

## O que você aprende

- Ler PDF e Markdown e preparar os documentos para o RAG.
- Dividir o texto em chunks, com tamanho e sobreposição.
- Gerar embeddings e guardar no Postgres com pgvector.
- Buscar trechos pelo sentido da pergunta (busca semântica).
- Gerar respostas com LLM citando as fontes, usando uma chain do LangChain.
- Expor tudo numa API com FastAPI (`/index`, `/ask`, `/health`).
- **Avaliar o retriever** com hit rate@k e MRR.
- **Avaliar a resposta** com DeepEval, usando um LLM como juiz.

## Como acompanhar o curso

Cada vídeo tem uma **tag** no Git, com o código **como ele está no final daquele vídeo**. Assim você pode começar de qualquer ponto e comparar com o que aparece na tela.

```bash
git clone https://github.com/lucianopalhares/rag-serie.git
cd rag-serie
```

| Tag | Vídeo |
|---|---|
| `video-0` | Setup (ponto de partida) |
| `video-1` | Ingestão de documentos |
| `video-2` | Chunking |
| `video-3` | Embeddings e banco vetorial |
| `video-4` | Busca semântica |
| `video-5` | Geração da resposta |
| `video-6` | Expondo na API |
| `video-7` | Avaliação do retriever (ranx) |
| `video-8` | Avaliação da resposta (DeepEval) |

Exemplos:

```bash
# Para assistir ao vídeo 1 com a aplicação base:
git checkout video-0

# Para assistir ao vídeo 2 com o vídeo 1 já implementado:
git checkout video-1

# Para ver o projeto completo, no final do curso:
git checkout video-8
```

## Como rodar

Pré-requisitos: **Docker** e uma **chave da API da OpenAI**. A chave passa a ser usada a partir do vídeo 3 (embeddings), e as chamadas ao modelo têm custo na sua conta.

```bash
cp .env.example .env        # edite e coloque sua OPENAI_API_KEY
docker compose up --build   # sobe o Postgres (pgvector) e a API
curl localhost:8562/health  # {"status":"ok"}
```

## Usando a API (a partir do vídeo 6)

```bash
# 1. Indexar os documentos (lê, divide e guarda no banco)
curl -X POST localhost:8562/index

# 2. Fazer uma pergunta
curl -X POST localhost:8562/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Quantos dias de férias posso converter em dinheiro?"}'
```

A documentação interativa fica em `http://localhost:8562/docs`.

## Rodando as avaliações (vídeos 7 e 8)

As avaliações usam bibliotecas extras (`requirements-eval.txt`). Rode dentro do container da API:

```bash
# Avaliar a busca (hit rate@k e MRR). Use --k para mudar o número de trechos.
docker compose exec api python -m app.evaluation.retriever_eval --k 4

# Avaliar as respostas com um LLM como juiz. Cada pergunta custa chamadas à OpenAI.
docker compose exec api python -m app.evaluation.answer_eval --limit 5
```

Dica: use no `.env` um `JUDGE_MODEL` mais forte que o `CHAT_MODEL`. Um juiz igual ao gerador tende a ser indulgente.

## Debug da API no Docker Compose

O serviço `api` já inicia o `debugpy` na porta `5678` e mantém o código local montado em `/code/app` dentro do container. A API não fica bloqueada enquanto o debugger não estiver conectado.

1. Suba os serviços:

   ```bash
   docker compose up --build
   ```

2. No VS Code, abra **Run and Debug** e selecione `Python: Attach na API (Docker Compose)`.

3. Coloque um breakpoint em qualquer arquivo Python dentro de `app/` e faça uma requisição, por exemplo:

   ```bash
   curl http://localhost:8562/health
   ```

O debugger pode ser conectado antes ou depois da requisição. Para encerrar, use `Ctrl+C` no terminal do Compose.

## Sobre o autor

**Luciano Palhares** é engenheiro de IA e criador do canal **Alquimia da Web**. Trabalha com:

- **RAG:** da ingestão de documentos à resposta com fontes.
- **Avaliação de qualidade:** medir a busca (hit rate, MRR) e a resposta (LLM como juiz), em vez de confiar no "parece funcionar".
- **Integração de IA em APIs e sistemas**, com Python, FastAPI e bancos vetoriais.

Este projeto reúne esse método: construir cada etapa do RAG e medir o resultado com números.

- 🎥 YouTube: https://www.youtube.com/@programadormelhor
- 🌐 Site e Portfolio: https://lucianopalhares.com.br
- 💼 LinkedIn: [_ver linkedin_](https://www.linkedin.com/in/l-palhares-rosa/)

## Sobre os documentos

Os arquivos em `data/docs/` são **fictícios** e foram escritos só para este exemplo. A empresa Nimbus Tecnologia não existe.

## Curso no YouTube

Gostou do projeto? Assista à série completa, com a explicação de cada passo:

▶ https://www.youtube.com/watch?v=b7ThWeBPWDc&list=PLbi5DUXOKEuc

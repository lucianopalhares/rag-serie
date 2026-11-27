import argparse

from app.evaluation.dataset import load_dataset
from app.evaluation.metrics import evaluate_retriever
from app.ingestion.indexer import index_documents
from app.retrieval.search import search
from app.retrieval.vectorstore import list_indexed_chunks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=4)
    args = parser.parse_args()

    dataset = load_dataset()
    
    result = evaluate_retriever(dataset, search, args.k)
    
    print(
        f"{result['total']} perguntas | hit_rate@{args.k} = {result['hit_rate']:.0%} | MRR = {result['mrr']:.2f}"
    )
    
    questions = {
        item["id"]: item["question"]
        for item in dataset.items
    }
    
    if result["failures"]:
        print(
            f"\n0 chunk certo não apareceu no top-{args.k} ({len(result['failures'])}):"
        )
        for f in result["failures"]:
            print(
                f"- {questions[f['query_id']]}\n esperado {f['expected']} recuperou: {f['retrieved']}"
            )

if __name__ == "__main__":
    main()


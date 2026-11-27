import warnings
from collections.abc import Callable

from app.evaluation.dataset import Dataset

warnings.filterwarnings("ignore", module=r"ranx.*")

from ranx import Qrels, Run, evaluate


def evaluate_retriever(
    dataset: Dataset,
    search_fn: Callable[[str, int], list],
    k: int = 5
) -> dict:
    qrels = dataset.qrels
    run_dict = {
        item["id"]: {
            hit.chunk_id: hit.score
            for hit in search_fn(item["question"], k)
        }
        for item in dataset.items
    }
    
    scores = evaluate(
        Qrels(qrels),
        Run(run_dict),
        [f"hit_rate@{k}", "mrr"]
    )
    
    failures = [
        {
            "query_id": qid,
            "expected": list(qrels[qid]),
            "retrieved": list(run_dict[qid])
        }
        for qid in run_dict
        if not set(run_dict[qid]) & set(qrels[qid])
    ]

    return {
        "total": len(run_dict),
        "k": k,
        "hit_rate": float(scores[f"hit_rate@{k}"]),
        "mrr": float(scores["mrr"]),
        "failures": failures,
    }


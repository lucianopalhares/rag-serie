import os

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "YES")

import argparse

from deepeval import evaluate
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from app import config
from app.evaluation.dataset import Dataset, load_dataset
from app.generation.answer import generate_answer
from app.retrieval.search import search


def build_test_cases(
    dataset: Dataset,
    limit: int,
    k: int = 4
) -> list[LLMTestCase]:
    cases = []

    for item in dataset.items[:limit]:
        hits = search(item["question"], k)

        cases.append(
            LLMTestCase(
                input=item["question"],
                actual_output=generate_answer(item["question"], hits),
                expected_output=item["answer"],
                retrieval_context=[h.content for h in hits]
            )
        )
    return cases

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    
    corretness = GEval(
        name="Correção",
        criteria="A resposta real deve concordar com a resposta esperada, sem contradizê-la nem inventar fatos",
        evaluation_params=[
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT
        ],
        threshold=0.7,
        model=config.JUDGE_MODEL
    )
    
    evaluate(
        test_cases=build_test_cases(
            load_dataset(), args.limit
        ),
        metrics=[corretness]
    )
    
if __name__ == "__main__":
    main()
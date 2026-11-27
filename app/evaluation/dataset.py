import json
from dataclasses import dataclass
from pathlib import Path

DATASET_PATH = Path(__file__).parent / "dataset.json"

@dataclass
class Dataset:
    items: list[dict]
    
    @property
    def qrels(self) -> dict[str, dict[str, int]]:
        return {
            item["id"]: {
                item["chunk_id"]: item["relevance"]
            }
            for item in self.items
        }
        
def load_dataset(path: Path = DATASET_PATH) -> Dataset:
    return Dataset(items=json.loads(path.read_text(encoding="utf-8")))


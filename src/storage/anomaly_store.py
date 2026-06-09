from pathlib import Path
from src.storage.base_store import BaseStore


class AnomalyStore(BaseStore):
    FILE_PATH = Path("data/anomalies.json")
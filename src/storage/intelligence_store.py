from pathlib import Path
from src.storage.base_store import BaseStore


class IntelligenceStore(BaseStore):
    FILE_PATH = Path("data/intelligence_reports.json")
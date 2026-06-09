from pathlib import Path
from src.storage.base_store import BaseStore


class AIReportStore(BaseStore):
    FILE_PATH = Path("data/ai_reports.json")
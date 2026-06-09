from src.storage.base_store import BaseStore
from datetime import datetime

class IntelligenceStore(BaseStore):

    def __init__(self):
        super().__init__("data/intelligence_reports.json")

    def save(self, report):
        data = self._read()

        if hasattr(report, "model_dump"):
            report = report.model_dump()

        report["stored_at"] = datetime.now().isoformat()

        data.append(report)
        self._write(data)

    def get_all(self):
        return self._read()
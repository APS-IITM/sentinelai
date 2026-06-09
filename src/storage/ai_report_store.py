from src.storage.base_store import BaseStore
from datetime import datetime

class AIReportStore(BaseStore):

    def __init__(self):
        super().__init__("data/ai_reports.json")

    def save(self, report: dict):
        data = self._read()

        report["stored_at"] = datetime.now().isoformat()
        data.append(report)

        self._write(data)

    def get_all(self):
        return self._read()

    def latest(self):
        data = self._read()
        return data[-1] if data else None
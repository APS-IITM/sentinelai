from src.storage.base_store import BaseStore
from datetime import datetime

class AnomalyStore(BaseStore):

    def __init__(self):
        super().__init__("data/anomalies.json")

    def save(self, event):
        data = self._read()

        if hasattr(event, "model_dump"):
            event = event.model_dump()

        event["stored_at"] = datetime.now().isoformat()

        data.append(event)
        self._write(data)

    def get_all(self):
        return self._read()
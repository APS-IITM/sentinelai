import json
from pathlib import Path
from datetime import datetime

ANOMALY_FILE = Path("data/anomalies.json")

ANOMALY_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


class AnomalyStore:

    @staticmethod
    def save(event):

        existing = []

        if ANOMALY_FILE.exists():
            with open(
                ANOMALY_FILE,
                "r",
                encoding="utf-8"
            ) as f:
                existing = json.load(f)

        existing.append(event)

        with open(
            ANOMALY_FILE,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                existing,
                f,
                indent=4
            )

    @staticmethod
    def get_all():

        if not ANOMALY_FILE.exists():
            return []

        with open(
            ANOMALY_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)
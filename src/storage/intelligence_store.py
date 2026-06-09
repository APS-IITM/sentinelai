import json
from pathlib import Path


class IntelligenceStore:

    FILE = Path(
        "data/intelligence_reports.json"
    )

    FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    @classmethod
    def save(cls, report):

        records = []

        if cls.FILE.exists():

            try:

                with open(
                    cls.FILE,
                    "r",
                    encoding="utf-8"
                ) as f:

                    records = json.load(f)

            except Exception:
                records = []

        records.append(report)

        with open(
            cls.FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                records,
                f,
                indent=4,
                default=str
            )

    @classmethod
    def get_all(cls):

        if not cls.FILE.exists():
            return []

        with open(
            cls.FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)
import json
from pathlib import Path


class AIReportStore:

    REPORT_FILE = Path(
        "data/ai_reports.json"
    )

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    @classmethod
    def save(cls, report):

        existing = []

        if cls.REPORT_FILE.exists():

            try:

                with open(
                    cls.REPORT_FILE,
                    "r",
                    encoding="utf-8"
                ) as f:

                    existing = json.load(f)

            except Exception:
                existing = []

        existing.append(report)

        with open(
            cls.REPORT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                existing,
                f,
                indent=4,
                default=str
            )

    @classmethod
    def get_all(cls):

        if not cls.REPORT_FILE.exists():
            return []

        with open(
            cls.REPORT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    @classmethod
    def latest(cls):

        reports = cls.get_all()

        if not reports:
            return None

        return reports[-1]
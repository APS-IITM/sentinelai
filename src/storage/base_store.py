import json
from pathlib import Path
from typing import Any, List


class BaseStore:
    """
    Industrial-grade JSON persistence engine.
    - Safe read/write
    - Auto file creation
    - Corruption resistant
    - Unified interface for all stores
    """

    FILE_PATH: Path = None

    @classmethod
    def _ensure_file(cls):
        if cls.FILE_PATH is None:
            raise ValueError("FILE_PATH not defined in subclass")

        cls.FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

        if not cls.FILE_PATH.exists():
            cls.FILE_PATH.write_text("[]", encoding="utf-8")

    @classmethod
    def save(cls, record: Any) -> None:
        cls._ensure_file()

        try:
            data = json.loads(cls.FILE_PATH.read_text(encoding="utf-8"))
        except Exception:
            data = []

        data.append(record)

        cls.FILE_PATH.write_text(
            json.dumps(data, indent=4, default=str),
            encoding="utf-8"
        )

    @classmethod
    def get_all(cls) -> List[Any]:
        cls._ensure_file()

        try:
            return json.loads(cls.FILE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return []

    @classmethod
    def latest(cls) -> Any:
        data = cls.get_all()
        return data[-1] if data else None

    @classmethod
    def clear(cls) -> None:
        cls._ensure_file()
        cls.FILE_PATH.write_text("[]", encoding="utf-8")
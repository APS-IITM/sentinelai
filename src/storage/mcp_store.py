import json
from pathlib import Path
from datetime import datetime

class MCPStore:

    BASE_DIR = Path("data/mcp")
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def save(cls, tool_name: str, data: dict):

        file_path = cls.BASE_DIR / f"{tool_name}.json"

        records = []
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    records = json.load(f)
            except Exception:
                records = []

        data["stored_at"] = datetime.now().isoformat()
        records.append(data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=4, default=str)

    @classmethod
    def get(cls, tool_name: str):
        file_path = cls.BASE_DIR / f"{tool_name}.json"

        if not file_path.exists():
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
import json
from pathlib import Path


class MCPStore:
    """
    Stores MCP tool outputs in both:
    - memory cache
    - persistent JSON files
    """

    DATA_DIR = Path("data/mcp")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    _cache = {}

    @staticmethod
    def save(tool_name: str, data: dict):

        MCPStore._cache.setdefault(tool_name, [])
        MCPStore._cache[tool_name].append(data)

        file_path = MCPStore.DATA_DIR / f"{tool_name}.json"

        try:
            if file_path.exists():
                existing = json.loads(file_path.read_text())
            else:
                existing = []
        except Exception:
            existing = []

        existing.append(data)

        file_path.write_text(
            json.dumps(existing, indent=4, default=str),
            encoding="utf-8"
        )

    @staticmethod
    def get(tool_name: str):
        return MCPStore._cache.get(tool_name, [])

    @staticmethod
    def load_from_disk(tool_name: str):
        file_path = MCPStore.DATA_DIR / f"{tool_name}.json"

        if not file_path.exists():
            return []

        try:
            return json.loads(file_path.read_text())
        except Exception:
            return []

    @staticmethod
    def clear(tool_name: str):
        MCPStore._cache[tool_name] = []

        file_path = MCPStore.DATA_DIR / f"{tool_name}.json"
        if file_path.exists():
            file_path.write_text("[]", encoding="utf-8")
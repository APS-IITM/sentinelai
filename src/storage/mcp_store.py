import json
from pathlib import Path
from src.splunk.config import DATA_DIR, MCP_DATA_STORE

class MCPStore:

    @staticmethod
    def save(tool_name, data):

        MCP_DATA_STORE.setdefault(tool_name, [])
        MCP_DATA_STORE[tool_name].append(data)

        file_path = DATA_DIR / f"{tool_name}.json"

        existing = []

        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                existing = json.load(f)

        existing.append(data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=4)

    @staticmethod
    def get(tool_name):
        return MCP_DATA_STORE.get(tool_name, [])

    @staticmethod
    def clear(tool_name):
        MCP_DATA_STORE[tool_name] = []
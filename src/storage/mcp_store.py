from threading import Lock

from src.storage.supabase_client import supabase
from src.storage.utils import safe_dict


class MCPStore:

    TABLE_NAME = "mcp_store"

    # 🔒 Internal class-level lock (no external file needed)
    _write_lock = Lock()

    @staticmethod
    def save(tool_name, data):
        """
        Thread-safe Supabase insert for MCP telemetry storage.
        Prevents socket race conditions (WinError 10035).
        """

        clean_payload = safe_dict(data)

        payload = {
            "tool_name": tool_name,
            "payload": clean_payload
        }

        # 🔒 SAFE SERIALIZED WRITE TO SUPABASE
        with MCPStore._write_lock:
            return (
                supabase
                .table(MCPStore.TABLE_NAME)
                .insert(payload)
                .execute()
            )

    @staticmethod
    def get(tool_name):
        response = (
            supabase
            .table(MCPStore.TABLE_NAME)
            .select("*")
            .eq("tool_name", tool_name)
            .execute()
        )

        return [
            row["payload"]
            for row in (response.data or [])
            if "payload" in row
        ]

    @staticmethod
    def clear(tool_name):
        with MCPStore._write_lock:
            return (
                supabase
                .table(MCPStore.TABLE_NAME)
                .delete()
                .eq("tool_name", tool_name)
                .execute()
            )
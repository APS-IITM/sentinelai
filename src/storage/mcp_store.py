from src.storage.supabase_client import supabase

from src.storage.utils import safe_dict 


class MCPStore:

    TABLE_NAME = "mcp_store"

    @staticmethod
    def save(
        tool_name,
        data
    ):
        # FIXED: Forces comprehensive JSON serialization on the incoming dataset
        clean_payload = safe_dict(data)

        payload = {
            "tool_name": tool_name,
            "payload": clean_payload
        }

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
            .eq(
                "tool_name",
                tool_name
            )
            .execute()
        )

        return [
            row["payload"]
            for row in response.data
            if "payload" in row
        ]

    @staticmethod
    def clear(tool_name):

        return (
            supabase
            .table(MCPStore.TABLE_NAME)
            .delete()
            .eq(
                "tool_name",
                tool_name
            )
            .execute()
        )
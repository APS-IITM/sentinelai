from src.storage.supabase_client import supabase


class MCPStore:

    TABLE_NAME = "mcp_store"

    @staticmethod
    def save(
        tool_name,
        data
    ):

        payload = {
            "tool_name": tool_name,
            "payload": data
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
        ]

    @staticmethod
    def clear(tool_name):

        (
            supabase
            .table(MCPStore.TABLE_NAME)
            .delete()
            .eq(
                "tool_name",
                tool_name
            )
            .execute()
        )
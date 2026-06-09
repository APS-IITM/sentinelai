from src.splunk.client import connect, run_search
from src.utils.formatter import normalize_response
from src.storage.mcp_store import MCPStore


class BaseTool:

    TOOL_NAME = "generic"

    def __init__(self):
        self.service = connect()

    def execute(self, query: str):

        raw = run_search(self.service, query)

        result = normalize_response(raw)

        # Automatically save result
        MCPStore.save(
            tool_name=self.TOOL_NAME,
            data={
                "query": query,
                "results": result
            }
        )

        return result
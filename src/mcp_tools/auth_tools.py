from src.mcp_tools.base_tool import BaseTool
from src.splunk.queries import SplunkQueries


class AuthTools(BaseTool):

    TOOL_NAME = "auth"

    def get_auth_logs(self, limit=10):
        query = SplunkQueries.get_auth_logs(limit)
        return self.execute(query)
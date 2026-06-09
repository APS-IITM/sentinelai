from src.mcp_tools.base_tool import BaseTool
from src.splunk.queries import SplunkQueries


class SecurityTools(BaseTool):

    TOOL_NAME = "security"

    def get_error_logs(self, limit=20):
        query = SplunkQueries.get_error_logs(limit)
        return self.execute(query)
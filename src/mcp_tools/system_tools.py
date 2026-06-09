from src.mcp_tools.base_tool import BaseTool
from src.splunk.queries import SplunkQueries


class SystemTools(BaseTool):

    TOOL_NAME = "system"

    def get_system_logs(self, limit=20):
        return self.execute(
            SplunkQueries.get_system_logs(limit)
        )

    def search_logs(self, keyword, limit=20):
        return self.execute(
            SplunkQueries.search_logs(keyword, limit)
        )

    def get_auth_logs(self, limit=20):
        return self.execute(
            SplunkQueries.get_auth_logs(limit)
        )

    def get_error_logs(self, limit=20):
        return self.execute(
            SplunkQueries.get_error_logs(limit)
        )

    def login_trend(self):
        return self.execute(
            SplunkQueries.login_trend()
        )

    def error_trend(self):
        return self.execute(
            SplunkQueries.error_trend()
        )
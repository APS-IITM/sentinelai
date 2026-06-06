from src.mcp_tools.base_tool import BaseTool
from src.splunk.queries import SplunkQueries


class SystemTools(BaseTool):

    def get_system_logs(self, limit=20):
        query = SplunkQueries.get_system_logs(limit)
        return self.execute(query)

    def search_logs(self, keyword, limit=20):
        query = SplunkQueries.search_logs(keyword, limit)
        return self.execute(query)

    def get_auth_logs(self, limit=20):
        query = SplunkQueries.get_auth_logs(limit)
        return self.execute(query)

    def get_error_logs(self, limit=20):
        query = SplunkQueries.get_error_logs(limit)
        return self.execute(query)

    def login_trend(self):
        query = SplunkQueries.login_trend()
        return self.execute(query)

    def error_trend(self):
        query = SplunkQueries.error_trend()
        return self.execute(query)
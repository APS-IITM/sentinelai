from src.mcp_tools.base_tool import BaseTool
from src.splunk.queries import SplunkQueries

class SecurityTools(BaseTool):
    """Handles everything related to access control, breaches, and authentication flaws."""
    TOOL_NAME = "security"

    def get_auth_logs(self, limit=20):
        return self.execute(SplunkQueries.get_auth_logs(limit))

    def login_trend(self):
        return self.execute(SplunkQueries.login_trend())

    def search_security_logs(self, keyword, limit=20):
        return self.execute(SplunkQueries.search_logs(keyword, limit))





class SystemHealthTools(BaseTool):
    """Tracks SIEM health, OS platform logs, and internal errors."""
    TOOL_NAME = "system_health"

    def get_system_logs(self, limit=20):
        return self.execute(SplunkQueries.get_system_logs(limit))

    def get_splunk_internal_errors(self, limit=20):
        return self.execute(SplunkQueries.get_splunk_internal_errors(limit))
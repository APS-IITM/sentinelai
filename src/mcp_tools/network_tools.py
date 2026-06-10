from src.mcp_tools.base_tool import BaseTool
from src.splunk.queries import SplunkQueries


class NetworkTools(BaseTool):
    """Handles network traffic telemetry, firewall logs, and edge detection."""
    TOOL_NAME = "network"

    def get_network_logs(self, limit=20):
        return self.execute(SplunkQueries.get_network_logs(limit))

    def network_trend(self):
        return self.execute(SplunkQueries.network_trend())

    def failed_connections(self, limit=20):
        return self.execute(SplunkQueries.failed_connections(limit))

    def top_source_ips(self, limit=20):
        return self.execute(SplunkQueries.top_source_ips(limit))

    def top_destination_ips(self, limit=20):
        return self.execute(SplunkQueries.top_destination_ips(limit))

    def port_scan_detection(self):
        return self.execute(SplunkQueries.port_scan_detection())
class SplunkQueries:

    @staticmethod
    def get_auth_logs(limit=20):
        return f"""
        search index=_internal ("login" OR "authentication")
        | stats count by user, host
        | sort -count
        | head {limit}
        """

    @staticmethod
    def get_error_logs(limit=20):
        return f"""
        search index=_internal ERROR
        | stats count by host, source
        | sort -count
        | head {limit}
        """

    @staticmethod
    def get_system_logs(limit=20):
        return f"""
        search index=_internal
        | stats count by sourcetype
        | sort -count
        | head {limit}
        """

    @staticmethod
    def search_logs(keyword, limit=20):
        return f"""
        search index=_internal "{keyword}"
        | stats count by host, sourcetype
        | head {limit}
        """

    @staticmethod
    def login_trend():
        return """
        search index=_internal "login"
        | bin _time span=5m
        | stats count by _time
        | sort _time
        """

    @staticmethod
    def error_trend():
        return """
        search index=_internal ERROR
        | bin _time span=5m
        | stats count by _time
        | sort _time
        """

    # ==========================
    # NETWORK LOGS
    # ==========================

    @staticmethod
    def get_network_logs(limit=20):
        return f"""
        search index=network
        | stats count by SRC, DST, PORT, ACTION
        | sort -count
        | head {limit}
        """

    @staticmethod
    def network_trend():
        return """
        search index=network
        | bin _time span=5m
        | stats count by _time
        | sort _time
        """

    @staticmethod
    def failed_connections(limit=20):
        return f"""
        search index=network ACTION=DENY
        | stats count by SRC, DST, PORT
        | sort -count
        | head {limit}
        """

    @staticmethod
    def top_source_ips(limit=20):
        return f"""
        search index=network
        | stats count by SRC
        | sort -count
        | head {limit}
        """

    @staticmethod
    def top_destination_ips(limit=20):
        return f"""
        search index=network
        | stats count by DST
        | sort -count
        | head {limit}
        """

    @staticmethod
    def port_scan_detection():
        return """
        search index=network
        | stats dc(PORT) as unique_ports by SRC
        | where unique_ports > 20
        | sort -unique_ports
        """
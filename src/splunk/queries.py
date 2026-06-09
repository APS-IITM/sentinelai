class SplunkQueries:

    # ==========================
    # AUTH
    # ==========================
    @staticmethod
    def get_auth_logs(limit=20, earliest="-24h"):
        return f"""
        search index=_internal earliest={earliest} ("login" OR "authentication")
        | stats count by user, host
        | sort -count
        | head {limit}
        """

    @staticmethod
    def login_trend():
        return """
        search index=_internal earliest=-24h "login"
        | bin _time span=5m
        | stats count by _time
        | sort _time
        """

    # ==========================
    # ERRORS
    # ==========================
    @staticmethod
    def get_error_logs(limit=20, earliest="-24h"):
        return f"""
        search index=_internal earliest={earliest} ERROR
        | stats count by host, source
        | sort -count
        | head {limit}
        """

    @staticmethod
    def error_trend():
        return """
        search index=_internal earliest=-24h ERROR
        | bin _time span=5m
        | stats count by _time
        | sort _time
        """

    # ==========================
    # SYSTEM
    # ==========================
    @staticmethod
    def get_system_logs(limit=20, earliest="-24h"):
        return f"""
        search index=_internal earliest={earliest}
        | stats count by sourcetype
        | sort -count
        | head {limit}
        """

    # ==========================
    # NETWORK
    # ==========================
    @staticmethod
    def network_trend():
        return """
        search index=network earliest=-24h
        | bin _time span=5m
        | stats count by _time
        | sort _time
        """

    @staticmethod
    def failed_connections(limit=20):
        return f"""
        search index=network ACTION=DENY earliest=-24h
        | stats count by SRC, DST, PORT
        | sort -count
        | head {limit}
        """

    @staticmethod
    def top_source_ips(limit=20):
        return f"""
        search index=network earliest=-24h
        | stats count by SRC
        | sort -count
        | head {limit}
        """

    @staticmethod
    def top_destination_ips(limit=20):
        return f"""
        search index=network earliest=-24h
        | stats count by DST
        | sort -count
        | head {limit}
        """

    @staticmethod
    def port_scan_detection():
        return """
        search index=network earliest=-24h
        | stats dc(PORT) as unique_ports by SRC
        | where unique_ports > 20
        | sort -unique_ports
        """
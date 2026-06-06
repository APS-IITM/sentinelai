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

    # 🔥 IMPORTANT FOR DAY 4 (ANOMALY DETECTION READY)
    @staticmethod
    def login_volume():
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
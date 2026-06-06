from src.splunk.client import (
    connect,
    run_search,
)


class SplunkQueries:
    def __init__(self):
        self.service = connect()

    def run_query(self, query):
        return run_search(
            self.service,
            query
        )

    def get_auth_logs(
        self,
        limit=20
    ):
        query = f"""
        search index=_internal
        ("login" OR "authentication")
        | head {limit}
        """

        return self.run_query(query)

    def get_error_logs(
        self,
        limit=20
    ):
        query = f"""
        search index=_internal ERROR
        | head {limit}
        """

        return self.run_query(query)

    def get_system_logs(
        self,
        limit=20
    ):
        query = f"""
        search index=_internal
        | head {limit}
        """

        return self.run_query(query)

    def search_logs(
        self,
        keyword,
        limit=20
    ):
        query = f"""
        search index=_internal "{keyword}"
        | head {limit}
        """

        return self.run_query(query)
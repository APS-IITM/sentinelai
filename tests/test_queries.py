from src.splunk.queries import SplunkQueries


def test_all_queries():
    splunk = SplunkQueries()

    print("\nAUTH LOGS")
    print("=" * 50)

    auth_logs = splunk.get_auth_logs()

    print(
        f"Retrieved {len(auth_logs)} logs"
    )

    print("\nERROR LOGS")
    print("=" * 50)

    error_logs = splunk.get_error_logs()

    print(
        f"Retrieved {len(error_logs)} logs"
    )

    print("\nSYSTEM LOGS")
    print("=" * 50)

    system_logs = splunk.get_system_logs()

    print(
        f"Retrieved {len(system_logs)} logs"
    )


if __name__ == "__main__":
    test_all_queries()
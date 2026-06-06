from src.splunk.queries import (
    SplunkQueries
)
from src.splunk.utills import (
    pretty_json
)


def print_logs(
    title,
    logs
):
    print(f"\n{title}")
    print("=" * 50)

    print(
        f"Total Logs: {len(logs)}"
    )

    if logs:
        print("\nSample Log:\n")
        print(
            pretty_json(
                logs[0]
            )
        )


def main():
    splunk = SplunkQueries()

    auth_logs = (
        splunk.get_auth_logs()
    )

    error_logs = (
        splunk.get_error_logs()
    )

    system_logs = (
        splunk.get_system_logs()
    )

    print_logs(
        "AUTH LOGS",
        auth_logs
    )

    print_logs(
        "ERROR LOGS",
        error_logs
    )

    print_logs(
        "SYSTEM LOGS",
        system_logs
    )


if __name__ == "__main__":
    main()
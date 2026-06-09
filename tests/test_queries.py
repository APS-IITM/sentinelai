"""
SentinelAI - Splunk Query Validation Test
"""

from src.splunk.queries import SplunkQueries
from src.utils.formatter import pretty_json


def main():

    splunk = SplunkQueries()

    print("\nAUTH LOGS")
    print("=" * 50)
    print(pretty_json(splunk.get_auth_logs()))

    print("\nERROR LOGS")
    print("=" * 50)
    print(pretty_json(splunk.get_error_logs()))

    print("\nSYSTEM LOGS")
    print("=" * 50)
    print(pretty_json(splunk.get_system_logs()))


if __name__ == "__main__":
    main()
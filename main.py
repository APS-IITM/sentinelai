from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools
from src.mcp_tools.network_tools import NetworkTools

from src.anomaly.analyzer import AnomalyAnalyzer

from src.utils.formatter import pretty_json


# =====================================
# DISPLAY MCP RESPONSE
# =====================================
def print_section(title, response):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    print(f"Success: {response.get('success')}")
    print(f"Total Records: {response.get('count')}")

    if response.get("error"):
        print(f"Error: {response['error']}")
        return

    data = response.get("data", [])

    if data:
        print("\nSample Record:\n")
        print(pretty_json(data[0]))


# =====================================
# EXTRACT TIME SERIES COUNTS
# =====================================
def extract_counts(response):

    data = response.get("data", [])

    values = []

    for item in data:

        if "count" in item:

            try:
                values.append(
                    int(item["count"])
                )

            except Exception:
                pass

    return values


# =====================================
# RUN ANOMALY DETECTION
# =====================================
def run_anomaly(engine, source, values):

    print("\n" + "=" * 70)
    print(f"ANOMALY RESULT : {source}")
    print("=" * 70)

    result = engine.analyze_series(
        source,
        values
    )

    if result:
        print(
            result.model_dump_json(
                indent=4
            )
        )
    else:
        print("No anomaly detected")


# =====================================
# MAIN
# =====================================
def main():

    # =================================
    # MCP TOOLS
    # =================================
    auth_tool = AuthTools()

    security_tool = SecurityTools()

    system_tool = SystemTools()

    network_tool = NetworkTools()

    # =================================
    # ANOMALY ENGINE
    # =================================
    anomaly_engine = AnomalyAnalyzer()

    # =================================
    # AUTH LOGS
    # =================================
    auth_logs = auth_tool.get_auth_logs(
        limit=20
    )

    print_section(
        "AUTH LOGS",
        auth_logs
    )

    # =================================
    # ERROR LOGS
    # =================================
    error_logs = security_tool.get_error_logs(
        limit=20
    )

    print_section(
        "ERROR LOGS",
        error_logs
    )

    # =================================
    # SYSTEM LOGS
    # =================================
    system_logs = system_tool.get_system_logs(
        limit=20
    )

    print_section(
        "SYSTEM LOGS",
        system_logs
    )

    # =================================
    # NETWORK LOGS
    # =================================
    network_logs = network_tool.get_network_logs(
        limit=20
    )

    print_section(
        "NETWORK LOGS",
        network_logs
    )

    # =================================
    # SEARCH LOGS
    # =================================
    search_logs = system_tool.search_logs(
        "login",
        limit=10
    )

    print_section(
        "SEARCH LOGS (LOGIN)",
        search_logs
    )

    # =================================
    # LOGIN TREND
    # =================================
    login_trend = system_tool.login_trend()

    print_section(
        "LOGIN TREND",
        login_trend
    )

    # =================================
    # ERROR TREND
    # =================================
    error_trend = system_tool.error_trend()

    print_section(
        "ERROR TREND",
        error_trend
    )

    # =================================
    # NETWORK TREND
    # =================================
    network_trend = network_tool.network_trend()

    print_section(
        "NETWORK TREND",
        network_trend
    )

    # =================================
    # EXTRACT TIME SERIES
    # =================================
    login_series = extract_counts(
        login_trend
    )

    error_series = extract_counts(
        error_trend
    )

    network_series = extract_counts(
        network_trend
    )

    print("\n" + "=" * 70)
    print("TIME SERIES DATA")
    print("=" * 70)

    print(
        f"Login Series: {login_series}"
    )

    print(
        f"Error Series: {error_series}"
    )

    print(
        f"Network Series: {network_series}"
    )

    # =================================
    # ANOMALY DETECTION
    # =================================
    if login_series:

        run_anomaly(
            anomaly_engine,
            "AUTHENTICATION",
            login_series
        )

    if error_series:

        run_anomaly(
            anomaly_engine,
            "ERROR_SYSTEM",
            error_series
        )

    if network_series:

        run_anomaly(
            anomaly_engine,
            "NETWORK_TRAFFIC",
            network_series
        )

    # =================================
    # NETWORK SECURITY CHECKS
    # =================================
    failed_connections = (
        network_tool.failed_connections()
    )

    print_section(
        "FAILED CONNECTIONS",
        failed_connections
    )

    top_sources = (
        network_tool.top_source_ips()
    )

    print_section(
        "TOP SOURCE IPS",
        top_sources
    )

    top_destinations = (
        network_tool.top_destination_ips()
    )

    print_section(
        "TOP DESTINATION IPS",
        top_destinations
    )

    port_scan = (
        network_tool.port_scan_detection()
    )

    print_section(
        "PORT SCAN DETECTION",
        port_scan
    )


if __name__ == "__main__":
    main()
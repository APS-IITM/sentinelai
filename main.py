from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools

from src.anomaly.analyzer import AnomalyAnalyzer

from src.utils.formatter import pretty_json


# =========================
# DISPLAY MCP RESPONSE
# =========================
def print_section(title, response):

    print("\n" + "=" * 70)
    print(f"{title}")
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


# =========================
# EXTRACT TIME SERIES
# =========================
def extract_counts(response):

    data = response.get("data", [])
    values = []

    for item in data:
        if "count" in item:
            try:
                values.append(int(item["count"]))
            except:
                pass

    return values


# =========================
# RUN ANOMALY ANALYSIS
# =========================
def run_anomaly(engine, source, values):

    result = engine.analyze_series(source, values)

    print("\n" + "=" * 70)
    print(f"ANOMALY RESULT: {source}")
    print("=" * 70)

    if result:
        print(result.model_dump_json(indent=4))
    else:
        print("No anomaly detected")


def main():

    # =====================
    # MCP LAYER INIT
    # =====================
    auth_tool = AuthTools()
    security_tool = SecurityTools()
    system_tool = SystemTools()

    # =====================
    # ANOMALY ENGINE INIT 
    # =====================
    anomaly_engine = AnomalyAnalyzer()

    # =====================
    # NORMAL LOGS 
    # =====================
    auth_logs = auth_tool.get_auth_logs(limit=20)
    print_section("AUTH LOGS", auth_logs)

    error_logs = security_tool.get_error_logs(limit=20)
    print_section("ERROR LOGS", error_logs)

    system_logs = system_tool.get_system_logs(limit=20)
    print_section("SYSTEM LOGS", system_logs)

    search_logs = system_tool.search_logs("login", limit=10)
    print_section("SEARCH LOGS (login)", search_logs)

    # =====================
    # INPUT STREAM (IMPORTANT)
    # =====================
    login_trend = system_tool.login_trend()
    print_section("LOGIN TREND (ANOMALY INPUT)", login_trend)

    error_trend = system_tool.error_trend()
    print_section("ERROR TREND (ANOMALY INPUT)", error_trend)

    # =====================
    # TIME SERIES EXTRACTION
    # =====================
    login_series = extract_counts(login_trend)
    error_series = extract_counts(error_trend)

    print("\n" + "=" * 70)
    print("TIME SERIES DATA (READY FOR ANOMALY ENGINE)")
    print("=" * 70)

    print("Login Series:", login_series)
    print("Error Series:", error_series)

    # =====================
    # ANOMALY DETECTION
    # =====================
    if login_series:
        run_anomaly(anomaly_engine, "AUTHENTICATION", login_series)

    if error_series:
        run_anomaly(anomaly_engine, "ERROR_SYSTEM", error_series)


if __name__ == "__main__":
    main()
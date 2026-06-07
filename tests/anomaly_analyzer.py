from src.mcp_tools.system_tools import SystemTools
from src.anomaly.analyzer import AnomalyAnalyzer

def extract_values(response):

    values = []

    for item in response.get("data", []):
        if "count" in item:
            try:
                values.append(int(item["count"]))
            except:
                pass

    return values


def main():

    tools = SystemTools()
    engine = AnomalyAnalyzer()

    # =====================
    # LOGIN ANOMALY
    # =====================
    login_data = tools.login_trend()
    login_values = extract_values(login_data)

    result = engine.analyze_series(
        "AUTHENTICATION",
        login_values
    )

    if result:
        print(result.model_dump_json(indent=4))
    else:
        print("No anomaly detected in AUTHENTICATION")

    # =====================
    # ERROR ANOMALY
    # =====================
    error_data = tools.error_trend()
    error_values = extract_values(error_data)

    result2 = engine.analyze_series(
        "ERROR_SYSTEM",
        error_values
    )

    if result2:
        print(result2.model_dump_json(indent=4))
    else:
        print("No anomaly detected in ERROR_SYSTEM")


if __name__ == "__main__":
    main()
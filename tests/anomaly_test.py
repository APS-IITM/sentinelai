"""
SentinelAI - Anomaly Engine Diagnostic Test
"""

from src.mcp_tools.system_tools import SystemTools
from src.anomaly.analyzer import AnomalyAnalyzer


def extract_values(response):
    if not response or not isinstance(response, dict):
        return []

    return [
        int(item["count"])
        for item in response.get("data", [])
        if "count" in item and str(item["count"]).isdigit()
    ]


def execute_test_stage(engine, source_name, values):

    print("\n" + "─" * 60)
    print(f"🔍 ANALYZING SUBSYSTEM: {source_name}")
    print("─" * 60)
    print(f"Time Series: {values}")

    try:
        result = engine.analyze_series(source_name, values)

        if result:
            print("🟢 [ANOMALY DETECTED]")
            print(result.model_dump_json(indent=2))
            return True
        else:
            print("⚪ [CLEAN] No anomaly detected")
            return False

    except TypeError as e:
        print(f"❌ Type Error: {e}")
        return False

    except Exception as e:
        print(f"❌ Execution Error: {e}")
        return False


def main():

    print("=" * 60)
    print(" SENTINELAI ANOMALY DIAGNOSTIC TEST ")
    print("=" * 60)

    tools = SystemTools()
    engine = AnomalyAnalyzer()

    try:
        login = extract_values(tools.login_trend())
        error = extract_values(tools.error_trend())

    except Exception:
        login = []
        error = []

    if not login or not error:
        print("💡 MOCK MODE ACTIVE")

        login = [12, 14, 11, 15, 13, 12, 450]
        error = [2, 1, 3, 2, 1, 180]

    execute_test_stage(engine, "AUTH", login)
    execute_test_stage(engine, "ERROR", error)

    print("\n✔ Diagnostic complete")


if __name__ == "__main__":
    main()
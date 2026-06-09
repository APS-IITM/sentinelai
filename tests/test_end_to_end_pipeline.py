"""
SentinelAI - Full End-to-End SOC Pipeline Test
"""

from src.mcp_tools.system_tools import SystemTools
from src.mcp_tools.network_tools import NetworkTools
from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine
from src.ai.analyzer import AIAnalyzer


def extract_values(response):
    if not response or not isinstance(response, dict):
        return []

    return [int(i["count"]) for i in response.get("data", []) if "count" in i]


def main():

    print("=" * 70)
    print(" SENTINELAI END-TO-END PIPELINE TEST ")
    print("=" * 70)

    system = SystemTools()
    network = NetworkTools()
    anomaly = AnomalyAnalyzer()
    intelligence = IntelligenceEngine()
    ai = AIAnalyzer()

    try:
        login = extract_values(system.login_trend())
        error = extract_values(system.error_trend())
        network_series = extract_values(network.network_trend())

    except Exception:
        print("💡 MOCK MODE")
        login = [10, 12, 11, 13, 240]
        error = [2, 3, 2, 180]
        network_series = [50, 48, 52, 1500]

    threats = []

    for name, series in [
        ("AUTH", login),
        ("ERROR", error),
        ("NETWORK", network_series)
    ]:
        t = anomaly.analyze_series(name, series)
        if t:
            threats.append(t)
            print(f"🚨 Anomaly detected: {name}")

    if not threats:
        print("✔ No threats detected")
        return

    report = intelligence.analyze(threats)

    print("\n📊 CTI REPORT")
    print(report.model_dump_json(indent=2))

    primary = threats[0]
    primary.description = f"Correlated incident: {report.incident_type}"
    primary.severity = report.severity

    print("\n🤖 AI ANALYSIS")
    print(ai.analyze_event(primary))


if __name__ == "__main__":
    main()
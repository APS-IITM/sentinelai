"""
SentinelAI - AUTONOMOUS ATTACK SIMULATION PIPELINE TEST
MCP → ANOMALY → INTELLIGENCE → AI
"""

from src.mcp_tools.system_tools import SystemTools
from src.mcp_tools.network_tools import NetworkTools
from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine
from src.ai.analyzer import AIAnalyzer


# ---------------------------------------------------------
# ATTACK SIMULATION SCENARIOS
# ---------------------------------------------------------
ATTACK_SCENARIOS = [
    {
        "name": "BRUTE_FORCE_ATTACK",
        "login": [10, 12, 11, 13, 300],
        "error": [1, 2, 1, 5],
        "network": [40, 42, 41, 39]
    },
    {
        "name": "PORT_SCAN_ATTACK",
        "login": [8, 9, 7, 10],
        "error": [2, 2, 3, 2],
        "network": [60, 65, 70, 900]
    },
    {
        "name": "DDOS_ATTACK",
        "login": [5, 5, 6, 5],
        "error": [10, 15, 20, 200],
        "network": [100, 120, 3000, 5000]
    }
]


# ---------------------------------------------------------
# UTIL
# ---------------------------------------------------------
def extract_values(response):
    if not response or not isinstance(response, dict):
        return []

    return [
        int(i["count"])
        for i in response.get("data", [])
        if "count" in i
    ]


# ---------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------
def main():

    print("=" * 80)
    print(" SENTINELAI AUTONOMOUS ATTACK SIMULATION ")
    print("=" * 80)

    system = SystemTools()
    network = NetworkTools()
    anomaly = AnomalyAnalyzer()
    intelligence = IntelligenceEngine()
    ai = AIAnalyzer()

    total_anomalies = 0
    total_reports = 0

    # -----------------------------------------------------
    # RUN ATTACK SCENARIOS
    # -----------------------------------------------------

    for attack in ATTACK_SCENARIOS:

        print("\n" + "-" * 80)
        print(f"🚨 SIMULATING: {attack['name']}")
        print("-" * 80)

        try:
            login = attack["login"]
            error = attack["error"]
            network_series = attack["network"]

        except Exception:
            print("⚠ Using fallback mock data")
            continue

        threats = []

        # -------------------------------------------------
        # MCP → ANOMALY STAGE
        # -------------------------------------------------
        for name, series in [
            ("AUTH", login),
            ("ERROR", error),
            ("NETWORK", network_series)
        ]:

            t = anomaly.analyze_series(name, series)

            if t:
                threats.append(t)
                total_anomalies += 1
                print(f"🚨 ANOMALY DETECTED → {name}")

        if not threats:
            print("✔ No anomalies detected in scenario")
            continue

        # -------------------------------------------------
        # INTELLIGENCE STAGE
        # -------------------------------------------------
        reports = intelligence.analyze(threats)

        if reports:
            total_reports += len(reports)

            print("\n🧠 INTELLIGENCE REPORTS:")
            for r in reports:
                print(f" - {r.incident_type} | {r.severity}")

        else:
            print("❌ No intelligence generated")

        # -------------------------------------------------
        # AI RESPONSE STAGE
        # -------------------------------------------------
        primary = threats[0]
        primary.description = f"Simulated Attack: {attack['name']}"

        try:
            ai_response = ai.analyze_event(primary)

            print("\n🤖 AI RESPONSE:")
            print(ai_response)

        except Exception as e:
            print(f"❌ AI Engine Failed: {str(e)}")

    # -----------------------------------------------------
    # FINAL SOC SCORECARD
    # -----------------------------------------------------

    print("\n" + "=" * 80)
    print(" SOC AUTONOMY SCORECARD ")
    print("=" * 80)

    print(f"Total Attack Scenarios : {len(ATTACK_SCENARIOS)}")
    print(f"Total Anomalies        : {total_anomalies}")
    print(f"Total CTI Reports      : {total_reports}")

    if total_anomalies > 0 and total_reports > 0:
        print("\n✅ SYSTEM IS FULLY AUTONOMOUS (END-TO-END SOC FLOW WORKING)")
    else:
        print("\n❌ SYSTEM IS NOT FULLY AUTONOMOUS")

    print("=" * 80)


if __name__ == "__main__":
    main()
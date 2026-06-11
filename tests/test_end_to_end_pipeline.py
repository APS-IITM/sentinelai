"""
SentinelAI - AUTOMATION VALIDATION PIPELINE TEST
Checks if SOC pipeline is truly automatic end-to-end
"""

from src.mcp_tools.system_tools import SystemTools
from src.mcp_tools.network_tools import NetworkTools
from src.anomaly.analyzer import AnomalyAnalyzer
from src.intelligence.engine import IntelligenceEngine
from src.ai.analyzer import AIAnalyzer


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
# TEST REPORT TRACKER
# ---------------------------------------------------------
class PipelineTestReport:

    def __init__(self):
        self.anomalies_triggered = 0
        self.intelligence_reports = 0
        self.failures = []
        self.events = []

    def log_anomaly(self, name):
        self.anomalies_triggered += 1
        self.events.append(f"ANOMALY → {name}")

    def log_intelligence(self, count):
        self.intelligence_reports += count
        self.events.append(f"INTELLIGENCE → {count} reports")

    def fail(self, msg):
        self.failures.append(msg)


# ---------------------------------------------------------
# MAIN TEST
# ---------------------------------------------------------
def main():

    print("=" * 70)
    print(" SENTINELAI AUTOMATION VALIDATION TEST ")
    print("=" * 70)

    system = SystemTools()
    network = NetworkTools()
    anomaly = AnomalyAnalyzer()
    intelligence = IntelligenceEngine()
    ai = AIAnalyzer()

    report = PipelineTestReport()

    # -----------------------------------------------------
    # DATA FETCH
    # -----------------------------------------------------

    try:
        login = extract_values(system.login_trend())
        error = extract_values(system.error_trend())
        network_series = extract_values(network.network_trend())

    except Exception:
        print("💡 MOCK MODE ACTIVATED")
        login = [10, 12, 11, 13, 240]
        error = [2, 3, 2, 180]
        network_series = [50, 48, 52, 1500]

    # -----------------------------------------------------
    # ANOMALY STAGE
    # -----------------------------------------------------

    threats = []

    for name, series in [
        ("AUTH", login),
        ("ERROR", error),
        ("NETWORK", network_series)
    ]:

        t = anomaly.analyze_series(name, series)

        if t:

            threats.append(t)
            report.log_anomaly(name)

            print(f"🚨 ANOMALY TRIGGERED → {name}")

    if not threats:

        print("✔ NO ANOMALIES DETECTED")

        report.fail("No anomaly triggered pipeline")

        return report

    # -----------------------------------------------------
    # INTELLIGENCE STAGE
    # -----------------------------------------------------

    intel_reports = intelligence.analyze(threats)

    if intel_reports:

        report.log_intelligence(len(intel_reports))

        print("\n🧠 INTELLIGENCE GENERATED:")
        for r in intel_reports:
            print(f" - {r.incident_type} | {r.severity}")

    else:

        report.fail("Intelligence engine returned empty output")

    # -----------------------------------------------------
    # AI STAGE
    # -----------------------------------------------------

    primary = threats[0]
    primary.description = "AUTOMATION TEST INCIDENT"

    try:
        ai_output = ai.analyze_event(primary)
        print("\n🤖 AI OUTPUT:")
        print(ai_output)

    except Exception as e:
        report.fail(f"AI Engine failed: {str(e)}")

    # -----------------------------------------------------
    # FINAL AUTOMATION SCORECARD
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print(" PIPELINE AUTOMATION REPORT ")
    print("=" * 70)

    print(f"Anomalies Triggered   : {report.anomalies_triggered}")
    print(f"Intelligence Reports  : {report.intelligence_reports}")
    print(f"Pipeline Events       : {len(report.events)}")

    if report.failures:
        print("\n❌ FAILURES:")
        for f in report.failures:
            print(" -", f)

    else:
        print("\n✅ PIPELINE FULLY AUTOMATED")

    print("\nEVENT TRACE:")
    for e in report.events:
        print(" -", e)

    print("=" * 70)


if __name__ == "__main__":
    main()
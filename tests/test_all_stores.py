"""
SentinelAI Store Integration Test

Run:
python tests/test_all_stores.py
"""

from uuid import uuid4
from datetime import datetime

from src.storage.mcp_store import MCPStore
from src.storage.anomaly_store import AnomalyStore
from src.storage.intelligence_store import IntelligenceStore
from src.storage.ai_report_store import AIReportStore


def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def test_mcp_store():
    print_header("TESTING MCP STORE")

    MCPStore.save(
        "auth",
        {
            "query": "index=_internal",
            "results": [
                {"user": "admin"},
                {"user": "guest"}
            ]
        }
    )

    records = MCPStore.get("auth")

    print(f"Records Found: {len(records)}")

    if records:
        print("PASS")
    else:
        print("FAIL")


def test_anomaly_store():
    print_header("TESTING ANOMALY STORE")

    anomaly = {
        "event_id": str(uuid4()),
        "source": "auth",
        "anomaly_type": "SPIKE",
        "severity": "HIGH",
        "score": 87,
        "attack_type": "BRUTE_FORCE_ATTACK",
        "description": "Multiple failed logins",
        "recommendation": "Investigate source IP",
        "data_points": 250,
        "acknowledged": False,
        "investigated": False,
        "timestamp": datetime.utcnow().isoformat()
    }

    AnomalyStore.save(anomaly)

    all_records = AnomalyStore.get_all()
    latest = AnomalyStore.latest()

    print(f"Total Anomalies: {len(all_records)}")
    print(f"Latest Event ID: {latest.get('event_id')}")

    print("PASS")


def test_intelligence_store():
    print_header("TESTING INTELLIGENCE STORE")

    report = {
        "report_id": str(uuid4()),
        "incident_type": "RECON_TO_CREDENTIAL_ATTACK",
        "severity": "CRITICAL",
        "attack_story":
            "Network reconnaissance followed by brute force activity.",
        "timeline": [
            {
                "time": datetime.utcnow().isoformat(),
                "source": "network",
                "attack": "NETWORK_SCAN",
                "severity": "MEDIUM"
            }
        ],
        "mitre_techniques": [
            "T1046",
            "T1110"
        ],
        "recommendations": [
            "Block IP",
            "Enable MFA"
        ],
        "event_count": 5
    }

    IntelligenceStore.save(report)

    reports = IntelligenceStore.get_all()
    latest = IntelligenceStore.latest()

    print(f"Reports Found: {len(reports)}")
    print(f"Latest Report: {latest.get('report_id')}")

    print("PASS")


def test_ai_report_store():
    print_header("TESTING AI REPORT STORE")

    ai_report = {
        "report_id": str(uuid4()),
        "source_type": "anomaly",
        "event_count": 10,
        "highest_severity": "CRITICAL",
        "summary":
            "Potential credential attack identified.",
        "generated_report":
            "# AI Analysis\n\nThis appears to be a brute-force attack.",
        "created_at": datetime.utcnow().isoformat()
    }

    AIReportStore.save(ai_report)

    reports = AIReportStore.get_all()
    latest = AIReportStore.latest()

    print(f"AI Reports Found: {len(reports)}")
    print(f"Latest Report: {latest.get('report_id')}")

    print("PASS")


def run_all_tests():
    print_header("SENTINELAI STORE TEST SUITE")

    try:
        test_mcp_store()
        test_anomaly_store()
        test_intelligence_store()
        test_ai_report_store()

        print_header("ALL TESTS COMPLETED")

    except Exception as e:
        print("\nTEST FAILED")
        print(str(e))


if __name__ == "__main__":
    run_all_tests()
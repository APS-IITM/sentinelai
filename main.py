"""
SentinelAI Service Layer
Used by Streamlit UI
"""

from src.storage.supabase_loader import (
    get_anomalies,
    save_anomaly,
    get_intel_reports,
    save_intel_report,
    get_ai_reports,
    save_ai_report,
    get_mcp,
)

from src.ai.analyzer import AIAnalyzer


# =====================================================
# MCP DATA
# =====================================================

def get_auth_data():
    return get_mcp("auth")


def get_network_data():
    return get_mcp("network")


def get_security_data():
    return get_mcp("security")


def get_system_data():
    return get_mcp("system")


def get_all_mcp_data():

    return {
        "auth": get_auth_data(),
        "network": get_network_data(),
        "security": get_security_data(),
        "system": get_system_data(),
    }


# =====================================================
# THREATS
# =====================================================

def get_all_anomalies():
    return get_anomalies()


def get_latest_anomalies(limit=10):

    data = get_anomalies()

    return sorted(
        data,
        key=lambda x: x.get("timestamp", ""),
        reverse=True
    )[:limit]


# =====================================================
# INTELLIGENCE
# =====================================================

def get_all_intelligence_reports():
    return get_intel_reports()


def get_latest_intelligence(limit=10):

    data = get_intel_reports()

    return sorted(
        data,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )[:limit]


# =====================================================
# AI REPORTS
# =====================================================

def get_all_ai_reports():
    return get_ai_reports()


def get_latest_ai_reports(limit=10):

    data = get_ai_reports()

    return sorted(
        data,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )[:limit]


# =====================================================
# MANUAL AI GENERATION
# =====================================================

def generate_ai_report(source_type="all"):

    analyzer = AIAnalyzer()

    return analyzer.generate_report(
        source_type=source_type
    )


# =====================================================
# DASHBOARD
# =====================================================

def get_dashboard_metrics():

    anomalies = get_anomalies()
    intelligence = get_intel_reports()
    ai_reports = get_ai_reports()

    return {
        "total_anomalies": len(anomalies),
        "total_intelligence": len(intelligence),
        "total_ai_reports": len(ai_reports),
    }


def get_soc_snapshot():

    return {
        "metrics": get_dashboard_metrics(),
        "latest_threats": get_latest_anomalies(5),
        "latest_intelligence": get_latest_intelligence(5),
        "latest_ai_reports": get_latest_ai_reports(5),
    }
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

# FIX 1: single import — removed duplicate inside generate_ai_report()
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
        "auth":     get_auth_data(),
        "network":  get_network_data(),
        "security": get_security_data(),
        "system":   get_system_data(),
    }


# =====================================================
# THREATS
# =====================================================

def get_all_anomalies():
    return get_anomalies()


def get_latest_anomalies(limit: int = 10, _data: list | None = None):
    
    data = _data if _data is not None else get_anomalies()
    return sorted(
        data,
        key=lambda x: x.get("timestamp") or "0000-00-00",   # FIX 4
        reverse=True,
    )[:limit]


# =====================================================
# INTELLIGENCE
# =====================================================

def get_all_intelligence_reports():
    return get_intel_reports()


def get_latest_intelligence(limit: int = 10, _data: list | None = None):
    """FIX 3 + FIX 4: same pattern as get_latest_anomalies."""
    data = _data if _data is not None else get_intel_reports()
    return sorted(
        data,
        key=lambda x: x.get("created_at") or "0000-00-00",  # FIX 4
        reverse=True,
    )[:limit]


# =====================================================
# AI REPORTS
# =====================================================

def get_all_ai_reports():
    return get_ai_reports()


def get_latest_ai_reports(limit: int = 10, _data: list | None = None):
    """FIX 3 + FIX 4: same pattern."""
    data = _data if _data is not None else get_ai_reports()
    return sorted(
        data,
        key=lambda x: x.get("created_at") or "0000-00-00",  # FIX 4
        reverse=True,
    )[:limit]


# =====================================================
# MANUAL AI GENERATION
# =====================================================

def generate_ai_report(wrapped_anomaly) -> str:
    
    try:
        analyzer = AIAnalyzer()
        return analyzer.analyze_event(wrapped_anomaly)
    except Exception as e:
        return f"⚠️ **AI Forensic Generation Failed:** {str(e)}"


# =====================================================
# DASHBOARD
# =====================================================

def get_dashboard_metrics(_anomalies=None, _intelligence=None, _ai_reports=None):
    
    def _safe_len(data, fetcher):
        if data is not None:
            return len(data)
        try:
            return len(fetcher())
        except Exception:
            return 0

    return {
        "total_anomalies":    _safe_len(_anomalies,    get_anomalies),
        "total_intelligence": _safe_len(_intelligence, get_intel_reports),
        "total_ai_reports":   _safe_len(_ai_reports,   get_ai_reports),
    }


def get_anomaly_source_distribution(_anomalies: list | None = None) -> dict:
    
    data = _anomalies if _anomalies is not None else get_anomalies()

    buckets = {"auth": 0, "network": 0, "security": 0, "system": 0}

    for row in data:
        src = str(row.get("source") or row.get("anomaly_type") or "system").lower()
        if "auth"     in src or "brute" in src or "credential" in src:
            buckets["auth"]     += 1
        elif "network" in src or "ddos" in src or "scan" in src:
            buckets["network"]  += 1
        elif "security" in src or "inject" in src or "xss" in src:
            buckets["security"] += 1
        else:
            buckets["system"]   += 1

    total = sum(buckets.values()) or 1   # avoid div/0
    return {k: round((v / total) * 100, 1) for k, v in buckets.items()}


def get_soc_snapshot():
    anomalies    = get_anomalies()
    intelligence = get_intel_reports()
    ai_reports   = get_ai_reports()

    return {
        "metrics":            get_dashboard_metrics(anomalies, intelligence, ai_reports),
        "latest_threats":     get_latest_anomalies(5,  _data=anomalies),
        "latest_intelligence": get_latest_intelligence(5, _data=intelligence),
        "latest_ai_reports":  get_latest_ai_reports(5,  _data=ai_reports),
        "source_distribution": get_anomaly_source_distribution(anomalies),
    }
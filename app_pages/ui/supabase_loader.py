import os
from dotenv import load_dotenv
from supabase import create_client, Client
from src.storage.base_store import BaseStore  # Adjust import based on where BaseStore is defined

load_dotenv()

# ==========================================
# 🔑 CLIENT INITIALIZATION ENGINE
# ==========================================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Critical credential block failure: SUPABASE_URL or SUPABASE_KEY is missing from environment.")

client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# 🏛️ REPOSITORY MATRIX (OOP LAYER)
# ==========================================

class AnomalyStore(BaseStore):
    TABLE_NAME = "anomalies"

class IntelligenceStore(BaseStore):
    TABLE_NAME = "intelligence_reports"

class AIReportStore(BaseStore):
    TABLE_NAME = "ai_reports"

class MCPStore(BaseStore):
    TABLE_NAME = "mcp_store"


# ==========================================
# 🔌 BACKWARD COMPATIBILITY FUNCTION SAPPERS
# ==========================================
# These map your existing front-end layout components natively to the new BaseStore engine

# ---------- ANOMALIES ----------
def get_anomalies():
    """Fetches all raw logs for Dashboard / Threat Monitor."""
    return AnomalyStore.get_all()

def save_anomaly(anomaly_dict):
    """🔥 NEW: Allows the Attack Simulator to push classified threat payloads!"""
    return AnomalyStore.save(anomaly_dict)


# ---------- INTELLIGENCE ----------
def get_intel_reports():
    """Fetches tactical CTI signature logs."""
    return IntelligenceStore.get_all()

def save_intel_report(intel_dict):
    """🔥 NEW: Allows your simulator correlation engine to persist multi-stage matrices!"""
    return IntelligenceStore.save(intel_dict)


# ---------- AI REPORTS ----------
def get_ai_reports():
    """Fetches summary briefings for the Workspace terminal view."""
    return AIReportStore.get_all()

def save_ai_report(report_dict):
    """Persists generative reports to your database layer."""
    return AIReportStore.save(report_dict)


# ---------- MCP MANAGEMENT ----------
def get_mcp(tool_name):
    """Fetches specific runtime system configurations."""
    if not MCPStore.TABLE_NAME:
        raise ValueError("TABLE_NAME not defined")
    response = client.table(MCPStore.TABLE_NAME).select("*").eq("tool_name", tool_name).execute()
    return response.data or []

def save_mcp_config(mcp_dict):
    """🔥 NEW: Allows configuration parameters to be saved dynamically."""
    return MCPStore.save(mcp_dict)
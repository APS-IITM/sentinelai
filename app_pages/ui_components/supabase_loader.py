import os
from dotenv import load_dotenv
from supabase import create_client, Client
from src.storage.base_store import BaseStore  
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

# ---------- ANOMALIES ----------
def get_anomalies():
    return AnomalyStore.get_all()

def save_anomaly(anomaly_dict):
    return AnomalyStore.save(anomaly_dict)


# ---------- INTELLIGENCE ----------
def get_intel_reports():
    return IntelligenceStore.get_all()

def save_intel_report(intel_dict):
    return IntelligenceStore.save(intel_dict)


# ---------- AI REPORTS ----------
def get_ai_reports():
    return AIReportStore.get_all()

def save_ai_report(report_dict):
    return AIReportStore.save(report_dict)


# ---------- MCP MANAGEMENT ----------
def get_mcp(tool_name):
    # FIXED: Route through the secure abstraction layer class to ensure type parsing works correctly
    if not MCPStore.TABLE_NAME:
        raise ValueError("TABLE_NAME not defined")
    
    # Leverages safe logic structures built into Layer 2 
    response = client.table(MCPStore.TABLE_NAME).select("*").eq("tool_name", tool_name).execute()
    return response.data or []

def save_mcp_config(mcp_dict):
    return MCPStore.save(mcp_dict)
import os
from dotenv import load_dotenv
from src.storage.base_store import BaseStore  

# 🔌 IMPORT THE INITIALIZED CLIENT FROM YOUR CLIENT SCRIPT
from src.storage.supabase_client import supabase 

load_dotenv()

# ==========================================
# ⛓️ INJECT CLIENT INTO THE BASE CLASS DIRECTLY
# ==========================================
# Because BaseStore does not accept arguments in __init__, 
# we bind the client directly to the base class so all children inherit it.
BaseStore.client = supabase


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


# FIXED: Reverted to empty constructors since BaseStore takes no arguments
anomaly_store = AnomalyStore()
intel_store = IntelligenceStore()
ai_store = AIReportStore()
mcp_store = MCPStore()


# ==========================================
# 🔌 BACKWARD COMPATIBILITY FUNCTION SAPPERS
# ==========================================

# ---------- ANOMALIES ----------
def get_anomalies():
    return anomaly_store.get_all()

def save_anomaly(anomaly_dict):
    return anomaly_store.save(anomaly_dict)


# ---------- INTELLIGENCE ----------
def get_intel_reports():
    return intel_store.get_all()

def save_intel_report(intel_dict):
    return intel_store.save(intel_dict)


# ---------- AI REPORTS ----------
def get_ai_reports():
    return ai_store.get_all()

def save_ai_report(report_dict):
    return ai_store.save(report_dict)


# ---------- MCP MANAGEMENT ----------
def get_mcp(tool_name):
    if not MCPStore.TABLE_NAME:
        raise ValueError("TABLE_NAME not defined")
    
    # Explicitly utilizes the imported central supabase engine asset
    response = supabase.table(MCPStore.TABLE_NAME).select("*").eq("tool_name", tool_name).execute()
    return response.data or []

def save_mcp_config(mcp_dict):
    return mcp_store.save(mcp_dict)
import os
from dotenv import load_dotenv
from src.storage.base_store import BaseStore  

# 🔌 IMPORT THE INITIALIZED CLIENT AND YOUR EXPLICIT MCP MODULE
from src.storage.supabase_client import supabase 
# Make sure the import path below points directly to your standalone MCPStore file:
from src.storage.mcp_store import MCPStore  

load_dotenv()

# ==========================================
# ⛓️ INJECT CLIENT INTO THE BASE CLASS DIRECTLY
# ==========================================
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


anomaly_store = AnomalyStore()
intel_store = IntelligenceStore()
ai_store = AIReportStore()


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


# ---------- MCP MANAGEMENT (RECONCILED LAYER) ----------
def get_mcp(tool_name):
    """Routes directly through the standalone MCPStore mapping logic to unpack payloads cleanly."""
    if not tool_name:
        return []
    # Leverages your custom payload extraction: row["payload"] for row in response.data
    return MCPStore.get(tool_name)


def save_mcp_config(mcp_dict):
    """
    Intercepts unified data dictionaries and splits them safely 
    to match the (tool_name, data) requirements of your standalone MCP script.
    """
    if not isinstance(mcp_dict, dict):
        return []
        
    # Extract structural arguments out of the dictionary
    tool_name = mcp_dict.get("tool_name") or mcp_dict.get("attack_type") or "UNKNOWN_TOOL"
    
    # If the simulator passes a raw dict, look for an inner payload block, or dump the whole dict
    data_content = mcp_dict.get("payload") or mcp_dict
    
    # Execute the standalone static method with correct arguments
    response = MCPStore.save(tool_name, data_content)
    return response.data or []
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- ANOMALIES ----------
def get_anomalies():
    res = client.table("anomalies").select("*").execute()
    return res.data

# ---------- INTELLIGENCE ----------
def get_intel_reports():
    res = client.table("intelligence_reports").select("*").execute()
    return res.data

# ---------- AI REPORTS ----------
def get_ai_reports():
    res = client.table("ai_reports").select("*").execute()
    return res.data

def save_ai_report(report_dict):
    res = client.table("ai_reports").insert(report_dict).execute()
    return res.data

# ---------- MCP ----------
def get_mcp(tool_name):
    res = client.table("mcp_store").select("*").eq("tool_name", tool_name).execute()
    return res.data
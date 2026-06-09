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


# ---------- MCP ----------
def get_mcp(tool):
    res = client.table("mcp_store").select("*").eq("tool", tool).execute()
    return res.data
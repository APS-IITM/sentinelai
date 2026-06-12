"""
SentinelAI Splunk Dashboard
LIVE MODE: Real-time MCP + Daemon Feed + Alerts
"""

import time
import pandas as pd
import streamlit as st

from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.network_tools import NetworkTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools

from src.alerts.global_alerts import GlobalAlertStore


# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="SentinelAI Splunk Live Dashboard",
    layout="wide"
)

st.title("⚙️ SentinelAI Splunk Live Stream")
st.caption("Real-time MCP → Splunk → Daemon → Alert Pipeline")

st.divider()


# ==========================================================
# LIVE CACHE (IN-MEMORY REAL TIME STORE)
# ==========================================================
class LiveCache:
    """
    Lightweight in-memory cache updated by daemon OR MCPStore sync.
    This is your REAL replacement for simulation.
    """

    _store = {
        "auth": [],
        "network": [],
        "security": [],
        "system": []
    }

    _last_update = 0

    @classmethod
    def push(cls, category: str, data: dict):
        if category not in cls._store:
            cls._store[category] = []

        cls._store[category].append(data)
        cls._last_update = time.time()

    @classmethod
    def get(cls, category: str):
        return cls._store.get(category, [])

    @classmethod
    def get_all(cls):
        return cls._store

    @classmethod
    def clear(cls):
        cls._store = {"auth": [], "network": [], "security": [], "system": []}


# ==========================================================
# SYNC FROM DAEMON 
# ==========================================================
def sync_from_daemon():
    """
    REAL FLOW:
    Daemon → MCPStore (Supabase) → Dashboard Cache

    Replace Supabase fetch if you want pure socket streaming later.
    """

    try:
        from src.storage.mcp_store import MCPStore

        # pull latest tool logs (REAL DAEMON OUTPUT)
        for tool in ["auth", "network", "security", "system"]:
            records = MCPStore.get(tool)

            if records:
                for r in records:
                    LiveCache.push(tool, r)

    except Exception as e:
        st.warning(f"Cache sync failed: {e}")


# ==========================================================
# AUTO SYNC (FAST LIGHTWEIGHT)
# ==========================================================
sync_from_daemon()


# ==========================================================
# TOOL INIT (ONLY IF NEEDED FOR DIRECT QUERY)
# ==========================================================
auth = AuthTools()
network = NetworkTools()
security = SecurityTools()
system = SystemTools()


# ==========================================================
# METRICS (FAST CACHE READ)
# ==========================================================
auth_logs = LiveCache.get("auth")
network_logs = LiveCache.get("network")
security_logs = LiveCache.get("security")
system_logs = LiveCache.get("system")


col1, col2, col3, col4 = st.columns(4)

col1.metric("Auth Events", len(auth_logs))
col2.metric("Network Events", len(network_logs))
col3.metric("Security Events", len(security_logs))
col4.metric("System Events", len(system_logs))

st.divider()


# ==========================================================
# ALERT ENGINE (GLOBAL DAEMON ALERTS)
# ==========================================================
st.subheader("🚨 Live Alerts")

alerts = GlobalAlertStore.get_latest() if hasattr(GlobalAlertStore, "get_latest") else []

if alerts:
    for alert in alerts[-5:]:
        st.error(f"⚠️ {alert.get('message', 'Anomaly detected')}")
else:
    st.success("System Stable (No Active Alerts)")


# ==========================================================
# EVENT FLOW GRAPH (MINIMAL FAST LINE CHART)
# ==========================================================
st.subheader("📈 Live Event Flow")

df = pd.DataFrame({
    "source": ["auth", "network", "security", "system"],
    "count": [
        len(auth_logs),
        len(network_logs),
        len(security_logs),
        len(system_logs)
    ]
})

st.line_chart(df.set_index("source"))


# ==========================================================
# LOG TABLES (FAST VIEW)
# ==========================================================
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Auth", "Network", "Security", "System"]
)

with tab1:
    st.dataframe(auth_logs, use_container_width=True)

with tab2:
    st.dataframe(network_logs, use_container_width=True)

with tab3:
    st.dataframe(security_logs, use_container_width=True)

with tab4:
    st.dataframe(system_logs, use_container_width=True)


# ==========================================================
# LIVE AUTO REFRESH (FAST LOOP)
# ==========================================================
time.sleep(2)   # low latency refresh

st.rerun()
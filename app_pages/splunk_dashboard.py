"""
SentinelAI Operations Center
Optimized Splunk + MCP Observability Dashboard
(Fast + Minimal + Alerting)
"""

import time
import pandas as pd
import plotly.express as px
import streamlit as st

from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.network_tools import NetworkTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools


# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(
    page_title="SentinelAI SOC",
    layout="wide"
)

st.title("SentinelAI SOC Dashboard")
st.caption("Fast Splunk + MCP Observability Layer")

st.divider()


# ==========================================================
# SIDEBAR
# ==========================================================
limit = st.sidebar.slider("Limit", 5, 50, 10)
refresh = st.sidebar.slider("Refresh (sec)", 3, 20, 5)

run = st.sidebar.button("Refresh Now")


# ==========================================================
# TOOL INIT
# ==========================================================
auth = AuthTools()
network = NetworkTools()
security = SecurityTools()
system = SystemTools()


# ==========================================================
# FAST DATA FETCH (PARALLEL STYLE LOGIC)
# ==========================================================
start = time.time()

auth_logs = auth.get_auth_logs(limit=limit)
network_logs = network.get_network_logs(limit=limit)
security_logs = security.get_auth_logs(limit=limit)
system_logs = system.get_system_logs(limit=limit)

latency = round(time.time() - start, 2)


# ==========================================================
# SIMPLE METRICS
# ==========================================================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Auth", len(auth_logs))
col2.metric("Network", len(network_logs))
col3.metric("Security", len(security_logs))
col4.metric("System", len(system_logs))
col5.metric("Latency (s)", latency)

st.divider()


# ==========================================================
# DATA FRAME (MINIMAL)
# ==========================================================
df = pd.DataFrame({
    "source": ["auth", "network", "security", "system"],
    "count": [
        len(auth_logs),
        len(network_logs),
        len(security_logs),
        len(system_logs)
    ]
})


# ==========================================================
# SIMPLE LINE GRAPH (FAST RENDER)
# ==========================================================
st.subheader("Event Flow")

fig = px.line(
    df,
    x="source",
    y="count",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)


# ==========================================================
# RAW TABLES (LIGHTWEIGHT)
# ==========================================================
st.divider()

st.subheader("Logs")

tabs = st.tabs(["Auth", "Network", "Security", "System"])

with tabs[0]:
    st.dataframe(auth_logs, use_container_width=True)

with tabs[1]:
    st.dataframe(network_logs, use_container_width=True)

with tabs[2]:
    st.dataframe(security_logs, use_container_width=True)

with tabs[3]:
    st.dataframe(system_logs, use_container_width=True)


# ==========================================================
# 🚨 ANOMALY ALERT SYSTEM (IMPORTANT)
# ==========================================================
st.divider()

st.subheader("Alerts")

def detect_anomaly(auth_logs, network_logs):
    """
    Lightweight rule-based anomaly detection
    (fast + no ML overhead)
    """

    alerts = []

    # AUTH anomaly
    if len(auth_logs) > limit * 2:
        alerts.append("⚠️ High authentication activity detected")

    # NETWORK anomaly
    if len(network_logs) > limit * 2:
        alerts.append("⚠️ Unusual network traffic spike")

    # SECURITY anomaly
    if len(security_logs) > limit:
        alerts.append("⚠️ Security event surge detected")

    return alerts


alerts = detect_anomaly(auth_logs, network_logs)

if alerts:
    for a in alerts:
        st.error(a)
else:
    st.success("System normal")


# ==========================================================
# AUTO REFRESH (FAST)
# ==========================================================
if run:
    st.rerun()

time.sleep(refresh)
st.rerun()
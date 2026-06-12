import streamlit as st
import pandas as pd
import time

from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.network_tools import NetworkTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SentinelAI Splunk Dashboard",
    layout="wide"
)

st.title("⚙️ SentinelAI Splunk Data Dashboard")
st.caption("Direct MCP → Splunk Query Visibility Layer")

st.markdown("---")

# =========================
# INIT TOOLS
# =========================
auth = AuthTools()
network = NetworkTools()
security = SecurityTools()
system = SystemTools()

# =========================
# SIDEBAR CONTROLS
# =========================
st.sidebar.header("Controls")

limit = st.sidebar.slider("Result Limit", 5, 50, 10)
refresh = st.sidebar.slider("Auto Refresh (sec)", 5, 60, 10)

run = st.sidebar.button("🔄 Refresh Now")

# =========================
# FETCH DATA
# =========================
with st.spinner("Querying Splunk via MCP tools..."):

    start = time.time()

    auth_logs = auth.get_auth_logs(limit=limit)
    network_logs = network.get_network_logs(limit=limit)
    security_logs = security.get_auth_logs(limit=limit)
    system_logs = system.get_system_logs(limit=limit)

    latency = time.time() - start

# =========================
# METRICS
# =========================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Auth Logs", len(auth_logs))
col2.metric("Network Logs", len(network_logs))
col3.metric("Security Logs", len(security_logs))
col4.metric("System Logs", len(system_logs))
col5.metric("Query Time (sec)", round(latency, 2))

st.markdown("---")

# =========================
# AUTH TABLE
# =========================
st.subheader("🔐 Auth Logs (Splunk)")

if auth_logs:
    st.dataframe(pd.DataFrame(auth_logs), use_container_width=True)
else:
    st.warning("No auth logs returned")

# =========================
# NETWORK TABLE
# =========================
st.subheader("🌐 Network Logs (Splunk)")

if network_logs:
    st.dataframe(pd.DataFrame(network_logs), use_container_width=True)
else:
    st.warning("No network logs returned")

# =========================
# SECURITY TABLE
# =========================
st.subheader("🛡️ Security Logs (Splunk)")

if security_logs:
    st.dataframe(pd.DataFrame(security_logs), use_container_width=True)
else:
    st.warning("No security logs returned")

# =========================
# SYSTEM TABLE
# =========================
st.subheader("⚙️ System Logs (Splunk)")

if system_logs:
    st.dataframe(pd.DataFrame(system_logs), use_container_width=True)
else:
    st.warning("No system logs returned")

# =========================
# DEBUG VIEW (OPTIONAL)
# =========================
with st.expander("🔍 Debug View (Raw MCP Output)"):

    st.json({
        "auth_sample": auth_logs[:2] if auth_logs else [],
        "network_sample": network_logs[:2] if network_logs else [],
        "security_sample": security_logs[:2] if security_logs else [],
        "system_sample": system_logs[:2] if system_logs else []
    })

# =========================
# AUTO REFRESH
# =========================
time.sleep(refresh)

if run:
    st.rerun()
else:
    st.rerun()
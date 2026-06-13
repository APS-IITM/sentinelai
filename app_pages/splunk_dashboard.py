"""
SentinelAI Splunk Dashboard
LIVE MODE: Real-time MCP + Daemon Feed + Alerts + Bounded RAM Log Stream
"""

import sys
import time
import socket
import threading
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

MAX_RAM_BYTES = 10 * 1024 * 1024 

if "terminal_logs" not in st.session_state:
    st.session_state["terminal_logs"] = []
if "terminal_bytes" not in st.session_state:
    st.session_state["terminal_bytes"] = 0

# ==========================================================
# THREAD-SAFE MEMORY MANAGEMENT HOOK
# ==========================================================
def push_terminal_log_to_state(log_line: str):
    formatted_line = log_line if log_line.endswith("\n") else f"{log_line}\n"
    line_bytes = sys.getsizeof(formatted_line)

    if st.session_state["terminal_bytes"] + line_bytes > MAX_RAM_BYTES:
        target_eviction_bytes = MAX_RAM_BYTES * 0.20
        freed_bytes = 0
        evict_count = 0
        
        for line in st.session_state["terminal_logs"]:
            freed_bytes += sys.getsizeof(line)
            evict_count += 1
            if freed_bytes >= target_eviction_bytes:
                break
                
        st.session_state["terminal_logs"] = st.session_state["terminal_logs"][evict_count:]
        st.session_state["terminal_bytes"] -= freed_bytes
        
        rotation_msg = f"--- [SYSTEM] RAM Limit Reached. Evicted oldest 20% ({evict_count} lines) ---\n"
        st.session_state["terminal_logs"].insert(0, rotation_msg)
        st.session_state["terminal_bytes"] += sys.getsizeof(rotation_msg)

    st.session_state["terminal_logs"].append(formatted_line)
    st.session_state["terminal_bytes"] += line_bytes

# ==========================================================
# BACKGROUND IN-MEMORY SOCKET SERVER
# ==========================================================
def run_log_server_listener():
    """Stable RAM socket listener for SplunkDaemon log stream"""

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("127.0.0.1", 5555))
    server_sock.listen(5)

    while True:
        client_conn = None
        try:
            client_conn, _ = server_sock.accept()
            buffer = ""

            while True:
                data = client_conn.recv(4096)
                if not data:
                    break

                # decode safely
                buffer += data.decode("utf-8", errors="ignore")

                # SAFE PARSING (handles partial Loguru bursts)
                while True:
                    if "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                    else:
                        # handle large single log bursts without newline
                        if len(buffer) > 500:
                            line, buffer = buffer[:500], buffer[500:]
                        else:
                            break

                    line = line.strip()
                    if line:
                        push_terminal_log_to_state(line)

        except Exception:
            pass
        finally:
            if client_conn:
                try:
                    client_conn.close()
                except Exception:
                    pass

# Start background server exactly once within the session state context
if "server_started" not in st.session_state:
    st.session_state["server_started"] = True
    threading.Thread(target=run_log_server_listener, daemon=True).start()

# Start background server exactly once within the session state context
if "server_started" not in st.session_state:
    st.session_state["server_started"] = True
    threading.Thread(target=run_log_server_listener, daemon=True).start()

# ==========================================================
# METRIC SYNCHRONIZATION
# ==========================================================
class LiveCache:
    _store = {"auth": [], "network": [], "security": [], "system": []}

    @classmethod
    def push(cls, category: str, data: dict):
        if category not in cls._store: cls._store[category] = []
        cls._store[category].append(data)

    @classmethod
    def get(cls, category: str):
        return cls._store.get(category, [])

def sync_from_daemon():
    try:
        from src.storage.mcp_store import MCPStore
        for tool in ["auth", "network", "security", "system"]:
            records = MCPStore.get(tool)
            if records:
                for r in records: 
                    LiveCache.push(tool, r)
    except Exception:
        pass

sync_from_daemon()

auth_logs = LiveCache.get("auth")
network_logs = LiveCache.get("network")
security_logs = LiveCache.get("security")
system_logs = LiveCache.get("system")

# ==========================================================
# UI LAYOUT
# ==========================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Auth Events", len(auth_logs))
col2.metric("Network Events", len(network_logs))
col3.metric("Security Events", len(security_logs))
col4.metric("System Events", len(system_logs))

st.divider()

st.subheader("🚨 Live Alerts")
alerts = GlobalAlertStore.get_latest() if hasattr(GlobalAlertStore, "get_latest") else []
if alerts:
    for alert in alerts[-5:]:
        st.error(f"⚠️ {alert.get('message', 'Anomaly detected')}")
else:
    st.success("System Stable (No Active Alerts)")

st.subheader("📈 Live Event Flow")
df = pd.DataFrame({
    "source": ["auth", "network", "security", "system"],
    "count": [len(auth_logs), len(network_logs), len(security_logs), len(system_logs)]
})
st.line_chart(df.set_index("source"))

st.divider()
tab1, tab2, tab3, tab4 = st.tabs(["Auth", "Network", "Security", "System"])
with tab1: st.dataframe(auth_logs, use_container_width=True)
with tab2: st.dataframe(network_logs, use_container_width=True)
with tab3: st.dataframe(security_logs, use_container_width=True)
with tab4: st.dataframe(system_logs, use_container_width=True)

# ==========================================================
# 💻 LIVE TERMINAL CONSOLE FEED (RAM CEILING TRACKED)
# ==========================================================
st.divider()
st.subheader("💻 Live Splunk Daemon Console Feed")

current_usage_mb = st.session_state["terminal_bytes"] / (1024 * 1024)
st.caption(f"**In-Memory Buffer Telemetry:** Using **{current_usage_mb:.4f} MB** / 10.0000 MB Ceiling Cap.")

MAX_RENDER_LINES = 250

logs = st.session_state["terminal_logs"]

terminal_output = "".join(logs[-MAX_RENDER_LINES:])



if terminal_output.strip():
    st.code(terminal_output, language="bash")
else:
    st.info("🔄 Socket initialized. Awaiting next collection loop cycle from SplunkDaemon...")

# Low latency view loop refresh 
time.sleep(2)
st.rerun()
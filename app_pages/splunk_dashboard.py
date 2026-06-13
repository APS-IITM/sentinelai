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

from src.alerts.global_alerts import GlobalAlertStore

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="SentinelAI Splunk Live Dashboard",
    layout="wide",
)

st.title("⚙️ SentinelAI Splunk Live Stream")
st.caption("Real-time MCP → Splunk → Daemon → Alert Pipeline")
st.divider()

MAX_RAM_BYTES   = 10 * 1024 * 1024   # 10 MB ceiling
MAX_RENDER_LINES = 250

# ==========================================================
# SESSION STATE BOOTSTRAP  (run once per browser session)
# ==========================================================
if "terminal_logs"    not in st.session_state:
    st.session_state["terminal_logs"]    = []
if "terminal_bytes"   not in st.session_state:
    st.session_state["terminal_bytes"]   = 0
if "socket_started"   not in st.session_state:
    st.session_state["socket_started"]   = False   # FIX 2: single flag, checked once

# ==========================================================
# THREAD-SAFE MEMORY MANAGEMENT
# ==========================================================
_log_lock = threading.Lock()

def push_log(line: str):
    """Append a log line to session state, evicting oldest 20% when over RAM ceiling."""
    formatted = line.strip() + "\n"
    line_bytes = sys.getsizeof(formatted)

    with _log_lock:
        # Evict oldest 20% if ceiling reached
        if st.session_state["terminal_bytes"] + line_bytes > MAX_RAM_BYTES:
            target = MAX_RAM_BYTES * 0.20
            freed, count = 0, 0
            for old_line in st.session_state["terminal_logs"]:
                freed += sys.getsizeof(old_line)
                count += 1
                if freed >= target:
                    break

            st.session_state["terminal_logs"]  = st.session_state["terminal_logs"][count:]
            st.session_state["terminal_bytes"] -= freed

            notice = f"--- [SYSTEM] RAM ceiling reached — evicted {count} oldest lines ---\n"
            st.session_state["terminal_logs"].insert(0, notice)
            st.session_state["terminal_bytes"] += sys.getsizeof(notice)

        st.session_state["terminal_logs"].append(formatted)
        st.session_state["terminal_bytes"] += line_bytes


def _socket_reader_thread():
    """
    Background thread: connect to SplunkDaemon's log socket as a CLIENT
    and push every line into session_state.
    Reconnects automatically if the daemon restarts.
    """
    while True:
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", 5555))          # CLIENT: connect, not bind
            push_log("[DASHBOARD] Connected to SplunkDaemon log stream")

            buffer = ""
            while True:
                data = sock.recv(4096)
                if not data:
                    push_log("[DASHBOARD] Daemon closed connection — reconnecting...")
                    break

                buffer += data.decode("utf-8", errors="ignore")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if line:
                        push_log(line)

                # Flush oversized buffers without a newline (rare Loguru burst)
                if len(buffer) > 500:
                    push_log(buffer[:500])
                    buffer = buffer[500:]

        except ConnectionRefusedError:
            push_log("[DASHBOARD] Daemon not reachable on :5555 — retrying in 3s...")
        except Exception as e:
            push_log(f"[DASHBOARD] Socket error: {e} — retrying in 3s...")
        finally:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass

        time.sleep(3)   # wait before reconnect attempt



if not st.session_state["socket_started"]:
    st.session_state["socket_started"] = True
    threading.Thread(target=_socket_reader_thread, daemon=True).start()


# ==========================================================
# METRIC SYNC FROM STORAGE
# ==========================================================
def fetch_live_counts() -> dict:
    """Pull current event counts from MCPStore each cycle."""
    counts = {"auth": 0, "network": 0, "security": 0, "system": 0}
    try:
        from src.storage.mcp_store import MCPStore
        for tool in counts:
            records = MCPStore.get(tool)
            counts[tool] = len(records) if records else 0
    except Exception:
        pass
    return counts

def fetch_live_tables() -> dict:
    """Pull full records for the tab dataframes."""
    tables = {"auth": [], "network": [], "security": [], "system": []}
    try:
        from src.storage.mcp_store import MCPStore
        for tool in tables:
            records = MCPStore.get(tool)
            if records:
                tables[tool] = records
    except Exception:
        pass
    return tables


counts = fetch_live_counts()
tables = fetch_live_tables()

# ==========================================================
# UI — METRICS ROW
# ==========================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Auth Events",     counts["auth"])
col2.metric("Network Events",  counts["network"])
col3.metric("Security Events", counts["security"])
col4.metric("System Events",   counts["system"])

st.divider()

# ==========================================================
# UI — LIVE ALERTS
# FIX 4: read 'title' key (matches what daemon pushes)
# ==========================================================
st.subheader("🚨 Live Alerts")

try:
    alerts = GlobalAlertStore.get_latest() if hasattr(GlobalAlertStore, "get_latest") else []
except Exception:
    alerts = []

if alerts:
    for alert in alerts[-5:]:
        severity   = str(alert.get("severity", "MEDIUM")).upper()
        title      = alert.get("title", "Anomaly detected")          # FIX 4
        attack     = alert.get("attack_type", "unknown")
        summary    = alert.get("summary", "")
        src_events = alert.get("source_events", "?")

        color_fn = st.error if severity in ("HIGH", "CRITICAL") else st.warning
        color_fn(f"⚠️ [{severity}] {title} — {attack} | {src_events} events | {summary}")
else:
    st.success("✅ System Stable — No Active Alerts")

st.divider()

# ==========================================================
# UI — LIVE EVENT FLOW CHART
# ==========================================================
st.subheader("📈 Live Event Flow")
chart_df = pd.DataFrame({
    "source": ["auth", "network", "security", "system"],
    "count":  [counts["auth"], counts["network"], counts["security"], counts["system"]],
})
st.bar_chart(chart_df.set_index("source"))   # bar chart suits discrete buckets better than line

st.divider()

# ==========================================================
# UI — EVENT TABS
# ==========================================================
tab1, tab2, tab3, tab4 = st.tabs(["Auth", "Network", "Security", "System"])
with tab1: st.dataframe(tables["auth"],     use_container_width=True)
with tab2: st.dataframe(tables["network"],  use_container_width=True)
with tab3: st.dataframe(tables["security"], use_container_width=True)
with tab4: st.dataframe(tables["system"],   use_container_width=True)

st.divider()

# ==========================================================
# UI — LIVE TERMINAL CONSOLE
# ==========================================================
st.subheader("💻 Live Splunk Daemon Console Feed")

used_mb = st.session_state["terminal_bytes"] / (1024 * 1024)
st.caption(
    f"In-memory buffer: **{used_mb:.4f} MB** / 10.00 MB ceiling  |  "
    f"Lines buffered: **{len(st.session_state['terminal_logs'])}**"
)

with _log_lock:
    logs_snapshot = list(st.session_state["terminal_logs"])

terminal_output = "".join(logs_snapshot[-MAX_RENDER_LINES:])

if terminal_output.strip():
    st.code(terminal_output, language="bash")
else:
    st.info("🔄 Connecting to SplunkDaemon on :5555 — waiting for first log burst...")

# ==========================================================
# FIX 3: Auto-rerun — use st.fragment or a simple sleep+rerun.
# The 2s sleep is fine but we snapshot state safely above first.
# ==========================================================
time.sleep(2)
st.rerun()
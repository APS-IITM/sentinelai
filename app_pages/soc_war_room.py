import streamlit as st
from datetime import datetime

from src.simulator.engine import AttackEngine
from src.simulator.state import AttackState

# =========================
# PRODUCTION PAGE CONFIG
# =========================
st.set_page_config(page_title="SOC War Room", layout="wide")

# Safe instantiation tied directly to Streamlit Session State Lifecycle
if "attack_engine" not in st.session_state:
    st.session_state.attack_engine = AttackEngine()

# Consolidated UX Theme styling
st.markdown("""
    <style>
    .card {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(0,0,0,0.08);
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
        transition: 0.25s ease-in-out;
        background: white;
        margin-bottom: 15px;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 28px rgba(0,0,0,0.12);
    }
    .attack-title {
        font-size: 18px;
        font-weight: 700;
        color: #111;
    }
    .badge {
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    .low { background: #dcfce7; color: #166534; }
    .med { background: #fef9c3; color: #854d0e; }
    .high { background: #ffedd5; color: #9a3412; }
    .crit { background: #fee2e2; color: #991b1b; }

    .brute { border-left: 5px solid #3b82f6; background: linear-gradient(135deg, #eff6ff, #ffffff); }
    .ddos { border-left: 5px solid #8b5cf6; background: linear-gradient(135deg, #f5f3ff, #ffffff); }
    .scan { border-left: 5px solid #10b981; background: linear-gradient(135deg, #ecfdf5, #ffffff); }
    .error { border-left: 5px solid #f59e0b; background: linear-gradient(135deg, #fffbeb, #ffffff); }
    .glow { font-weight: 700; }
    .soc-title { font-size: 26px; font-weight: 800; color: #1e293b; }
    .sub { font-size: 14px; color: #64748b; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)


def attack_style(attack_type: str) -> str:
    return {
        "brute_force": "brute",
        "ddos": "ddos",
        "port_scan": "scan",
        "error_storm": "error"
    }.get(attack_type, "")

def badge(sev: str) -> str:
    sev_upper = str(sev).upper()
    return {
        "LOW": "<span class='badge low'>LOW</span>",
        "MEDIUM": "<span class='badge med'>MEDIUM</span>",
        "HIGH": "<span class='badge high'>HIGH</span>",
        "CRITICAL": "<span class='badge crit'>CRITICAL</span>"
    }.get(sev_upper, f"<span class='badge low'>{sev_upper}</span>")

# =========================
# HEADER CONTROL CONSOLE
# =========================
st.markdown("<div class='soc-title'>🛡️ SOC WAR ROOM — COMMAND CENTER</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Military-grade Threat Simulation Grid — Managed by SentinelAI Background Daemon</div>", unsafe_allow_html=True)
st.markdown("---")

# =========================
# ATTACK SIMULATION GRID (CARDS)
# =========================
st.markdown("### ⚔️ Live Vector Deployment Engine")
col1, col2 = st.columns(2)

def attack_card(title: str, attack_type: str, description: str, col):
    style = attack_style(attack_type)
    with col:
        st.markdown(f"""
        <div class="card {style}">
            <div class="attack-title">{title}</div>
            <p style="color:#555; font-size:13px; margin-top:8px;">{description}</p>
        </div>
        """, unsafe_allow_html=True)

        # Triggering using execution keys inside isolated session bindings
        if st.button(f"DEPLOY {title}", key=f"btn_{attack_type}", use_container_width=True):
            with st.spinner("Injecting malicious payload stream to pipeline logs..."):
                try:
                    # Fires attack via the simulator engine, writing logs directly to attack_stream.log
                    result = st.session_state.attack_engine.launch_attack(attack_type)
                    st.success(f"🚀 {title} payload stream generated! Events injected: {result['events']}. Ready for daemon ingestion collection.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed deploying pipeline matrix exception payload: {str(e)}")

# Left Column Blocks
attack_card(
    "BRUTE FORCE VECTOR",
    "brute_force",
    "Credential stuffing & authentication breach simulation targeting auth layer.",
    col1
)

attack_card(
    "DDoS FLOOD GRID",
    "ddos",
    "High-volume network saturation attack simulation across edge nodes.",
    col1
)

# Right Column Blocks
attack_card(
    "PORT SCAN SWEEP",
    "port_scan",
    "Reconnaissance scan across network ports and exposed services.",
    col2
)

attack_card(
    "ERROR STORM",
    "error_storm",
    "System-level fault injection simulating service failure cascade.",
    col2
)

st.markdown("---")

# =========================
# ACTIVE SIMULATOR STATE
# =========================
st.markdown("### 🧠 Simulated Vectors in Pipeline Log")
state = AttackState.get_state()

if not state:
    st.info("No vectors deployed during this UI run cycle yet.")
else:
    for attack_id, data in list(state.items()):
        # Pull actual baseline severity assigned to the event block instead of randomness
        op_sev = data.get("severity", "LOW")
        st.markdown(f"""
        <div class="card">
            <div class="attack-title glow" style="color: #1e3a8a;">SIMULATOR RUN ID: {attack_id}</div>
            <div style="margin-top: 10px; font-size: 13px; color: #334155;">
                <p style="margin: 3px 0;"><b>TARGET SYSTEM LINK:</b> {data['type'].upper()}</p>
                <p style="margin: 3px 0;"><b>STREAM FILE STATUS:</b> <span style="color:#16a34a; font-weight:bold;">WRITTEN</span></p>
                <p style="margin: 3px 0;"><b>LOG EVENTS POOLED:</b> {data['events_generated']}</p>
            </div>
            <p style="margin-top:10px;">{badge(op_sev)}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# LIVE BACKGROUND STATUS
# =========================
st.markdown("### 📡 Daemon Processing Monitor State")
st.markdown(f"""
<div class="card" style="border-left: 5px solid #4f46e5;">
    <h4 class="glow" style="margin:0; color:#1e293b;">SENTINELAI DAEMON LISTENER IS PASSIVE</h4>
    <p style="margin: 8px 0 4px 0; font-size:13px;">The background script automatically handles polling, normalization via MCP tools, anomaly scoring, and target intelligence reporting independently.</p>
    <p style="margin: 4px 0; font-size:12px; color:#64748b;">Current Active UI Render Timestamp (UTC): {datetime.utcnow().isoformat()}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
### 🧬 SOC Pipeline Topology
`Streamlit UI` ➔ `Injected Attack Logs` ➔ `SplunkDaemon (MCP Tool Belt Integration)` ➔ `Anomaly Engine Series` ➔ `Intelligence Analyzer`
""")
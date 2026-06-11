import streamlit as st
import random
from datetime import datetime

from src.simulator.engine import AttackEngine
from src.simulator.state import AttackState
import main

st.set_page_config(page_title="SOC War Room", layout="wide")

engine = AttackEngine()

# =========================
# SOC STYLE HEADER
# =========================
st.markdown("""
<style>
    .soc-header {
        background: #0B0F19;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #1F2937;
        color: #E5E7EB;
        font-size: 22px;
        font-weight: 600;
        letter-spacing: 1px;
    }

    .sub {
        color: #9CA3AF;
        font-size: 13px;
    }

    .attack-card {
        background: #0F172A;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #1F2937;
        transition: 0.2s;
        cursor: pointer;
    }

    .attack-card:hover {
        border: 1px solid #38BDF8;
        transform: scale(1.02);
    }

    .badge {
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        background: #1F2937;
        color: #93C5FD;
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="soc-header">🛡️ SOC WAR ROOM — ACTIVE DEFENSE CONTROL CENTER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Minimalist command interface for simulated threat execution & monitoring</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# ATTACK CONTROL PANEL (CARDS)
# =========================

attack_catalog = [
    ("Brute Force Intrusion", "brute_force", "AUTH VECTOR"),
    ("DDoS Flood Simulation", "ddos", "NETWORK VECTOR"),
    ("Port Scan Recon", "port_scan", "NETWORK SURVEY"),
    ("Error Storm Injection", "error_storm", "SYSTEM FAULT")
]

cols = st.columns(2)

def launch_attack(label, attack_type):

    result = engine.launch_attack(attack_type)
    severity = random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])

    main.save_simulated_attack({
        "source": "SOC_SIM",
        "attack_type": attack_type,
        "severity": severity,
        "data_points": result["events"],
        "created_at": str(datetime.utcnow())
    })

    st.toast(f"🚨 {label} executed | {severity}", icon="⚠️")


for i, (label, attack_type, tag) in enumerate(attack_catalog):

    with cols[i % 2]:

        st.markdown(f"""
        <div class="attack-card">
            <div style="display:flex; justify-content:space-between;">
                <h4 style="margin:0; color:#E5E7EB;">{label}</h4>
                <span class="badge">{tag}</span>
            </div>

            <p style="color:#9CA3AF; font-size:13px; margin-top:8px;">
                Click to simulate controlled security breach scenario
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"DEPLOY {label}", key=attack_type):
            launch_attack(label, attack_type)

st.markdown("---")

# =========================
# ACTIVE ATTACK REGISTRY
# =========================

st.markdown("### 📡 Active SOC Threat Registry")

state = AttackState.get_state()

if not state:
    st.info("No active threats detected in current simulation window.")
else:
    for attack_id, data in state.items():

        status_color = "🟢" if data["status"] == "RUNNING" else "🔴"

        st.markdown(f"""
        <div style="
            background:#0B0F19;
            padding:12px;
            border-radius:10px;
            border:1px solid #1F2937;
            margin-bottom:10px;
        ">
            <h4 style="color:#E5E7EB;">{status_color} Attack ID: {attack_id}</h4>
            <p style="color:#9CA3AF;">Type: {data['type']}</p>
            <p style="color:#9CA3AF;">Status: {data['status']}</p>
            <p style="color:#9CA3AF;">Events: {data['events_generated']}</p>
        </div>
        """, unsafe_allow_html=True)

# =========================
# LIVE FEED (SIMULATION STYLE)
# =========================

sev = random.choice(["LOW","MEDIUM","HIGH","CRITICAL"])

st.markdown(f"""
### 📡 Live Telemetry Feed
- Severity: **{sev}**
- Status: Streaming secure SOC pipeline
- Timestamp: {datetime.utcnow().isoformat()}
""")
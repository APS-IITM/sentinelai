import streamlit as st
import random
from datetime import datetime

from src.simulator.engine import AttackEngine
from src.simulator.state import AttackState
from src.storage.supabase_loader import save_anomaly

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="SOC War Room", layout="wide")

st.markdown("""
    <style>

    .card {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(0,0,0,0.08);
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
        transition: 0.25s ease-in-out;
        background: white;
    }

    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 28px rgba(0,0,0,0.12);
    }

    /* TITLES */
    .attack-title {
        font-size: 18px;
        font-weight: 700;
        color: #111;
    }

    /* BADGES */
    .badge {
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
    }

    .low { background: #dcfce7; color: #166534; }
    .med { background: #fef9c3; color: #854d0e; }
    .high { background: #ffedd5; color: #9a3412; }
    .crit { background: #fee2e2; color: #991b1b; }

    /* ATTACK TYPE SKINS */
    .brute {
        border-left: 5px solid #3b82f6;
        background: linear-gradient(135deg, #eff6ff, #ffffff);
    }

    .ddos {
        border-left: 5px solid #8b5cf6;
        background: linear-gradient(135deg, #f5f3ff, #ffffff);
    }

    .scan {
        border-left: 5px solid #10b981;
        background: linear-gradient(135deg, #ecfdf5, #ffffff);
    }

    .error {
        border-left: 5px solid #f59e0b;
        background: linear-gradient(135deg, #fffbeb, #ffffff);
    }

    .glow {
        font-weight: 700;
    }

    </style>
    """, unsafe_allow_html=True)

def attack_style(attack_type):
    return {
        "brute_force": "brute",
        "ddos": "ddos",
        "port_scan": "scan",
        "error_storm": "error"
    }.get(attack_type, "")
# =========================
# HEADER
# =========================
st.markdown("<div class='soc-title'>🛡️ SOC WAR ROOM — COMMAND CENTER</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Military-grade Threat Simulation & Active Incident Control Grid</div>", unsafe_allow_html=True)

st.markdown("---")

engine = AttackEngine()

# =========================
# UTIL
# =========================
def random_severity():
    return random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])

def badge(sev):
    return {
        "LOW": "<span class='badge low'>LOW</span>",
        "MEDIUM": "<span class='badge med'>MEDIUM</span>",
        "HIGH": "<span class='badge high'>HIGH</span>",
        "CRITICAL": "<span class='badge crit'>CRITICAL</span>"
    }.get(sev, "")

# =========================
# ATTACK GRID (CARDS)
# =========================
st.markdown("### ⚔️ Attack Simulation Grid")

col1, col2 = st.columns(2)

def attack_card(title, attack_type, description, col):

    style = attack_style(attack_type)

    with col:
        st.markdown(f"""
        <div class="card {style}">
            <div class="attack-title">{title}</div>
            <p style="color:#555; font-size:13px;">
                {description}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"DEPLOY {title}", key=attack_type):
            with st.spinner("Deploying threat vector..."):
                result = engine.launch_attack(attack_type)
                sev = random_severity()

                save_anomaly({
                    "source": "SOC_SIM",
                    "attack_type": attack_type,
                    "severity": sev,
                    "data_points": result["events"],
                    "created_at": str(datetime.now())
                })

                st.success(f"{title} → {result['events']} events | {sev}")

# LEFT COLUMN
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

# RIGHT COLUMN
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
# ACTIVE OPERATIONS PANEL
# =========================
st.markdown("### 🧠 Active Operations Grid")

state = AttackState.get_state()

if not state:
    st.info("No active threat operations detected in SOC grid.")
else:
    for attack_id, data in state.items():

        sev = random_severity()

        st.markdown(f"""
        <div class="card">
            <div class="attack-title glow">OPERATION ID: {attack_id}</div>

            <p><b>TYPE:</b> {data['type']}</p>
            <p><b>STATUS:</b> {data['status']}</p>
            <p><b>EVENTS GENERATED:</b> {data['events_generated']}</p>

            <p>{badge(sev)}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# LIVE TACTICAL FEED
# =========================
st.markdown("### 📡 Live Tactical SOC Feed")

sev = random_severity()

st.markdown(f"""
<div class="card">
    <h4 class="glow">REAL-TIME SIGNAL INTAKE</h4>
    <p>Severity Level: {badge(sev)}</p>
    <p>Timestamp: {datetime.now()}</p>
    <p>Status: Continuous threat monitoring active across all nodes...</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
### 🧬 SOC Pipeline
Attack Simulator → MCP Layer → Splunk → Anomaly Engine → Intelligence Engine → AI Forensics
""")
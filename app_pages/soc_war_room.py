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
body {
    background-color: #0b0f19;
}

.soc-title {
    font-size: 28px;
    font-weight: 700;
    color: #ff3b3b;
    letter-spacing: 1px;
}

.sub {
    color: #aaa;
    font-size: 13px;
}

.card {
    background: linear-gradient(145deg, #111827, #0f172a);
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #1f2937;
    box-shadow: 0 0 15px rgba(255, 0, 0, 0.05);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.02);
    border: 1px solid #ff3b3b;
}

.attack-title {
    font-size: 18px;
    font-weight: 600;
    color: white;
}

.badge {
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 12px;
    display: inline-block;
}

.low { background: #16a34a; color: white; }
.med { background: #eab308; color: black; }
.high { background: #f97316; color: white; }
.crit { background: #dc2626; color: white; }

.glow {
    color: #ff3b3b;
    text-shadow: 0 0 10px rgba(255,0,0,0.6);
}
</style>
""", unsafe_allow_html=True)

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
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="attack-title">{title}</div>
            <p style="color:#9ca3af; font-size:13px;">
                {description}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"DEPLOY {title}", key=attack_type):
            with st.spinner("Deploying simulated threat vector..."):
                result = engine.launch_attack(attack_type)
                sev = random_severity()

                save_anomaly({
                    "source": "SOC_SIM",
                    "attack_type": attack_type,
                    "severity": sev,
                    "data_points": result["events"],
                    "created_at": str(datetime.now())
                })

                st.success(f"VECTOR DEPLOYED → {result['events']} events | {sev}")

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
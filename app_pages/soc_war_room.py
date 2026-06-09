import streamlit as st
import time
from datetime import datetime

from src.simulator.engine import AttackEngine
from src.streaming.refresh_manager import start_streaming
from src.streaming.event_bus import EventBus
from app_pages.ui_components.supabase_loader import save_anomaly

# =========================
# PAGE CONFIG
# =========================
st.title("🟥 PRO SOC WAR ROOM")
st.caption("Real-Time Cyber Defense Command Center | Attack Simulation + Intelligence Fusion")
st.markdown("---")

engine = AttackEngine()


# =========================
# START SOC STREAM (AUTO PIPELINE)
# =========================
if "stream_started" not in st.session_state:
    st.session_state.stream_started = False


# =========================
# ATTACK CONTROL MATRIX (PRO CARDS)
# =========================
st.markdown("### ⚔️ Attack Control Matrix")

def attack_card(title, desc, color, attack_type):

    st.markdown(f"""
    <div class="card" style="border-left:4px solid {color};">
        <h3>{title}</h3>
        <p style="color:#666;">{desc}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"Execute {title}", key=attack_type):

        with st.spinner("Launching simulated attack..."):

            result = engine.launch_attack(attack_type)

            # Save anomaly for dashboard + intelligence
            save_anomaly({
                "source": "SOC_SIM",
                "attack_type": attack_type,
                "severity": "HIGH",
                "data_points": result["events"],
                "created_at": str(datetime.now())
            })

            st.success(f"{title} completed → {result['events']} events generated")


col1, col2 = st.columns(2)

with col1:
    attack_card("Brute Force Attack", "Credential guessing simulation", "#D4AF37", "brute_force")

with col2:
    attack_card("Port Scan Attack", "Network reconnaissance simulation", "#444444", "port_scan")

col3, col4 = st.columns(2)

with col3:
    attack_card("DDoS Attack", "Traffic flood simulation", "#AA820A", "ddos")

with col4:
    attack_card("Error Storm", "System failure simulation", "#777777", "error_storm")


st.markdown("---")


# =========================
# SOC STREAM CONTROL PANEL (PRO)
# =========================
st.markdown("### 📡 SOC Live Stream Engine")

colA, colB = st.columns(2)

with colA:
    if st.button("▶ Start SOC Stream Engine"):
        start_streaming()
        st.session_state.stream_started = True
        st.success("Live SOC streaming activated")

with colB:
    if st.button("⛔ Reset Event Stream"):
        EventBus.clear()
        st.warning("Event stream cleared")


st.markdown("---")


# =========================
# LIVE SOC EVENT FEED (CORE FEATURE)
# =========================
st.markdown("### 🔴 Live SOC Event Feed")

events = EventBus.get_latest(20)

if not events:

    st.info("No live events. Start SOC Stream Engine or launch an attack.")

else:

    for e in reversed(events):

        if e["type"] == "ANOMALY":

            st.error(f"""
            🚨 ANOMALY DETECTED  
            Payload: {e['payload']}  
            """)

        elif e["type"] == "ERROR":

            st.warning(f"""
            ⚠️ SYSTEM ERROR  
            {e['payload']}
            """)

        else:

            st.success("✅ Normal traffic observed")


st.markdown("---")


# =========================
# INCIDENT TIMELINE VIEW (SOC STYLE)
# =========================
st.markdown("### ⏱️ Incident Timeline")

if events:

    for i, e in enumerate(events[-10:]):

        st.markdown(f"""
        <div class="card">
            <h4>Event #{i+1}</h4>
            <p><b>Type:</b> {e['type']}</p>
            <p><b>Time:</b> {datetime.fromtimestamp(e['timestamp']) if 'timestamp' in e else 'LIVE'}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("Timeline will populate when events are generated")


# =========================
# SOC PIPELINE VISUAL (PRO CONTEXT)
# =========================
st.markdown("---")

st.markdown("### 🧠 SOC Intelligence Pipeline")

st.markdown("""
<div class="card">

<b>Attack Lifecycle:</b><br>
🟥 Attack Simulator → 🟧 MCP Tools → 🟨 Splunk Query Layer → 🟩 Anomaly Detection → 🟦 Intelligence Engine → 🤖 AI Analysis

<hr>

<b>Live Mode:</b> Streaming Security Operations Center<br>
<b>Detection Type:</b> Behavioral + Statistical + ML Hybrid<br>
<b>Purpose:</b> Cyber attack simulation + SOC training environment

</div>
""", unsafe_allow_html=True)


# =========================
# OPTIONAL AUTO REFRESH (SAFE VERSION)
# =========================
time.sleep(2)
st.rerun()
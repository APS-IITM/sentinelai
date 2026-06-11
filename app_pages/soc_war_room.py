import streamlit as st
import time
import random
from datetime import datetime

from src.simulator.engine import AttackEngine
from src.simulator.state import AttackState
from src.storage.supabase_loader import save_anomaly


st.title("🟥 SOC WAR ROOM")
st.caption("Live Attack Simulation + Real-Time Threat Command Center")
st.markdown("---")

engine = AttackEngine()

def random_severity():
    return random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])

def severity_color(sev):
    return {
        "LOW": "🟢",
        "MEDIUM": "🟡",
        "HIGH": "🟠",
        "CRITICAL": "🔴"
    }.get(sev, "⚪")

st.subheader("⚔️ Attack Execution Panel")
col1, col2 = st.columns(2)

def launch_attack_ui(title, attack_type):
    if st.button(f"Launch {title}"):
        with st.spinner("Executing attack simulation..."):
            result = engine.launch_attack(attack_type)
            severity = random_severity()

            save_anomaly({
                "source": "SOC_SIM",
                "attack_type": attack_type,
                "severity": severity,
                "data_points": result["events"],
                "created_at": str(datetime.now())
            })

            st.success(f"{title} → {result['events']} events | Severity: {severity}")

with col1:
    launch_attack_ui("Brute Force", "brute_force")
    launch_attack_ui("DDoS Flood", "ddos")

with col2:
    launch_attack_ui("Port Scan", "port_scan")
    launch_attack_ui("Error Storm", "error_storm")

st.markdown("---")

st.subheader("🧠 Active Attack Registry")
state = AttackState.get_state()

if not state:
    st.info("No active attacks currently running.")
else:
    for attack_id, data in state.items():
        status = data["status"]
        icon = "🟢" if status == "running" else "🔴"

        st.markdown(f"""
        <div class="card">
            <h4>{icon} Attack ID: {attack_id}</h4>
            <p><b>Type:</b> {data['type']}</p>
            <p><b>Status:</b> {status}</p>
            <p><b>Events Generated:</b> {data['events_generated']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# FIXED: Static telemetry snapshot rendering removes UI thread blocking issues
st.subheader("📡 Live SOC Feed Snapshot")
sev = random_severity()
st.markdown(f"""
### {severity_color(sev)} Event Stream Update
- Severity: {sev}
- Timestamp: {datetime.now()}
- Status: Active telemetry capture pipeline synchronized...
""")

st.markdown("---")
st.markdown("""
### 🧬 SOC Pipeline Flow
Attack Simulator → MCP Tools → Splunk → Anomaly Engine → Intelligence Engine → AI Layer
""")
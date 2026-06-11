import streamlit as st
import random
from datetime import datetime

from src.simulator.engine import AttackEngine
from src.simulator.state import AttackState
import main

st.title("🟥 SOC WAR ROOM")
st.markdown("---")

engine = AttackEngine()

def launch(name, attack_type):
    if st.button(name):
        result = engine.launch_attack(attack_type)
        severity = random.choice(["LOW","MEDIUM","HIGH","CRITICAL"])

        main.save_simulated_attack({
            "source": "SOC_SIM",
            "attack_type": attack_type,
            "severity": severity,
            "data_points": result["events"],
            "created_at": str(datetime.now())
        })

        st.success(f"{name} executed")

st.button("Brute Force") and launch("Brute Force", "brute_force")
st.button("DDoS") and launch("DDoS", "ddos")
st.button("Port Scan") and launch("Port Scan", "port_scan")

state = AttackState.get_state()

st.markdown("### Active Attacks")

for k,v in state.items():
    st.write(k, v)
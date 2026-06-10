import sys
import subprocess
import os
import streamlit as st

from app_pages.ui_components.theme import apply_theme
from app_pages.splash import show_splash


# =====================================================
# 🚀 AUTOMATED DECOUPLED BACKEND ENGINE STARTUP
# =====================================================
@st.cache_resource
def start_background_soc_daemon():
    """
    Spawns the Splunk monitoring daemon as an independent background process.
    @st.cache_resource guarantees this function executes EXACTLY ONCE on server boot.
    """
    # Locate the correct script path dynamically regardless of execution environment
    base_dir = os.path.dirname(os.path.abspath(__file__))
    daemon_script = os.path.join(base_dir, "src", "anomaly", "splunk_daemon.py")

    if not os.path.exists(daemon_script):
        st.error(f"❌ Initialization Error: Background daemon script not found at {daemon_script}")
        return False

    try:
        # Spin up the daemon script in a separate OS process context
        # env=os.environ passes your loaded system variables and .env tokens through
        process = subprocess.Popen(
            [sys.executable, daemon_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=os.environ
        )
        
        # Log to the terminal hosting your Streamlit instance
        print(f"🔥 [SentinelAI SOC Bootstrap] Automatically launched Splunk Daemon (PID: {process.pid})")
        return True
        
    except Exception as e:
        print(f"💥 [SentinelAI SOC Bootstrap] Failed to auto-start background engine: {str(e)}")
        return False


# Trigger the background daemon before rendering the application views
daemon_is_live = start_background_soc_daemon()

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="SentinelAI SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()


# =====================================================
# SPLASH CONTROL (FIXED: NO RERUN CRASH)
# =====================================================
if "splash_done" not in st.session_state:
    show_splash()
    st.session_state.splash_done = True


# =====================================================
# MAIN SOC NAVIGATION SYSTEM
# =====================================================
pages = {
    "🛡️ SOC Command Center": [
        st.Page("app_pages/dashboard.py", title="SOC Home"),
    ],
    "📊 Monitoring": [
        st.Page("app_pages/threat_monitor.py", title="Threat Monitor"),
    ],
    "🟥 War Room": [
        st.Page("app_pages/soc_war_room.py", title="Attack Simulator"),
    ],
    "🧠 Intelligence": [
        st.Page("app_pages/intelligence_center.py", title="CTI Engine"),
        st.Page("app_pages/ai_reports.py", title="AI Reports"),
    ],
    "🧰 Forensics": [
        st.Page("app_pages/investigation.py", title="Investigation Console"),
    ],
    "⚙️ Settings": [
        st.Page("app_pages/settings.py", title="System Config"),
    ],
}


# =====================================================
# SOC NAVIGATION RENDER
# =====================================================
nav = st.navigation(pages)
nav.run()
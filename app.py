import streamlit as st
import threading

from src.devops.data_sync_manager import DataSyncManager

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="SentinelAI - Incident Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# BACKGROUND DATA SYNC STARTER
# ==============================

def start_data_sync():
    manager = DataSyncManager(
        repo_path=".",        # root of repo
        interval_minutes=3    # 2–4 min safe batch window
    )
    manager.start()


# 🔥 RUN ONLY ONCE PER SESSION
if "sync_started" not in st.session_state:
    threading.Thread(
        target=start_data_sync,
        daemon=True
    ).start()

    st.session_state.sync_started = True


# ==============================
# GLOBAL UI THEME
# ==============================
st.markdown("""
<style>
.stApp { background-color: #FAFAFA; color: #1C1C1C; }

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #EAEAEA;
    padding: 16px 22px;
    border-radius: 6px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.015);
}

.stDataFrame {
    background-color: #FFFFFF !important;
    border-radius: 6px;
}

h1, h2, h3 {
    font-family: Inter, sans-serif;
    font-weight: 500;
}

.stButton>button {
    background-color: #FFFFFF;
    color: #1C1C1C;
    border: 1px solid #D4AF37;
}
.stButton>button:hover {
    background-color: #D4AF37;
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE (DATA ONLY)
# ==============================
if "active_threat_profiles" not in st.session_state:
    st.session_state.active_threat_profiles = []

if "compiled_cti_report" not in st.session_state:
    st.session_state.compiled_cti_report = None


# ==============================
# NAVIGATION (CLEAN)
# ==============================
pages = {
    "📊 Monitoring": [
        st.Page("app/dashboard.py", title="Dashboard"),
        st.Page("app/threat_monitor.py", title="Threat Monitor"),
    ],
    "🧠 Intelligence": [
        st.Page("app/intelligence_center.py", title="CTI Engine"),
        st.Page("app/ai_reports.py", title="AI Reports"),
    ],
    "🧰 Forensics": [
        st.Page("app/investigation.py", title="Investigation Console"),
        st.Page("app/settings.py", title="Settings"),
    ]
}

nav = st.navigation(pages)
nav.run()
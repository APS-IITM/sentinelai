import streamlit as st

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
        st.Page("app/pages/dashboard.py", title="Dashboard"),
        st.Page("app/pages/threat_monitor.py", title="Threat Monitor"),
    ],
    "🧠 Intelligence": [
        st.Page("app/pages/intelligence_center.py", title="CTI Engine"),
        st.Page("app/pages/ai_reports.py", title="AI Reports"),
    ],
    "🧰 Forensics": [
        st.Page("app/pages/investigation.py", title="Investigation Console"),
        st.Page("app/pages/settings.py", title="Settings"),
    ]
}

nav = st.navigation(pages)
nav.run()
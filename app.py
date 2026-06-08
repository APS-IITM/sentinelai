import streamlit as st
import numpy as np

# 1. Mandatory Streamlit Configuration Page Setup
st.set_page_config(
    page_title="SentinelAI - Incident Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injecting Minimalistic Luxury Style Layers (Light Minimal Theme)
st.markdown("""
    <style>
    .stApp { background-color: #FAFAFA; color: #1C1C1C; }
    
    /* Premium Border Accent Shadow Box */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #EAEAEA;
        padding: 16px 22px;
        border-radius: 6px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.015);
    }
    
    /* Clean custom styling for tables and data containers */
    .stDataFrame, div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border-radius: 6px;
    }
    
    /* Text Custom Overrides */
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 500 !important; color: #111111; }
    
    /* Elegant Button Accent Rules */
    .stButton>button {
        background-color: #FFFFFF;
        color: #1C1C1C;
        border: 1px solid #D4AF37 !important;
        padding: 6px 16px;
        transition: all 0.25s ease;
    }
    .stButton>button:hover {
        background-color: #D4AF37 !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Cache the Fallback Log Vectors Inside Session State (Simulating live data arrays)
if "login_series" not in st.session_state:
    st.session_state.login_series = [12, 14, 15, 11, 13, 12, 14, 16, 12, 15, 11, 14, 280]
    st.session_state.error_series = [2, 1, 3, 2, 4, 1, 2, 3, 1, 2, 4, 3, 195]
    st.session_state.network_series = [45, 52, 48, 50, 47, 53, 49, 51, 46, 50, 52, 48, 1420]
    st.session_state.active_threats_cache = []
    st.session_state.compiled_cti_report = None

# 4. Declare Clean Native Multi-Page Layout Routing Properties
pages = {
    "Monitoring & Telemetry": [
        st.Page("app/dashboard.py", title="Dashboard Overview", icon="✨"),
        st.Page("app/threat_monitor.py", title="Threat Monitor Feed", icon="🔍"),
        st.Page("app/intelligence_center.py", title="Intelligence Center", icon="🧭"),
    ],
    "Forensics & Query Hub": [
        st.Page("app/ai_reports.py", title="AI Incident Reports", icon="🧠"),
        st.Page("app/investigation.py", title="Interactive Investigation", icon="🧰"),
        st.Page("app/settings.py", title="System Settings", icon="⚙️"),
    ]
}

pg = st.navigation(pages)
pg.run()
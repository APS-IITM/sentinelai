from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

# =====================================================
# SPLUNK CONFIG 
# =====================================================

try:
    import streamlit as st

    SPLUNK_HOST = st.secrets["splunk"].get(
        "host",
        os.getenv("SPLUNK_HOST", "localhost")
    )

    SPLUNK_PORT = int(
        st.secrets["splunk"].get(
            "port",
            os.getenv("SPLUNK_PORT", 8089)
        )
    )

    SPLUNK_USERNAME = st.secrets["splunk"].get(
        "username",
        os.getenv("SPLUNK_USERNAME")
    )

    SPLUNK_PASSWORD = st.secrets["splunk"].get(
        "password",
        os.getenv("SPLUNK_PASSWORD")
    )

    SPLUNK_WEB_PORT = int(
        st.secrets["splunk"].get(
            "web_port",
            os.getenv("SPLUNK_WEB_PORT", 8000)
        )
    )

    SPLUNK_HEC_PORT = int(
        st.secrets["splunk"].get(
            "hec_port",
            os.getenv("SPLUNK_HEC_PORT", 8088)
        )
    )

except Exception:

    SPLUNK_HOST = os.getenv(
        "SPLUNK_HOST",
        "localhost"
    )

    SPLUNK_PORT = int(
        os.getenv(
            "SPLUNK_PORT",
            8089
        )
    )

    SPLUNK_USERNAME = os.getenv(
        "SPLUNK_USERNAME"
    )

    SPLUNK_PASSWORD = os.getenv(
        "SPLUNK_PASSWORD"
    )

    SPLUNK_WEB_PORT = int(
        os.getenv(
            "SPLUNK_WEB_PORT",
            8000
        )
    )

    SPLUNK_HEC_PORT = int(
        os.getenv(
            "SPLUNK_HEC_PORT",
            8088
        )
    )

# =====================================================
# MCP STORAGE CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "mcp_storage"
DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# RUNTIME MCP CACHE
# =====================================================

MCP_DATA_STORE = {
    "search_results": [],
    "alerts": [],
    "incidents": [],
    "investigations": [],
    "intel_results": [],
    "risk_events": [],
    "audit_logs": []
}

# =====================================================
# VALIDATION
# =====================================================

def validate_config():
    required = {
        "SPLUNK_HOST": SPLUNK_HOST,
        "SPLUNK_USERNAME": SPLUNK_USERNAME,
        "SPLUNK_PASSWORD": SPLUNK_PASSWORD,
    }

    missing = [
        key
        for key, value in required.items()
        if not value
    ]

    if missing:
        raise ValueError(
            f"Missing Splunk configuration: "
            f"{', '.join(missing)}"
        )

    return True
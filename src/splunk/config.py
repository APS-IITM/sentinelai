from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

# =====================================================
# Splunk Configuration
# =====================================================

SPLUNK_HOST = os.getenv("SPLUNK_HOST")
SPLUNK_PORT = int(os.getenv("SPLUNK_PORT", 8089))
SPLUNK_USERNAME = os.getenv("SPLUNK_USERNAME")
SPLUNK_PASSWORD = os.getenv("SPLUNK_PASSWORD")

# =====================================================
# MCP Storage Configuration
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "mcp_storage"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Runtime MCP Cache
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
# Validation
# =====================================================

def validate_config():
    required = {
        "SPLUNK_HOST": SPLUNK_HOST,
        "SPLUNK_USERNAME": SPLUNK_USERNAME,
        "SPLUNK_PASSWORD": SPLUNK_PASSWORD,
    }

    missing = [
        key for key, value in required.items()
        if not value
    ]

    if missing:
        raise ValueError(
            f"Missing environment variables: {', '.join(missing)}"
        )

    return True
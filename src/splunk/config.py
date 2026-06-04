from dotenv import load_dotenv
import os

load_dotenv()

SPLUNK_HOST = os.getenv("SPLUNK_HOST")
SPLUNK_PORT =int(os.getenv("SPLUNK_PORT",8089))
SPLUNK_USERNAME =os.getenv("SPLUNK_USERNAME")
SPLUNK_PASSWORD =os.getenv("SPLUNK_PASSWORD")

def validate_config():
    required ={
        "SPLUN_HOST":SPLUNK_HOST,
        "SPLUNK_USERNAME": SPLUNK_USERNAME,
        "SPLUNK_PASSWORD": SPLUNK_PASSWORD,
    }

    missing=[
        key for key, value in required.items()
        if not value
    ]

    if missing:
        raise ValueError(
            f"Missing variables: {', '.join(missing)}"
        )
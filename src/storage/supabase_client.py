import os

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

try:
    import streamlit as st

    SUPABASE_URL = st.secrets["supabase"].get(
        "url",
        os.getenv("SUPABASE_URL")
    )

    SUPABASE_KEY = st.secrets["supabase"].get(
        "key",
        os.getenv("SUPABASE_KEY")
    )

    SUPABASE_DATABASE_PASSWORD = st.secrets["supabase"].get(
        "database_password",
        os.getenv("SUPABASE_DATABASE_PASSWORD")
    )

except Exception:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_DATABASE_PASSWORD = os.getenv(
        "SUPABASE_DATABASE_PASSWORD"
    )

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL missing")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY missing")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
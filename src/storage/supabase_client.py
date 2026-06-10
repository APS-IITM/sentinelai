import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

try:
    import streamlit as st

    # Safely look at st.secrets["supabase"], falling back to os.getenv if missing
    supabase_secrets = st.secrets.get("supabase", {})
    
    SUPABASE_URL = supabase_secrets.get("url") or os.getenv("SUPABASE_URL")
    SUPABASE_KEY = supabase_secrets.get("key") or os.getenv("SUPABASE_KEY")
    SUPABASE_DATABASE_PASSWORD = supabase_secrets.get("database_password") or os.getenv("SUPABASE_DATABASE_PASSWORD")

except Exception:
    # Fallback entirely to environment variables if streamlit isn't running
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_DATABASE_PASSWORD = os.getenv("SUPABASE_DATABASE_PASSWORD")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL missing from both Streamlit secrets and environment variables.")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY missing from both Streamlit secrets and environment variables.")

# This is the client that other files will import
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
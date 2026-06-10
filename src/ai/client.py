import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

try:
    import streamlit as st

    GOOGLE_API_KEY = st.secrets["google"].get(
        "api_key",
        os.getenv("GOOGLE_API_KEY")
    )

    GEMINI_MODEL = st.secrets["google"].get(
        "gemini_model",
        os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    )

except Exception:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(GEMINI_MODEL)
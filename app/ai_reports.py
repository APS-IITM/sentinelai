import streamlit as st
from src.ai.analyzer import AIAnalyzer

st.title("🧠 AI Incident Reports")

if st.button("Generate AI Report from Stored Data"):

    ai = AIAnalyzer()
    report = ai.generate_report("all")

    st.markdown("### SOC Report")
    st.write(report.generated_report)
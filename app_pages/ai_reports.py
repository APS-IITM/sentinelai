import streamlit as st
import main

st.title("🧠 AI Reports")

reports = main.get_all_ai_reports()

if not reports:
    st.info("No reports")
    st.stop()

options = {
    f"{r.get('source_type')} #{r.get('id')}": r
    for r in reports
}

choice = st.selectbox("Select", list(options.keys()))

selected = options[choice]

st.markdown(f"""
<div class="card">
    <h3>{choice}</h3>
    <p>{selected.get('generated_report')}</p>
</div>
""", unsafe_allow_html=True)

st.download_button(
    "Download",
    selected.get("generated_report", ""),
    file_name="ai_report.txt"
)
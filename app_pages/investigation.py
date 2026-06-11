#investigation.py
import streamlit as st
import pandas as pd
from src.storage.supabase_loader import get_mcp

st.title("🧰 Investigation Console")
st.caption("Examine localized subsets across microservice configuration tables")
st.markdown("---")

tool = st.selectbox("Select Target Dataset Layer", ["auth", "network", "system", "security"])

if st.button("Query Selected Dataset Cluster"):
    with st.spinner(f"Extracting tracking matrix for {tool}..."):
        data = get_mcp(tool)
        
        if data:
            df = pd.DataFrame(data)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info(f"Zero structured forensic telemetry entries are categorized matching the target flag: '{tool}'")
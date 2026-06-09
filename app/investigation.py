import streamlit as st
import pandas as pd
from src.storage.mcp_store import MCPStore

st.title("🧰 Investigation Console")

tool = st.selectbox("Select Dataset", ["auth", "network", "system", "security"])

data = MCPStore.get(tool)

if data:
    st.dataframe(pd.DataFrame(data))
else:
    st.info("No data available for selected source.")
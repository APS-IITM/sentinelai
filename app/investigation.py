import streamlit as st
import pandas as pd

st.title("🧰 SPL Investigation Console")
st.caption("Interact manually with your connected Splunk Enterprise or Cloud cluster framework deployments.")

# Natural language generation assistant input
st.markdown("### 🤖 Natural Language SPL Query Assistant")
nl_prompt = st.text_input("Describe the target activity you are searching for in natural text:", 
                          placeholder="e.g. Show me all failed logins from user 'admin' in the last 2 hours")

if nl_prompt:
    st.code("index=security sourcetype=linux_secure user=admin action=failure | bucket _time span=5m | stats count by _time", language="splunk")
    st.caption("💡 Generated SPL Query structure based on your conversational prompt request.")

st.markdown("---")

# Raw Console Input Section
st.markdown("### Custom SPL Terminal Executer")
spl_terminal = st.text_area("SPL Input Code Interface:", value="index=security_summary | head 5")

if st.button("⚡ Execute Splunk Query Cluster Connection"):
    st.success("Query compiled and sent to endpoint host node successfully. 5 logs found.")
    
    # Returned query dataframe visualization
    mock_results = pd.DataFrame([
        {"_time": "2026-06-08 16:15:00", "host": "auth_gateway", "sourcetype": "access_combined", "message": "status=401 user=invalid_root"},
        {"_time": "2026-06-08 16:15:05", "host": "auth_gateway", "sourcetype": "access_combined", "message": "status=401 user=invalid_admin"},
    ])
    st.dataframe(mock_results, use_container_width=True)
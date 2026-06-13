import streamlit as st
import pandas as pd
import requests
import urllib.parse
import main

st.set_page_config(page_title="Tactical Threat Monitor", layout="wide")
st.title("🔍 Tactical Threat Monitor")
st.markdown("---")

data = main.get_all_anomalies()

if not data:
    st.warning("No anomaly data found.")
    st.stop()

df = pd.DataFrame(data)

# ================================================================
# TABLE — click a row to select it
# ================================================================
st.markdown("### 📋 Live Threat Table")
st.caption("Click any row to select it, then choose an action below.")

event = st.dataframe(
    df,
    use_container_width=True,
    on_select="rerun",
    selection_mode="single-row",
    hide_index=True,
)

selected_rows = event.selection.rows

# ================================================================
# ACTION PANEL — shown only when a row is selected
# ================================================================
if not selected_rows:
    st.info("👆 Click any row in the table above to get started.")
    st.stop()

row = df.iloc[selected_rows[0]].to_dict()
attack_type = row.get("attack_type", "Unknown")
severity    = row.get("severity", "?")
source      = row.get("source", "?")

st.markdown("---")

# Selected row summary badge
badge_color = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(
    str(severity).upper(), "⚪"
)
st.markdown(
    f"**Selected:** {badge_color} `{attack_type}` &nbsp;|&nbsp; "
    f"Severity: `{severity}` &nbsp;|&nbsp; Source: `{source}`"
)

# Action buttons side by side
col_a, col_b, _ = st.columns([1, 1, 4])
do_report = col_a.button("🧠 Generate AI Report", use_container_width=True)
do_search = col_b.button("🌐 Search Google",       use_container_width=True)

# ================================================================
# RESULT PANEL
# ================================================================
st.markdown("### 📄 Results")
result_area = st.container()

# ── AI REPORT ───────────────────────────────────────────────────
if do_report:
    class Wrap:
        def __init__(self, r):
            self.source      = r.get("source")
            self.attack_type = r.get("attack_type")
            self.severity    = r.get("severity")
            self.description = r.get("description", "")
            self.data_points = r.get("data_points", 0)

    with result_area:
        with st.spinner("Generating AI threat report..."):
            result = main.generate_ai_report(Wrap(row))
        st.success("AI Report ready")
        st.markdown(result)

# ── GOOGLE SEARCH ────────────────────────────────────────────────
elif do_search:
    query       = f"{attack_type} attack type cybersecurity {severity} severity"
    encoded     = urllib.parse.quote_plus(query)
    search_url  = f"https://www.google.com/search?q={encoded}"

    # Use DuckDuckGo Instant Answer API (no key needed, JSON friendly)
    ddg_url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_redirect=1&no_html=1&skip_disambig=1"

    with result_area:
        with st.spinner("Fetching search results..."):
            try:
                resp = requests.get(ddg_url, timeout=6)
                resp.raise_for_status()
                ddg  = resp.json()
            except Exception as e:
                ddg  = {}
                st.warning(f"Could not fetch live results ({e}). Showing link only.")

        st.success(f"Search results for: **{query}**")

        # Abstract / summary
        abstract = ddg.get("AbstractText", "").strip()
        if abstract:
            st.markdown(f"**📖 Overview**\n\n{abstract}")
            abstract_src = ddg.get("AbstractSource", "")
            abstract_url = ddg.get("AbstractURL", "")
            if abstract_url:
                st.markdown(f"*Source: [{abstract_src}]({abstract_url})*")
            st.markdown("---")

        # Related topics
        topics = ddg.get("RelatedTopics", [])
        shown  = 0
        if topics:
            st.markdown("**🔗 Related Topics**")
            for t in topics:
                if shown >= 6:
                    break
                text = t.get("Text", "").strip()
                url  = t.get("FirstURL", "")
                if text and url:
                    st.markdown(f"- [{text}]({url})")
                    shown += 1

        if not abstract and not shown:
            st.info("No instant-answer data found. Open the full Google search below.")

        # Always show the Google link as fallback
        st.markdown(f"🔍 [Open full Google search ↗]({search_url})")

else:
    with result_area:
        st.info("Choose an action above — **Generate AI Report** or **Search Google**.")
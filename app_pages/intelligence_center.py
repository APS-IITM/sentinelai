import streamlit as st
import pandas as pd
from datetime import datetime
from app_pages.ui_components.supabase_loader import get_intel_reports

st.title("🧭 Intelligence Center")
st.caption("Correlate active threat profiles using pre-evaluated data streams")
st.markdown("---")

# Load baseline records
raw_reports = get_intel_reports()

if not raw_reports:
    st.info("No validated structural threat intelligence documents found in database records.")
    st.stop()

# Convert to DataFrame to enable fast, intuitive lookups and transformations
intel_df = pd.DataFrame(raw_reports)

# Ensure essential fallback schema structures exist
if "incident_type" not in intel_df.columns:
    intel_df["incident_type"] = "Unclassified"
if "severity" not in intel_df.columns:
    intel_df["severity"] = "UNKNOWN"
if "created_at" not in intel_df.columns:
    intel_df["created_at"] = datetime.utcnow()
else:
    intel_df["created_at"] = pd.to_datetime(intel_df["created_at"], errors="coerce")


# ==========================================
# 🎛️ DRILL-DOWN FILTERS CORE MATRIX
# ==========================================
st.subheader("🔍 Threat Intelligence Query Filters")

col_type, col_sev, col_date = st.columns(3)

with col_type:
    type_options = ["ALL"] + sorted(list(intel_df["incident_type"].unique()))
    selected_type = st.selectbox("Filter by Incident Type", type_options)

with col_sev:
    sev_options = ["ALL"] + sorted(list(intel_df["severity"].unique()))
    selected_sev = st.selectbox("Filter by Severity Vector", sev_options)

with col_date:
    # Extract date limits or default safely to today if parsing fails
    min_date = intel_df["created_at"].min().date() if not intel_df["created_at"].isna().all() else datetime.today().date()
    max_date = intel_df["created_at"].max().date() if not intel_df["created_at"].isna().all() else datetime.today().date()
    
    if min_date == max_date:
        # Simple insurance to ensure valid streamlit date slider boundaries
        date_range = st.date_input("Filter by Date Range", [min_date])
    else:
        date_range = st.date_input("Filter by Date Range", [min_date, max_date])


# Apply evaluation logic sequentially
filtered_df = intel_df.copy()

if selected_type != "ALL":
    filtered_df = filtered_df[filtered_df["incident_type"] == selected_type]

if selected_sev != "ALL":
    filtered_df = filtered_df[filtered_df["severity"] == selected_sev]

if len(date_range) == 2:
    start_dt, end_dt = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = filtered_df[(filtered_df["created_at"] >= start_dt) & (filtered_df["created_at"] <= end_dt)]

st.markdown("---")


# ==========================================
# 📄 PAGINATION ENGINE (MAX 5 ENTRIES / PAGE)
# ==========================================
records_to_render = filtered_df.to_dict(orient="records")
total_records = len(records_to_render)

if total_records == 0:
    st.warning("Zero indicators of compromise match the requested target filter properties.")
else:
    ITEMS_PER_PAGE = 5
    
    # Calculate operational ceiling limits 
    max_pages = max(1, ((total_records - 1) // ITEMS_PER_PAGE) + 1)
    
    # Render pagination control buttons inside footer/header tracking bar
    pag_col1, pag_col2 = st.columns([1, 4])
    with pag_col1:
        current_page = st.number_input(f"Page (1-{max_pages})", min_value=1, max_value=max_pages, value=1, step=1)
    with pag_col2:
        st.markdown(f"<p style='margin-top:32px; color:#666;'>Showing <b>{min((current_page-1)*ITEMS_PER_PAGE + 1, total_records)} - {min(current_page*ITEMS_PER_PAGE, total_records)}</b> out of <b>{total_records}</b> filtered threat records.</p>", unsafe_allow_html=True)

    # Slice dataset partition cleanly
    start_idx = (current_page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_slice = records_to_render[start_idx:end_idx]

    # Render data cards securely
    for report in page_slice:
        st.markdown(f"""
        <div class="card" style="margin-bottom: 16px;">
            <h3 style="margin-top:0; color:#111;">Type: {report.get('incident_type', 'Unclassified')}</h3>
            <p style="color:#666; margin-bottom: 4px;"><b>Severity Vector:</b> <span style="color:#D4AF37; font-weight:600;">{report.get('severity', 'UNKNOWN')}</span></p>
            <p style="color:#999; font-size:12px; margin-bottom: 12px;"><b>Ingestion Timestamp:</b> {str(report.get('created_at'))}</p>
            <div style="background:#FDFDFD; padding:12px; border-left:3px solid #D4AF37; border-radius:4px; line-height:1.5;">
                {report.get('attack_story', 'No story parameters written.')}
            </div>
        </div>
        """, unsafe_allow_html=True)
# hushh_mcp/agents/job_copilot/ui/app_tracker.py

import streamlit as st
import pandas as pd
import os

LOG_PATH = "vault/logs/applications.csv"

st.set_page_config(page_title="📋 Job Application Tracker", layout="centered")
st.title("📋 Job Application Tracker")

if not os.path.exists(LOG_PATH):
    st.warning("No applications found yet.")
else:
    df = pd.read_csv(LOG_PATH)

    st.subheader("🔍 Filter Applications")
    email_filter = st.text_input("Filter by Recruiter Email")
    status_filter = st.selectbox("Filter by Status", ["", "✅ Sent and Follow-up Scheduled", "📅 Interview", "❌ Rejected"])

    # Filter dataframe
    filtered_df = df.copy()
    if email_filter:
        filtered_df = filtered_df[filtered_df["Email"].str.contains(email_filter, case=False)]
    if status_filter:
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    st.subheader("🛠 Update Application Status")
    for i, row in filtered_df.iterrows():
        st.markdown(f"**Company:** {row['Company']} | **Email:** {row['Email']}")
        new_status = st.selectbox(
            f"Update status for {row['Company']} ({i})",
            ["✅ Sent and Follow-up Scheduled", "📅 Interview", "❌ Rejected"],
            index=["✅ Sent and Follow-up Scheduled", "📅 Interview", "❌ Rejected"].index(row["Status"]),
            key=f"status_{i}"
        )
        if new_status != row["Status"]:
            df.at[i, "Status"] = new_status

    if st.button("💾 Save Changes"):
        df.to_csv(LOG_PATH, index=False)
        st.success("✅ Status updates saved!")

    st.subheader("📊 All Applications")
    st.dataframe(df, use_container_width=True)

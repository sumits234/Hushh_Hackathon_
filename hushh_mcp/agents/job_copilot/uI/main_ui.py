import streamlit as st
from flows import start_job_application_flow
import os

st.set_page_config(page_title="🎯 AI Job Application Agent")
st.title("🤖 AI Job Application Agent")
st.write("Upload your resume and job description, and let the AI handle the rest!")

# === Recruiter Email ===
recruiter_email = st.text_input("Recruiter Email", placeholder="e.g., hr@openai.com")

# === Resume Upload ===
resume_file = st.file_uploader("📄 Upload Your Resume (TXT)", type="txt")

# === Job Description Upload ===
jd_file = st.file_uploader("💼 Upload Job Description (TXT)", type="txt")

# === Submit ===
if st.button("🚀 Apply Now"):
    if not recruiter_email or not resume_file or not jd_file:
        st.warning("⚠️ Please upload all files and provide recruiter email.")
    else:
        with st.spinner("Running your AI agent..."):

            # Save uploaded resume
            resume_path = "vault/resumes/uploaded_resume.txt"
            with open(resume_path, "wb") as f:
                f.write(resume_file.read())

            # Save uploaded JD
            jd_path = "vault/jds/uploaded_jd.txt"
            with open(jd_path, "wb") as f:
                f.write(jd_file.read())

            # Call job flow using uploaded files
            start_job_application_flow(
                to_email=recruiter_email,
                resume_file="uploaded_resume.txt",
                jd_file="uploaded_jd.txt"
            )

        st.success("✅ Done! Application email sent and calendar scheduled.")
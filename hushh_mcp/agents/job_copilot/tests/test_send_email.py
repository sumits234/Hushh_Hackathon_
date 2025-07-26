import os
from dotenv import load_dotenv
from hushh_mcp.agents.job_copilot.services.emailer import send_email

load_dotenv()

if __name__ == "__main__":
    send_email(
        to_address=os.getenv("LINKEDIN_USERNAME"),  # Use your email or replace directly
        subject="Test Email from Job Copilot",
        body="Hello! This is a test email from my AI agent.",
        attachments=[]
    )

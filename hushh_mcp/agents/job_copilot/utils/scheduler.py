from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from services.emailer import send_email_with_gmail  # import your Gmail function

scheduler = BackgroundScheduler()

def schedule_follow_up(to_email, resume_path, cover_letter_path):
    followup_time = datetime.now() + timedelta(days=3)

    def followup_task():
        subject = "Follow-up on Job Application"
        body = f"""
        Dear Hiring Manager,

        I wanted to follow up regarding the application I sent a few days ago. 
        I’m excited about the opportunity and would love to discuss it further.

        Best regards,  
        Sumit Adikari
        """
        send_email_with_gmail(to_email, subject, body, resume_path, cover_letter_path)

    scheduler.add_job(followup_task, 'date', run_date=followup_time)
    scheduler.start()
    print(f"✅ Follow-up scheduled for {followup_time}")

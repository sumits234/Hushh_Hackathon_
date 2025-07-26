import sys
import os
import datetime

# ✅ Add job_copilot directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
job_copilot_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, job_copilot_dir)

# ✅ Add project root to sys.path so 'services' is found
root_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
sys.path.insert(0, root_dir)

# ✅ Import your calendar function
from services.calendar import add_interview_event

if __name__ == "__main__":
    # ✅ Set a test date and time
    interview_datetime = datetime.datetime.now() + datetime.timedelta(minutes=5)

    # ✅ Call the function
    add_interview_event(
        start_datetime=interview_datetime,
        duration_minutes=30,
        summary="🎯 Test Interview - Sumit AI Agent"
    )

    print("📅 Test calendar event created successfully!")

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import pickle
import datetime 

def add_interview_event(start_datetime, duration_minutes, summary="Interview"):
    try:
        token_path = os.getenv("GOOGLE_CALENDAR_TOKEN", "google_creds/token.pickle")

        if not os.path.exists(token_path):
            print("❌ Token file not found. Run generate_calendar_token.py first.")
            return

        with open(token_path, "rb") as token_file:
            creds = pickle.load(token_file)

        service = build('calendar', 'v3', credentials=creds)

        end_datetime = start_datetime + datetime.timedelta(minutes=duration_minutes)

        event = {
            'summary': summary,
            'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'Asia/Kolkata'},
        }

        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print("📅 Event created:", event_result.get('htmlLink'))

    except Exception as e:
        print("❌ Error scheduling calendar event:", str(e))

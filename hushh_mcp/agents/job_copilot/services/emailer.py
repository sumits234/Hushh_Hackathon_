import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None
    if os.path.exists('google_creds/token.json'):
        creds = Credentials.from_authorized_user_file('google_creds/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('google_creds/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('google_creds/token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def send_email_with_gmail(to_email, subject, body_text, resume_path, cover_letter_path):
    service = gmail_authenticate()
    
    msg = EmailMessage()
    msg['To'] = to_email
    msg['From'] = "me"
    msg['Subject'] = subject
    msg.set_content(body_text)

    # Attach resume
    with open(resume_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename='Resume.pdf')

    # Attach cover letter
    with open(cover_letter_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename='CoverLetter.pdf')

    encoded_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    create_message = {'raw': encoded_msg}

    send_message = service.users().messages().send(userId="me", body=create_message).execute()
    print(f"✅ Email sent to {to_email}. Message ID: {send_message['id']}")

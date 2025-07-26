import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    load_dotenv()  # <-- Add this line
    creds_path = os.getenv("GMAIL_API_CREDENTIALS")
    if not creds_path:
        raise ValueError("GMAIL_API_CREDENTIALS not set in environment variables.")
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=0)
    token_path = os.path.join(os.path.dirname(creds_path), "token.pickle")
    with open(token_path, "wb") as token_file:
        pickle.dump(creds, token_file)
    print("✅ Gmail token saved to", token_path)

if __name__ == "__main__":
    main()

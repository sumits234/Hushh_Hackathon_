import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds_path = os.getenv("GOOGLE_CALENDAR_CRED")
    if not creds_path:
        raise ValueError("GOOGLE_CALENDAR_CRED not set in .env file")

    # OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=0)

    # Save token
    token_path = os.path.join(os.path.dirname(creds_path), "token.pickle")
    with open(token_path, "wb") as token_file:
        pickle.dump(creds, token_file)

    print(f"✅ Calendar token saved to {token_path}")

if __name__ == "__main__":
    main()

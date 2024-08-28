import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the scopes to include both Gmail and Google Sheets access
SCOPES = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/spreadsheets'
]

def gmail_authenticate():
    creds = None
    # Check if token.pickle exists to load credentials
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds

def build_gmail_service(creds):
    return build('gmail', 'v1', credentials=creds)

def build_sheets_service(creds):
    return build('sheets', 'v4', credentials=creds)

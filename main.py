from auth import gmail_authenticate, build_gmail_service, build_sheets_service
from search import search_messages
from write import write_to_google_sheets

from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SEARCH_REGEX = os.getenv("SEARCH_REGEX")
DAYS_TO_SEARCH = int(os.getenv("DAYS_TO_SEARCH"))
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
DATA_RANGE = os.getenv("DATA_RANGE")

###################

creds = gmail_authenticate()
gmail_service = build_gmail_service(creds)

sheets_service = build_sheets_service(creds)

# Calculate the date 30 days ago
date_30_days_ago = (datetime.now() - timedelta(days=DAYS_TO_SEARCH)).strftime('%Y/%m/%d')
query = "subject:Purchase" + f' after:{date_30_days_ago}'

data = search_messages(gmail_service, query, SEARCH_REGEX)
write_to_google_sheets(sheets_service, SPREADSHEET_ID, DATA_RANGE, data)

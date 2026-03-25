#!/usr/bin/env python3
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta
from pathlib import Path

CRED_DIR = Path('/home/rwhitaker/.openclaw/workspace/skills/google-calendar/config')
TOKEN_FILE = CRED_DIR / 'token.json'

creds = Credentials.from_authorized_user_file(TOKEN_FILE)
if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())

service = build('calendar', 'v3', credentials=creds)

# Get events for today from United calendar
now = datetime.now(timezone.utc)
start_of_day = (now.replace(hour=0, minute=0, second=0, microsecond=0))
end_of_day = start_of_day + timedelta(days=1)

events_result = service.events().list(
    calendarId='teq6qq3e0q1l0nr1leu7kkr78ppju73t@import.calendar.google.com',
    timeMin=start_of_day.isoformat(),
    timeMax=end_of_day.isoformat(),
    singleEvents=True,
    orderBy='startTime',
    maxResults=50
).execute()

events = events_result.get('items', [])
print(f'United Calendar ({len(events)} events):')
for event in events:
    summary = event.get('summary', 'No title')
    start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', 'No time'))
    print(f'  - {summary}')
    print(f'    Time: {start}')
    print()

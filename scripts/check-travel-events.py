#!/usr/bin/env python3
"""Check for travel events on all calendars."""

import sys
sys.path.insert(0, '/home/rwhitaker/.openclaw/workspace/skills/google-calendar')

from pathlib import Path
from datetime import datetime, timezone, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Credential paths
WORK_CRED_DIR = Path('/home/rwhitaker/.openclaw/workspace/skills/google-calendar/config')
WORK_TOKEN = WORK_CRED_DIR / 'token.json'

# All calendars now read from DCG work account (shared calendars)
CALENDARS = [
    ('DCG', 'primary', WORK_TOKEN),
    ('United', 'teq6qq3e0q1l0nr1leu7kkr78ppju73t@import.calendar.google.com', WORK_TOKEN),
]

def get_credentials(token_file):
    """Load credentials from token file. Returns None on any error."""
    if token_file.exists():
        try:
            creds = Credentials.from_authorized_user_file(token_file)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return creds
        except Exception:
            return None
    return None

def parse_time(time_str):
    """Parse time string to datetime."""
    if 'T' in time_str:
        try:
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            return dt.astimezone()
        except:
            return None
    else:
        try:
            dt = datetime.fromisoformat(time_str)
            dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except:
            return None

def get_travel_events(days_ahead=7):
    """Get travel events from all calendars for the next week."""
    all_events = []

    # Travel keywords
    travel_keywords = ['travel', 'trip', 'flight', 'airport', 'fly', 'flying',
                    'vacation', 'holiday', 'departure', 'arrival',
                    'hotel', 'airbnb', 'air bnb', 'air b&b']

    for cal_name, cal_id, token_file in CALENDARS:
        creds = get_credentials(token_file)
        if not creds:
            continue

        try:
            service = build('calendar', 'v3', credentials=creds)

            # Get events for next 7 days
            time_min = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            time_max = (datetime.now(timezone.utc) + timedelta(days=days_ahead)).strftime('%Y-%m-%dT%H:%M:%SZ')

            events_result = service.events().list(
                calendarId=cal_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime',
                maxResults=100
            ).execute()

            events = events_result.get('items', [])

            for event in events:
                summary = event.get('summary', 'No title').lower()

                # Check if event has travel keywords
                if any(keyword in summary for keyword in travel_keywords):
                    start = event.get('start', {})
                    end = event.get('end', {})

                    if 'dateTime' in start:
                        start_dt = parse_time(start['dateTime'])
                    elif 'date' in start:
                        start_dt = parse_time(start['date'])
                    else:
                        continue

                    if 'dateTime' in end:
                        end_dt = parse_time(end['dateTime'])
                    elif 'date' in end:
                        end_dt = parse_time(end['date'])
                    else:
                        continue

                    if start_dt and end_dt:
                        all_events.append({
                            'calendar': cal_name,
                            'summary': event.get('summary', 'No title'),
                            'start': start_dt,
                            'end': end_dt
                        })

        except Exception as e:
            print(f"Error fetching {cal_name} calendar: {e}", file=sys.stderr)

    all_events.sort(key=lambda x: x['start'])
    return all_events

def display_travel_events(events):
    """Display travel events."""
    if not events:
        return False

    print("✈️  Travel Events (Next 7 Days)")
    print()

    for event in events:
        start = event['start']
        summary = event['summary']
        cal_name = event['calendar']

        if start.hour == 0 and start.minute == 0:
            date_str = start.strftime('%a, %b %d')
            print(f"   {date_str}")
            print(f"      {summary}")
        else:
            datetime_str = start.strftime('%a, %b %d @ %-I:%M %p')
            print(f"   {datetime_str}")
            print(f"      {summary}")

        print(f"      [{cal_name}]")
        print()

    return True

if __name__ == '__main__':
    events = get_travel_events()

    if events:
        display_travel_events(events)
    else:
        # No output means no travel events found
        pass

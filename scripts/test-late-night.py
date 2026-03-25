#!/usr/bin/env python3
"""Test script to verify late-night event detection works."""

import sys
import subprocess
from datetime import datetime, timezone, timedelta

sys.path.insert(0, '/home/rwhitaker/.openclaw/workspace/skills/google-calendar')

from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

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

def get_credentials(token_file):
    """Load credentials from token file."""
    if token_file.exists():
        try:
            creds = Credentials.from_authorized_user_file(token_file)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return creds
        except Exception:
            return None
    return None

def should_filter_event(summary):
    """Check if event should be filtered out."""
    if not summary:
        return False
    summary_lower = summary.lower()
    if 'cancelled' in summary_lower or 'canceled' in summary_lower:
        return True
    return False

def matches_keywords(summary):
    """Check if event summary contains any watched keywords."""
    if not summary:
        return False
    keywords = ["outage", "maintenance", "change", "help hub", "production", "deploy", "release", "upgrade"]
    summary_lower = summary.lower()
    for keyword in keywords:
        if keyword.lower() in summary_lower:
            return True
    return False

def main():
    now = datetime.now(timezone.utc)
    date = now.strftime('%Y-%m-%d')

    cal_id = 'teq6qq3e0q1l0nr1leu7kkr78ppju73t@import.calendar.google.com'
    token_file = Path('/home/rwhitaker/.openclaw/workspace/skills/google-calendar/config/token.json')

    creds = get_credentials(token_file)
    if not creds:
        print("❌ Could not load credentials")
        return

    try:
        service = build('calendar', 'v3', credentials=creds)

        time_min = f"{date}T00:00:00Z"
        time_max = f"{date}T23:59:59Z"

        events_result = service.events().list(
            calendarId=cal_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime',
            maxResults=100
        ).execute()

        events = events_result.get('items', [])

        print(f"📅 Checking United calendar for late-night events: {date}")
        print()

        found_any = False

        for event in events:
            summary = event.get('summary', 'No title')

            if should_filter_event(summary):
                continue

            if not matches_keywords(summary):
                continue

            start = event.get('start', {})

            if 'dateTime' in start:
                start_dt = parse_time(start['dateTime'])
            else:
                continue

            if not start_dt:
                continue

            local_start = start_dt.astimezone()

            # Check if event starts after 9 PM
            if local_start.hour >= 21:
                if not found_any:
                    print("🚨 **Late-night work events found:** 🚨\n")
                    found_any = True

                time_str = local_start.strftime('%-I:%M %p')
                print(f"⏰ {time_str} — {summary}")

        if not found_any:
            print("✅ No late-night work events found today")
        else:
            print()
            print("These events would trigger a Discord alert 1 hour before they start.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()

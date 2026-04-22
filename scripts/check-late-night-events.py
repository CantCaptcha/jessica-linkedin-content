#!/home/rwhitaker/.openclaw/workspace/skills/google-calendar/venv/bin/python3
"""
Check for upcoming late-night work events and send Discord alerts."""

import sys
import subprocess
import json
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, '/home/rwhitaker/.openclaw/workspace/skills/google-calendar')

from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
DISCORD_CHANNEL = "discord:1488952869603377243"  # #Richard channel
LATE_NIGHT_HOUR = 21  # Events after 9 PM (local time)
DEFAULT_ALERT_HOURS_BEFORE = 2  # Default alert 2 hours before

# Keywords to watch for
KEYWORDS = [
    "outage", "maintenance", "change", "help hub",
    "production", "deploy", "release", "upgrade"
]

# Heartbeat state tracking
HEARTBEAT_STATE_FILE = Path.home() / '.openclaw' / 'workspace' / 'state' / 'heartbeat-state.json'

def load_heartbeat_state():
    """Load last heartbeat state from disk."""
    if HEARTBEAT_STATE_FILE.exists():
        try:
            with open(HEARTBEAT_STATE_FILE, 'r') as f:
                return json.load(f)
        except:
                return {}
    return {}

def save_heartbeat_state(state):
    """Save heartbeat state to disk."""
    HEARTBEAT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HEARTBEAT_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

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

def should_filter_event(summary):
    """Check if event should be filtered out."""
    if not summary:
        return False

    summary_lower = summary.lower()

    # Filter out cancelled events
    if 'cancelled' in summary_lower or 'canceled' in summary_lower:
        return True

    # Filter out personal events
    personal_keywords = [
        'doctor', 'dentist', 'medical', 'appointment',
        'personal', 'pharmacy', 'prescription', 'therapy',
        'physical therapy', 'chiropractor', 'optometrist',
        'eye doctor', 'dermatologist', 'specialist'
    ]

    for keyword in personal_keywords:
        if keyword in summary_lower:
            return True

    return False

def should_filter_united_event(summary):
    """Check if United calendar event should be filtered out."""
    if not summary:
        return False

    summary_lower = summary.lower()

    if 'office hours' in summary_lower:
        return True

    united_personal_keywords = [
        'doctor', 'dentist', 'medical', 'appointment',
        'pharmacy', 'prescription', 'therapy', 'chiropractor',
        'optometrist', 'eye doctor', 'dermatologist', 'specialist',
        'hair', 'nail', 'massage', 'spa', 'salon',
        'gym', 'fitness', 'yoga', 'pilates',
        'school', 'parent-teacher', 'pta', 'school pickup',
        'vet', 'veterinary', 'pet',
        'car service', 'oil change', 'auto repair',
        'real estate', 'inspection', 'contractor',
        'personal', 'lunch', 'break', 'coffee',
        'birthday', 'anniversary', 'holiday',
        'vacation', 'pto', 'day off',
        'follow-up', 'checkup', 'check-up',
    ]

    for keyword in united_personal_keywords:
        if keyword in summary_lower:
            return True

    if ':' in summary:
        parts = summary.split(':', 1)
        if len(parts) == 2:
            after_colon = parts[1].strip().lower()
            for keyword in united_personal_keywords:
                if keyword in after_colon:
                    return True

    return False

def matches_keywords(summary):
    """Check if event summary contains any watched keywords."""
    if not summary:
        return False

    summary_lower = summary.lower()
    for keyword in KEYWORDS:
        if keyword.lower() in summary_lower:
            return True
    return False

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

def check_late_night_events():
    """
    Check for upcoming late-night work events on United calendar.
    Alerts if current time is within the event's alert window.
    """
    state = load_heartbeat_state()
    last_alerts = state.get('lastAlerts', {})

    now_utc = datetime.now(timezone.utc)

    # Check today, tomorrow, AND day after (to catch UTC day boundary events)
    dates_to_check = [
        now_utc.strftime('%Y-%m-%d'),
        (now_utc + timedelta(days=1)).strftime('%Y-%m-%d'),
        (now_utc + timedelta(days=2)).strftime('%Y-%m-%d')
    ]

    matching_events_for_alert = []
    current_alerts_sent = []

    for date in dates_to_check:
        cal_id = 'teq6qq3e0q1l0nr1leu7kkr78ppju73t@import.calendar.google.com'
        token_file = Path('/home/rwhitaker/.openclaw/workspace/skills/google-calendar/config/token.json')

        creds = get_credentials(token_file)
        if not creds:
            continue

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

            for event in events:
                summary = event.get('summary', 'No Title')

                # Skip filtered events
                if should_filter_event(summary) or should_filter_united_event(summary):
                    continue

                # Must match at least one keyword
                if not matches_keywords(summary):
                    continue

                start = event.get('start', {})
                if 'dateTime' not in start:
                    continue

                start_dt_utc = parse_time(start['dateTime'])
                if not start_dt_utc:
                    continue
                
                local_start = start_dt_utc.astimezone() # Convert to local for LATE_NIGHT_HOUR check

                # Check if event starts after LATE_NIGHT_HOUR (local time) or before 6 AM (local time)
                if local_start.hour >= LATE_NIGHT_HOUR or local_start.hour < 6:
                    # Calculate event-specific alert window
                    alert_start_utc = start_dt_utc - timedelta(hours=DEFAULT_ALERT_HOURS_BEFORE + 0.5) # 2.5 hours before
                    alert_end_utc = start_dt_utc - timedelta(hours=DEFAULT_ALERT_HOURS_BEFORE - 0.5) # 1.5 hours before

                    # Check if current time is within this event's alert window
                    if alert_start_utc <= now_utc <= alert_end_utc:
                        event_key = f"{start_dt_utc.isoformat()}|{summary}"
                        
                        # Only alert if not already sent for this event
                        if event_key not in last_alerts:
                            matching_events_for_alert.append({
                                'summary': summary,
                                'start': start_dt_utc
                            })
                            current_alerts_sent.append(event_key)

        except HttpError as e:
            pass

    # Update state only with current alerts sent in THIS run
    # This ensures that if no alerts are sent, last_alerts is not cleared incorrectly
    state['lastAlerts'] = current_alerts_sent
    state['lastAlertTimestamp'] = datetime.now(timezone.utc).isoformat()
    save_heartbeat_state(state)

    return matching_events_for_alert

def send_discord_alert(event):
    """
    Send Discord alert about upcoming late-night event.
    Includes summary, start time (local), and a call to action.
    """
    start_time = event['start'].astimezone()
    time_str = start_time.strftime('%I:%M %p on %A, %B %-d')

    message = f"🚨 **Upcoming Late-Night Work Event** 🚨\n\n"
    message += f"**{event['summary']}**\n"
    message += f"⏰ Starts: {time_str}\n\n"
    message += f"Just wanted to give you a heads-up! You might want to check if you can help out."

    try:
        result = subprocess.run(
            ['openclaw', 'message', 'send', '--channel', DISCORD_CHANNEL, '--message', message],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"✓ Sent Discord alert for: {event['summary']}")
            return True
        else:
            print(f"❌ Failed to send Discord alert: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error sending Discord alert: {e}")
        return False

def main():
    """Main function - orchestrates checking and alerting."""
    print("Checking for late-night events...")
    events_to_alert = check_late_night_events()

    if events_to_alert:
        print(f"Found {len(events_to_alert)} events to alert.")
        for event in events_to_alert:
            send_discord_alert(event)
    else:
        print("✓ No late-night events found to alert.")

if __name__ == '__main__':
    main()

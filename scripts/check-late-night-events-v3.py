#!/usr/bin/env python3
"""Check for upcoming late-night work events and send Discord alerts."""

import sys
import subprocess
import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, '/home/rwhitaker/.openclaw/workspace/skills/google-calendar')

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
DISCORD_CHANNEL = "discord:1469388540403253260#bot"
LATE_NIGHT_HOUR = 21
ALERT_HOURS_BEFORE = 2

# Keywords to watch for
KEYWORDS = [
    "outage", "maintenance", "change", "help hub",
    "production", "deploy", "release", "upgrade"
]

def parse_time(time_str):
    """Parse time string to datetime."""
    if 'T' in time_str:
        try:
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            return dt.astimezone(timezone.utc)
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
    
    if 'cancelled' in summary_lower or 'canceled' in summary_lower:
        return True
    
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

def check_late_night_events():
    """Check for upcoming late-night work events on United calendar.
    Returns tuple: (matching_events, alert_window_start, alert_window_end)
    """
    now_utc = datetime.now(timezone.utc)
    alert_window_start = now_utc + timedelta(hours=ALERT_HOURS_BEFORE - 0.5)
    alert_window_end = now_utc + timedelta(hours=ALERT_HOURS_BEFORE + 0.5)
    
    dates_to_check = [
        now_utc.strftime('%Y-%m-%d'),
        (now_utc + timedelta(days=1)).strftime('%Y-%m-%d'),
        (now_utc + timedelta(days=2)).strftime('%Y-%m-%d')
    ]
    
    matching_events = []
    
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
            print(f"[DEBUG] Date: {date} - API returned {len(events)} events")
            
            for event in events:
                summary = event.get('summary', 'No title')
                
                if should_filter_event(summary):
                    print(f"[DEBUG]   Filtered out (general): {summary}")
                    continue
                
                if should_filter_united_event(summary):
                    print(f"[DEBUG]   Filtered out (United): {summary}")
                    continue
                
                if not matches_keywords(summary):
                    print(f"[DEBUG]   No keyword match: {summary}")
                    continue
                
                start = event.get('start', {})
                end = event.get('end', {})
                
                if 'dateTime' in start:
                    start_dt = parse_time(start['dateTime'])
                elif 'date' in start:
                    continue
                else:
                    continue
                
                if not start_dt:
                    continue
                
                local_start = start_dt.astimezone(timezone.utc).astimezone()
                
                if local_start.hour >= LATE_NIGHT_HOUR or local_start.hour < 6:
                    if alert_window_start <= start_dt <= alert_window_end:
                        matching_events.append({
                            'summary': summary,
                            'start': start_dt,
                            'end': end.get('dateTime')
                        })
        
        except HttpError as e:
            pass
    
    return (matching_events, alert_window_start, alert_window_end)

def send_discord_alert(event):
    """Send Discord alert about upcoming late-night event."""
    start_time = event['start'].astimezone(timezone.utc).astimezone()
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
        return result.returncode == 0
    except Exception as e:
        return False

def main():
    events, alert_window_start, alert_window_end = check_late_night_events()
    
    now_utc = datetime.now(timezone.utc)
    now_local = now_utc.astimezone(timezone.utc).astimezone()
    
    print(f"[DEBUG] Now (UTC): {now_utc.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[DEBUG] Now (Local): {now_local.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[DEBUG] Alert window (UTC): {alert_window_start.strftime('%Y-%m-%d %H:%M')} to {alert_window_end.strftime('%Y-%m-%d %H:%M')}")
    print(f"[DEBUG] Found {len(events)} matching events")
    
    if events:
        for event in events:
            event_start = event['start'].astimezone(timezone.utc).astimezone()
            event_start_local = event_start.astimezone(timezone.utc).astimezone()
            print(f"[DEBUG] Event: {event['summary']} | UTC: {event['start'].strftime('%Y-%m-%d %H:%M')} | Local: {event_start_local.strftime('%Y-%m-%d %H:%M')}")
            send_discord_alert(event)
    else:
        print("[DEBUG] No late-night events found to alert")

if __name__ == '__main__':
    main()

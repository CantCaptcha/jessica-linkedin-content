#!/usr/bin/env python3
"""Check for new/forwarded messages from Vince or Jessica."""

import sys
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
sys.path.insert(0, '/home/rwhitaker/.openclaw/workspace/skills/gmail')

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Credential paths
GMAIL_DIR = Path('/home/rwhitaker/.openclaw/workspace/skills/gmail')
TOKEN = GMAIL_DIR / 'config/token.json'
STATE_FILE = Path('/home/rwhitaker/.openclaw/workspace/scripts/dcg-email-state.json')

# People to watch for
WATCH_EMAILS = [
    'vincent.scott@cybersecgru.com',
    'jessica.allen@cybersecgru.com'
]

def get_credentials():
    """Load credentials from token file."""
    if TOKEN.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN))
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return creds
        except Exception:
            return None
    return None

def load_state():
    """Load state of already-notified messages."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {'notified_ids': []}

def save_state(state):
    """Save state of already-notified messages."""
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except:
        pass

def is_new_message(subject):
    """Check if this is a new message (not a reply)."""
    subject_lower = subject.lower()

    # Skip if it's a reply
    reply_patterns = ['re:', '回复:', '回复：', '回复']
    for pattern in reply_patterns:
        if subject_lower.startswith(pattern):
            return False

    return True

def is_forwarded_message(subject):
    """Check if this is a forwarded message."""
    subject_lower = subject.lower()

    # Forward patterns
    forward_patterns = ['fwd:', 'fw:', 'forward:']
    for pattern in forward_patterns:
        if pattern in subject_lower:
            return True

    return False

def check_recent_emails():
    """Check for new/forwarded messages from watched people."""
    creds = get_credentials()
    if not creds:
        return []

    try:
        service = build('gmail', 'v1', credentials=creds)

        # Build search query for watched people
        from_query = ' OR '.join([f'from:{email}' for email in WATCH_EMAILS])

        # Get messages from last 2 hours
        time_min = (datetime.now() - timedelta(hours=2)).strftime('%Y/%m/%d')

        results = service.users().messages().list(
            userId='me',
            q=f'{from_query} after:{time_min}',
            maxResults=20
        ).execute()

        messages = results.get('messages', [])
        new_alerts = []

        for msg in messages:
            msg_id = msg['id']

            # Get message details
            msg_data = service.users().messages().get(
                userId='me',
                id=msg_id,
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()

            headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
            subject = headers.get('Subject', 'No Subject')
            from_addr = headers.get('From', '')
            date = headers.get('Date', '')

            # Check if this is from a watched person
            watched_person = None
            for email in WATCH_EMAILS:
                if email.lower() in from_addr.lower():
                    # Extract name from email
                    name = email.split('@')[0].replace('.', ' ').title()
                    watched_person = name
                    break

            if not watched_person:
                continue

            # Check if it's a new message (not a reply)
            if not is_new_message(subject):
                continue

            # Check if it's a forwarded message OR a new message
            is_new = is_new_message(subject)
            is_fwd = is_forwarded_message(subject)

            if not is_new and not is_fwd:
                continue

            # Check if already notified
            state = load_state()
            if msg_id in state['notified_ids']:
                continue

            # This is a message we should alert about
            alert = {
                'id': msg_id,
                'from': watched_person,
                'subject': subject,
                'date': date,
                'type': 'Forwarded' if is_fwd else 'New'
            }
            new_alerts.append(alert)

            # Mark as notified
            state['notified_ids'].append(msg_id)
            save_state(state)

        return new_alerts

    except HttpError as e:
        return []

def send_discord_notification(alerts):
    """Send notification to Discord."""
    if not alerts:
        return

    # Format message
    message_lines = ['📧 **New DCG Emails**\n']
    for alert in alerts:
        emoji = '📤' if alert['type'] == 'Forwarded' else '✉️'
        message_lines.append(f'{emoji} **From {alert["from"]}**: {alert["subject"]}')

    message = '\n'.join(message_lines)

    # Send via message tool to Discord
    try:
        # This will be called from cron, so we use the message tool
        # But since we're in a script, we need to send it differently
        # For now, let's just write to a file that the main session can check
        alert_file = Path('/home/rwhitaker/.openclaw/workspace/scripts/dcg-email-alert.txt')
        with open(alert_file, 'w') as f:
            f.write(message)
    except:
        pass

def main():
    alerts = check_recent_emails()

    if alerts:
        print(f"Found {len(alerts)} new/forwarded message(s) to notify about")
        for alert in alerts:
            print(f"  [{alert['type']}] From {alert['from']}: {alert['subject']}")

        # Send notification
        send_discord_notification(alerts)
    else:
        print("No new/forwarded messages from Vince or Jessica")

if __name__ == '__main__':
    main()

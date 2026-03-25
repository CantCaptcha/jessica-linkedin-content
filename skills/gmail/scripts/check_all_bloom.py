#!/usr/bin/env python3
"""Check all Bloom Growth emails for Richard's action items."""

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from pathlib import Path
import base64
import re
from html import unescape

TOKEN_FILE = Path('config/token.json')
creds = Credentials.from_authorized_user_file(TOKEN_FILE)
service = build('gmail', 'v1', credentials=creds)

# Bloom Growth email IDs (from earlier search)
bloom_emails = [
    ('19cb9cafe78f5195', 'Mar 4, 2026'),
    ('19c71b46d6bf2425', 'Feb 18, 2026'),
    ('19c4da7431753d10', 'Feb 11, 2026'),
    ('19c29979ee74d78a', 'Feb 4, 2026'),
    ('19c0573ea9bc2de7', 'Jan 28, 2026'),
]

def get_body(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            body = get_body(part)
            if body:
                return body
    else:
        if payload.get('body', {}).get('data'):
            data = payload['body']['data']
            return base64.urlsafe_b64decode(data).decode('utf-8')
    return None

print("=== Richard's Bloom Growth Action Items ===\n")

for email_id, date in bloom_emails:
    msg = service.users().messages().get(userId='me', id=email_id, format='full').execute()
    body = get_body(msg['payload'])
    clean_text = unescape(re.sub(r'<[^>]+>', '\n', body))
    lines = [l.strip() for l in clean_text.split('\n') if l.strip()]

    # Find Richard's name and look for the next non-empty line (the action item)
    for i, line in enumerate(lines):
        if line == 'Richard Whitaker' and i + 1 < len(lines):
            # The action item should be the next non-empty line (often starts with •)
            next_line = lines[i+1] if i + 1 < len(lines) else None
            if next_line and len(next_line) > 10:
                # Look for a due date (usually line i+2 or i+3)
                due_date = None
                for j in range(i+2, min(i+5, len(lines))):
                    if re.match(r'\d{1,2}/\d{1,2}/\d{4}', lines[j]):
                        due_date = lines[j]
                        break

                print(f"📋 {date}")
                print(f"   {next_line}")
                if due_date:
                    print(f"   Due: {due_date}")
                else:
                    # Check if the next line after the action item might be a date
                    if i + 2 < len(lines) and len(lines[i+2]) < 20:
                        print(f"   Due: {lines[i+2]}")
                print()
                break

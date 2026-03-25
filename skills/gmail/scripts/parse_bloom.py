#!/usr/bin/env python3
"""Parse Bloom Growth email for action items."""

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from pathlib import Path
import base64
import re
from html import unescape

TOKEN_FILE = Path('config/token.json')
creds = Credentials.from_authorized_user_file(TOKEN_FILE)
service = build('gmail', 'v1', credentials=creds)

# Get the most recent Bloom Growth email
msg = service.users().messages().get(userId='me', id='19cb9cafe78f5195', format='full').execute()

# Extract body recursively
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

body = get_body(msg['payload'])

# Clean HTML and look for content
clean_text = re.sub(r'<[^>]+>', '\n', body)
clean_text = unescape(clean_text)

# Find section mentioning Richard or action items
lines = clean_text.split('\n')

# Print TO-DOS section
print('=== TO-DOS Section (lines 630-700) ===')
for i in range(630, 700):
    line = lines[i].strip()
    if line:
        print(line)

print('\n=== Around second Richard mention (lines 900-950) ===')
for i in range(900, 950):
    line = lines[i].strip()
    if line:
        print(line)

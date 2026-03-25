#!/usr/bin/env python3
"""Generate OAuth URL for manual authorization."""

from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import json

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar.freebusy',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

CRED_DIR = Path(__file__).parent.parent / 'config'
CREDENTIALS_FILE = CRED_DIR / 'credentials.json'

flow = InstalledAppFlow.from_client_secrets_file(
    str(CREDENTIALS_FILE),
    SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)

authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='consent'
)

print("=" * 80)
print("OAuth Authorization URL for Personal Gmail (richwhit@gmail.com)")
print("=" * 80)
print()
print("1. Visit this URL in your browser:")
print()
print(authorization_url)
print()
print("2. Sign in to your richwhit@gmail.com account")
print("3. Grant permission for Calendar and Gmail access")
print("4. Copy the authorization code that Google shows you")
print()
print("5. Run this command to complete the setup:")
print()
print("   cd /home/rwhitaker/.openclaw/workspace/skills/gmail-personal")
print("   venv/bin/python3 scripts/finish_auth.py YOUR_AUTH_CODE")
print()
print("=" * 80)

#!/usr/bin/env python3
"""
Simple OAuth authentication script for Google Calendar.
Run this to authenticate and create token.json
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from pathlib import Path

SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/calendar.events',
          'https://www.googleapis.com/auth/calendar.freebusy']

CRED_DIR = Path(__file__).parent.parent / 'config'
CREDENTIALS_FILE = CRED_DIR / 'credentials.json'
TOKEN_FILE = CRED_DIR / 'token.json'

print("=" * 60)
print("Google Calendar Authentication")
print("=" * 60)
print()
print("This will open a browser window for you to authorize.")
print()

if not CREDENTIALS_FILE.exists():
    print(f"Error: {CREDENTIALS_FILE} not found!")
    print("Please place credentials.json in the config directory.")
    exit(1)

try:
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
    creds = flow.run_local_server(port=0)

    with open(TOKEN_FILE, 'w') as f:
        creds.to_json(f)

    print()
    print("=" * 60)
    print("✓ Authentication successful!")
    print("=" * 60)
    print(f"Credentials saved to: {TOKEN_FILE}")

except Exception as e:
    print()
    print("=" * 60)
    print("✗ Authentication failed")
    print("=" * 60)
    print(f"Error: {e}")
    exit(1)

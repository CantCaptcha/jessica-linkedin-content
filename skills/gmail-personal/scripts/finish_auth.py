#!/usr/bin/env python3
"""Exchange authorization code for fresh tokens."""

import sys
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta, timezone

CRED_FILE = Path(__file__).parent.parent / 'config' / 'credentials.json'
TOKEN_FILE = Path(__file__).parent.parent / 'config' / 'token.json'

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar.freebusy',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

# Get auth code from command line
if len(sys.argv) < 2:
    print("Usage: python3 finish_auth.py <authorization_code>")
    sys.exit(1)

auth_code = sys.argv[1].strip()

# Load credentials
with open(CRED_FILE, 'r') as f:
    cred_data = json.load(f)

client_id = cred_data['installed']['client_id']
client_secret = cred_data['installed']['client_secret']

# Exchange auth code for tokens
data = {
    'code': auth_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
    'grant_type': 'authorization_code'
}

print("Exchanging authorization code for tokens...")
response = requests.post('https://oauth2.googleapis.com/token', data=data)

if response.status_code == 200:
    tokens = response.json()

    # Save token file
    token_data = {
        'token': tokens['access_token'],
        'refresh_token': tokens['refresh_token'],
        'token_uri': 'https://oauth2.googleapis.com/token',
        'client_id': client_id,
        'client_secret': client_secret,
        'scopes': SCOPES,
        'expiry': (datetime.now(timezone.utc) + timedelta(seconds=tokens['expires_in'])).isoformat()
    }

    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)

    print()
    print("=" * 80)
    print("✓ Authentication successful!")
    print("=" * 80)
    print(f"✓ Access token valid for {tokens['expires_in']} seconds")
    print(f"✓ Refresh token: {tokens['refresh_token'][:20]}...")
    print(f"✓ Saved to: {TOKEN_FILE}")
    print()
    print("You can now run JOB REJECT checks!")
    print("=" * 80)
else:
    print()
    print("=" * 80)
    print("✗ Failed to exchange auth code")
    print("=" * 80)
    print(f"Status: {response.status_code}")
    print(f"Error: {response.text}")
    print()
    print("Common issues:")
    print("- Authorization code expired (they expire quickly)")
    print("- Already used this code (each code can only be used once)")
    print("- Wrong redirect URI in OAuth consent screen")
    print("=" * 80)
    sys.exit(1)

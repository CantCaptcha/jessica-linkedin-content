#!/usr/bin/env python3
"""Exchange authorization code for fresh tokens."""

import json
import requests
from pathlib import Path

CRED_FILE = Path(__file__).parent / 'config' / 'credentials.json'
TOKEN_FILE = Path(__file__).parent / 'config' / 'token.json'

# Load credentials
with open(CRED_FILE, 'r') as f:
    cred_data = json.load(f)

client_id = cred_data['installed']['client_id']
client_secret = cred_data['installed']['client_secret']
redirect_uri = cred_data['installed']['redirect_uris'][0]

# The auth code from the user
auth_code = "4/0AfrIepDPGKyLGxhTwxkhsAactZHalC1UHU670bAHPwGWSqftVeh99p8sSLfuYOP-ZSrCaA"

# Exchange auth code for tokens
data = {
    'code': auth_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code'
}

response = requests.post('https://oauth2.googleapis.com/token', data=data)

if response.status_code == 200:
    tokens = response.json()

    # Save token file
    from datetime import datetime, timedelta, timezone
    token_data = {
        'token': tokens['access_token'],
        'refresh_token': tokens['refresh_token'],
        'token_uri': 'https://oauth2.googleapis.com/token',
        'client_id': client_id,
        'client_secret': client_secret,
        'scopes': cred_data['installed'].get('scopes', []),
        'expiry': (datetime.now(timezone.utc) + timedelta(seconds=tokens['expires_in'])).isoformat()
    }

    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)

    print("✓ Successfully obtained new tokens!")
    print(f"✓ Access token valid for {tokens['expires_in']} seconds")
    print(f"✓ Refresh token: {tokens['refresh_token'][:20]}...")
    print(f"✓ Saved to: {TOKEN_FILE}")
else:
    print(f"✗ Failed to exchange auth code: {response.text}")

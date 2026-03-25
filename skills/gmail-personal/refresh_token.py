#!/usr/bin/env python3
"""Manually refresh the Gmail token."""

import json
import requests
from pathlib import Path

TOKEN_FILE = Path(__file__).parent / 'config' / 'token.json'

# Load current token
with open(TOKEN_FILE, 'r') as f:
    token_data = json.load(f)

# Use refresh token to get new access token
data = {
    'grant_type': 'refresh_token',
    'client_id': token_data['client_id'],
    'client_secret': token_data['client_secret'],
    'refresh_token': token_data['refresh_token']
}

response = requests.post('https://oauth2.googleapis.com/token', data=data)

if response.status_code == 200:
    new_token = response.json()
    token_data['token'] = new_token['access_token']
    # Calculate expiry (usually 1 hour from now)
    from datetime import datetime, timedelta, timezone
    token_data['expiry'] = (datetime.now(timezone.utc) + timedelta(seconds=new_token['expires_in'])).isoformat()

    # Save updated token
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)

    print("✓ Token refreshed successfully!")
    print(f"✓ New token valid until: {token_data['expiry']}")
else:
    print(f"✗ Failed to refresh token: {response.text}")

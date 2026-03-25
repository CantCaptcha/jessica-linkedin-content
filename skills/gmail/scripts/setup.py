#!/usr/bin/env python3
"""
Manual OAuth authentication script for Gmail.
This script provides a URL for manual authorization.
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import json

# We'll use the same OAuth client as Calendar, but with Gmail scopes
CREDENTIALS_FILE = Path('/home/rwhitaker/.openclaw/workspace/skills/google-calendar/config/credentials.json')
TOKEN_FILE = Path(__file__).parent.parent / 'config' / 'token.json'

# Combined scopes for Calendar + Gmail
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar.freebusy',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]

print("=" * 60)
print("Gmail + Calendar OAuth Authentication")
print("=" * 60)
print()

if not CREDENTIALS_FILE.exists():
    print(f"Error: {CREDENTIALS_FILE} not found!")
    print("Using existing Calendar OAuth credentials.")
    exit(1)

try:
    # Load credentials to get redirect_uri
    with open(CREDENTIALS_FILE, 'r') as f:
        creds_data = json.load(f)

    redirect_uri = creds_data.get('installed', {}).get('redirect_uris', ['http://localhost'])[0]
    print(f"Using redirect URI: {redirect_uri}")
    print()
    print("This will authenticate for both Calendar and Gmail.")
    print()

    # Create config directory if needed
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE),
        SCOPES,
        redirect_uri=redirect_uri
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'  # Force re-authorization to get new scopes
    )

    print("Step 1: Visit this URL to authorize:")
    print("-" * 60)
    print(authorization_url)
    print("-" * 60)
    print()

    auth_code = input("Step 2: Paste the authorization code here: ").strip()

    flow.fetch_token(code=auth_code)
    creds = flow.credentials

    print("\nSaving credentials...")
    print(f"Saving to: {TOKEN_FILE}")

    # Manually save the credentials as JSON
    token_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes,
        'expiry': creds.expiry.isoformat() if creds.expiry else None
    }

    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)

    print(f"✓ Credentials saved to: {TOKEN_FILE}")

    if TOKEN_FILE.exists():
        print(f"✓ Verified: file exists and has {TOKEN_FILE.stat().st_size} bytes")

    print()
    print("=" * 60)
    print("✓ Authentication successful!")
    print("=" * 60)
    print(f"Scopes granted: {len(creds.scopes)}")
    print(f" - Calendar access: ✓")
    print(f" - Gmail access: ✓")

except Exception as e:
    print()
    print("=" * 60)
    print("✗ Authentication failed")
    print("=" * 60)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

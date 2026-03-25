#!/usr/bin/env python3
"""
Manual OAuth authentication script for Google Calendar.
This script provides a URL for manual authorization instead of opening a browser.
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from pathlib import Path
import json

SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/calendar.events',
          'https://www.googleapis.com/auth/calendar.freebusy']

CRED_DIR = Path(__file__).parent.parent / 'config'
CREDENTIALS_FILE = CRED_DIR / 'credentials.json'
TOKEN_FILE = CRED_DIR / 'token.json'

print("=" * 60)
print("Google Calendar Manual Authentication")
print("=" * 60)
print()

if not CREDENTIALS_FILE.exists():
    print(f"Error: {CREDENTIALS_FILE} not found!")
    print("Please place credentials.json in the config directory.")
    exit(1)

try:
    # Load credentials to get redirect_uri
    with open(CREDENTIALS_FILE, 'r') as f:
        creds_data = json.load(f)

    redirect_uri = creds_data.get('installed', {}).get('redirect_uris', ['http://localhost'])[0]
    print(f"Using redirect URI: {redirect_uri}")
    print()

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE),
        SCOPES,
        redirect_uri=redirect_uri
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
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

except Exception as e:
    print()
    print("=" * 60)
    print("✗ Authentication failed")
    print("=" * 60)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

#!/usr/bin/env python3
"""
Manual OAuth authentication script for personal Gmail (richwhit@gmail.com).
This will create Google Cloud OAuth credentials for personal account.
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
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
TOKEN_FILE = CRED_DIR / 'token.json'

print("=" * 60)
print("Personal Gmail (richwhit@gmail.com) OAuth Setup")
print("=" * 60)
print()

CRED_DIR.mkdir(parents=True, exist_ok=True)

print("Step 1: Create OAuth credentials for personal Gmail")
print("-" * 60)
print("You'll need to create a new Google Cloud project or use an existing one:")
print()
print("1. Go to: https://console.cloud.google.com/")
print("2. Create a new project (or use existing)")
print("3. Go to: APIs & Services > Library")
print("4. Search for and enable:")
print("   - Google Calendar API")
print("   - Gmail API")
print("5. Go to: APIs & Services > Credentials")
print("6. Create Credentials > OAuth client ID")
print("7. Configure OAuth consent screen (External is fine for personal use)")
print("8. Select 'Desktop application'")
print("9. Download the credentials file")
print()
print("⚠️  IMPORTANT: Use a DIFFERENT OAuth client than DCG account!")
print("   DCG uses client_id starting with: 298800104924...")
print()

if not CREDENTIALS_FILE.exists():
    input("Press Enter after you've placed credentials.json in the config directory...")

try:
    # Load credentials to get redirect_uri
    with open(CREDENTIALS_FILE, 'r') as f:
        creds_data = json.load(f)

    redirect_uri = creds_data.get('installed', {}).get('redirect_uris', ['http://localhost'])[0]
    print(f"Using redirect URI: {redirect_uri}")
    print()
    print("Step 2: Authenticate with personal Gmail account")
    print("-" * 60)
    print("This will open a browser for you to authorize.")
    print()

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE),
        SCOPES,
        redirect_uri=redirect_uri
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    print("Visit this URL to authorize:")
    print("-" * 60)
    print(authorization_url)
    print("-" * 60)
    print()

    auth_code = input("Paste the authorization code here: ").strip()

    flow.fetch_token(code=auth_code)
    creds = flow.credentials

    print("\nSaving credentials...")
    print(f"Saving to: {TOKEN_FILE}")

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
    print("✓ Personal Gmail authentication complete!")
    print("=" * 60)
    print(f"✓ Calendar access enabled")
    print(f"✓ Gmail access enabled")
    print(f"✓ Account: richwhit@gmail.com")

except Exception as e:
    print()
    print("=" * 60)
    print("✗ Authentication failed")
    print("=" * 60)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

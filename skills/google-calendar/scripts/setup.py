#!/usr/bin/env python3
"""
Google Calendar Setup Script

This script helps set up OAuth credentials for Google Calendar API access.
Run this script to get started with Google Calendar integration.
"""

import os
import json
import webbrowser
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/calendar.events',
          'https://www.googleapis.com/auth/calendar.freebusy']


def get_credentials_path():
    """Get the path to store credentials."""
    skill_dir = Path(__file__).parent.parent
    return skill_dir / 'config'


def setup():
    """Set up Google Calendar OAuth credentials."""
    cred_dir = get_credentials_path()
    cred_dir.mkdir(exist_ok=True)

    credentials_file = cred_dir / 'credentials.json'
    token_file = cred_dir / 'token.json'

    print("=" * 60)
    print("Google Calendar Setup")
    print("=" * 60)
    print()

    # Check if credentials already exist
    if token_file.exists():
        print("Credentials already exist at:", token_file)
        overwrite = input("Do you want to re-authenticate? (y/N): ").lower()
        if overwrite != 'y':
            print("Setup cancelled. Using existing credentials.")
            return

    print("Step 1: Get OAuth credentials")
    print("-" * 60)
    print("To use Google Calendar, you need OAuth credentials from Google Cloud:")
    print()
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a new project (or select existing)")
    print("3. Go to: APIs & Services > Library")
    print("4. Search for 'Google Calendar API' and enable it")
    print("5. Go to: APIs & Services > Credentials")
    print("6. Click 'Create Credentials' > 'OAuth client ID'")
    print("7. Select 'Desktop application'")
    print("8. Download the credentials file as 'credentials.json'")
    print("9. Place it at:", credentials_file)
    print()
    print(f"Current credentials file location: {credentials_file}")
    print()

    # Wait for credentials file
    while not credentials_file.exists():
        input("Press Enter after you've placed the credentials.json file...")
        if not credentials_file.exists():
            print("File not found. Please check the path and try again.")

    print()
    print("Step 2: Authenticate")
    print("-" * 60)
    print("A browser window will open for you to authorize the app.")
    print()

    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_file, SCOPES)
        creds = flow.run_local_server(port=0)

        # Save the credentials
        with open(token_file, 'w') as f:
            creds.to_json(f)

        print()
        print("=" * 60)
        print("✓ Setup complete!")
        print("=" * 60)
        print(f"Credentials saved to: {token_file}")
        print()

        # Test the connection
        print("Testing connection...")
        service = build('calendar', 'v3', credentials=creds)
        calendar_list = service.calendarList().list().execute()

        print(f"✓ Successfully connected! Found {len(calendar_list.get('items', []))} calendars.")
        print()
        print("You're ready to use Google Calendar with OpenClaw!")

    except Exception as e:
        print()
        print("=" * 60)
        print("✗ Setup failed")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("Please check:")
        print("1. credentials.json is valid")
        print("2. Google Calendar API is enabled in your Google Cloud project")
        print("3. OAuth consent screen is configured")
        return False

    return True


if __name__ == '__main__':
    setup()

#!/usr/bin/env python3
"""Get the full content of a specific email message."""

import sys
import base64
from pathlib import Path

# Add the Gmail skill to the path
sys.path.insert(0, '/home/rwhitaker/.openclaw/workspace/skills/gmail-personal')

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Configuration
CRED_DIR = Path('/home/rwhitaker/.openclaw/workspace/skills/gmail-personal/config')
TOKEN_FILE = CRED_DIR / 'token.json'

def get_credentials():
    """Load or refresh Gmail credentials."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE)

    # Refresh if expired
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as e:
            print(f"Error refreshing credentials: {e}")
            return None

    return creds

def get_message_content(message_id: str):
    """Get the full content of a message."""
    creds = get_credentials()
    if not creds:
        print("Error: No valid credentials found.")
        return None

    try:
        service = build('gmail', 'v1', credentials=creds)

        # Get the message with full content
        message = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()

        # Extract the email body
        payload = message.get('payload', {})
        body_data = None

        # Helper function to recursively find the body
        def find_body(part):
            if 'body' in part and 'data' in part['body']:
                return part['body']['data']
            if 'parts' in part:
                for subpart in part['parts']:
                    result = find_body(subpart)
                    if result:
                        return result
            return None

        body_data = find_body(payload)

        if body_data:
            # Decode base64
            body_bytes = base64.urlsafe_b64decode(body_data)
            content = body_bytes.decode('utf-8')
            return content
        else:
            return "No body content found"

    except Exception as e:
        print(f"Error getting message: {e}")
        return None

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message_id = sys.argv[1]
        content = get_message_content(message_id)
        if content:
            print(content)
        else:
            print("Failed to get message content")
    else:
        print("Usage: python3 get_email_content.py <message_id>")

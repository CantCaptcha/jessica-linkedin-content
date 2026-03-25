#!/usr/bin/env python3
"""
Gmail API Helper Script - HTML Support

This script provides functions to interact with Gmail API.
It supports:
- Sending HTML emails
- Listing emails
"""

import sys
import base64
import json
from pathlib import Path
from typing import Optional, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Google libraries not installed.")
    print("Run: pip3 install google-auth google-auth-oauthlib google-api-python-client")
    sys.exit(1)

# Configuration
SKILL_DIR = Path(__file__).parent.parent
CRED_DIR = SKILL_DIR / 'config'
TOKEN_FILE = CRED_DIR / 'token.json'
CREDENTIALS_FILE = CRED_DIR / 'credentials.json'

# Scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]


def get_credentials():
    """Load or refresh Gmail credentials."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE)

    # Refresh if expired
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save refreshed credentials manually
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
        except Exception as e:
            print(f"Error refreshing credentials: {e}")
            return None

    if not creds or not creds.valid:
        print("Error: No valid credentials found.")
        print(f"Please run: python3 {SKILL_DIR}/scripts/setup.py")
        return None

    return creds


def get_service():
    """Get authenticated Gmail service."""
    creds = get_credentials()
    if not creds:
        return None

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error creating service: {e}")
        return None


def create_email(to: str, subject: str, body: str, from_name: Optional[str] = None, is_html: bool = False) -> MIMEMultipart:
    """Create an email message (text or HTML)."""
    message = MIMEMultipart('alternative')

    # Set headers
    message['To'] = to
    message['Subject'] = subject

    if from_name:
        message['From'] = formataddr((from_name, 'richard.whitaker@cybersecgru.com'))

    # Add text part
    if is_html:
        # Create HTML version
        html_part = MIMEText(body, 'html')
        message.attach(html_part)

        # Also add plain text fallback
        plain_text = body.replace('<br>', '\n').replace('<strong>', '').replace('</strong>', '')
        plain_text = plain_text.replace('<h2>', '').replace('</h2>', '').replace('</h2>', '')
        plain_part = MIMEText(plain_text, 'plain')
        message.attach(plain_part)
    else:
        # Plain text email
        text_part = MIMEText(body, 'plain')
        message.attach(text_part)

    return message


def send_email(to: str, subject: str, body: str, from_name: Optional[str] = None, is_html: bool = False) -> str:
    """Send an email using Gmail API.

    Returns:
        Message ID of the sent email, or None if failed.
    """
    service = get_service()
    if not service:
        return None

    try:
        # Read HTML body from file if it's a path
        import os
        if is_html and os.path.isfile(body):
            with open(body, 'r') as f:
                html_body = f.read()
        else:
            html_body = body

        if is_html:
            # Create HTML email directly
            message = MIMEText(html_body, 'html')
        else:
            # Plain text email
            message = MIMEText(html_body, 'plain')

        # Set headers
        message['To'] = to
        message['Subject'] = subject

        if from_name:
            message['From'] = formataddr((from_name, 'richard.whitaker@cybersecgru.com'))

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        send_message = service.users().messages().send(
            userId="me",
            body=create_message
        ).execute()

        return send_message.get('id')

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def list_emails(max_results: int = 10) -> List[dict]:
    """List recent emails.

    Returns:
        List of email dictionaries with id, snippet, sender, subject, date.
    """
    service = get_service()
    if not service:
        return []

    try:
        results = service.users().messages().list(
            userId='me',
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])
        emails = []

        for msg in messages:
            msg_data = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()

            headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}

            emails.append({
                'id': msg['id'],
                'snippet': msg_data.get('snippet', ''),
                'from': headers.get('From', ''),
                'subject': headers.get('Subject', ''),
                'date': headers.get('Date', '')
            })

        return emails

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Gmail Helper')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Send email command
    send_parser = subparsers.add_parser('send', help='Send an email')
    send_parser.add_argument('--to', required=True, help='Recipient email address')
    send_parser.add_argument('--subject', required=True, help='Email subject')
    send_parser.add_argument('--body', required=True, help='Email body')
    send_parser.add_argument('--from-name', help='Sender name')
    send_parser.add_argument('--html', action='store_true', help='Send as HTML email')

    # List emails command
    list_parser = subparsers.add_parser('list', help='List recent emails')
    list_parser.add_argument('--max', type=int, default=10, help='Maximum emails to list')

    args = parser.parse_args()

    if args.command == 'send':
        message_id = send_email(args.to, args.subject, args.body, args.from_name, args.html)
        if message_id:
            print(f"✓ Email sent successfully! Message ID: {message_id}")
        else:
            print("✗ Failed to send email")
    elif args.command == 'list':
        emails = list_emails(args.max)
        for email in emails:
            print(f"From: {email['from']}")
            print(f"Subject: {email['subject']}")
            print(f"Date: {email['date']}")
            print(f"Snippet: {email['snippet']}")
            print()

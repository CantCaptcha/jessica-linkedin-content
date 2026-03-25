#!/usr/bin/env python3
"""
Gmail API Helper Script

This script provides functions to interact with Gmail API.
It supports:
- Sending emails
- Listing emails
"""

import sys
import base64
import json
from pathlib import Path
from typing import Optional, List
from email.message import EmailMessage

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
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
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


def create_email(to: str, subject: str, body: str, from_name: Optional[str] = None) -> EmailMessage:
    """Create an email message."""
    message = EmailMessage()
    message.set_content(body)

    message['To'] = to
    message['Subject'] = subject

    if from_name:
        message['From'] = from_name

    return message


def send_email(to: str, subject: str, body: str, from_name: Optional[str] = None) -> str:
    """Send an email using Gmail API.

    Returns:
        Message ID of the sent email, or None if failed.
    """
    service = get_service()
    if not service:
        return None

    try:
        email_message = create_email(to, subject, body, from_name)
        encoded_message = base64.urlsafe_b64encode(email_message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        send_message = service.users().messages().send(
            userId="me",
            body=create_message
        ).execute()

        return send_message.get('id')

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def get_label_id(label_name: str) -> Optional[str]:
    """Get the Gmail API label ID for a given label name.

    Args:
        label_name: The display name of the label (e.g., "JOB RESPONDED")

    Returns:
        The label ID, or None if not found.
    """
    service = get_service()
    if not service:
        return None

    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        for label in labels:
            if label.get('name', '').upper() == label_name.upper():
                return label.get('id')

        return None

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def get_message_labels(message_id: str) -> List[str]:
    """Get display names of labels for a specific message.

    Args:
        message_id: The ID of the message

    Returns:
        List of label display names (e.g., ['INBOX', 'JOB REJECT', 'JOB RESPONDED'])
    """
    service = get_service()
    if not service:
        return []

    try:
        msg_data = service.users().messages().get(
            userId='me',
            id=message_id,
            format='metadata'
        ).execute()

        # Get label IDs from the message
        label_ids = msg_data.get('labelIds', [])

        # If no label IDs, return empty list
        if not label_ids:
            return []

        # Map label IDs to display names
        results = service.users().labels().list(userId='me').execute()
        all_labels = results.get('labels', [])

        # Create a mapping from ID to display name
        label_map = {label['id']: label['name'] for label in all_labels}

        # Convert label IDs to display names
        label_names = [label_map[lid] for lid in label_ids if lid in label_map]

        return label_names

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


def reply_to_message(message_id: str, body: str) -> Optional[str]:
    """Reply to a specific message.

    Args:
        message_id: The ID of the message to reply to
        body: The reply body text

    Returns:
        The message ID of the sent reply, or None if failed.
    """
    service = get_service()
    if not service:
        return None

    try:
        # Get the original message to extract details
        original_msg = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()

        payload = original_msg.get('payload', {})
        headers = {h['name']: h['value'] for h in payload.get('headers', [])}

        from_email = headers.get('From', '')
        subject = headers.get('Subject', '')
        to_email = headers.get('To', '')
        cc_email = headers.get('Cc', '')
        message_id_header = headers.get('Message-ID', '')
        references = headers.get('References', '')
        in_reply_to = headers.get('In-Reply-To', '')

        # Extract sender's email from From header
        if '<' in from_email and '>' in from_email:
            sender_email = from_email[from_email.find('<') + 1:from_email.rfind('>')]
        else:
            sender_email = from_email.strip()

        # Create reply message
        message = EmailMessage()
        message.set_content(body)
        message['To'] = sender_email
        message['Subject'] = subject if subject.lower().startswith('re:') else f'Re: {subject}'
        if cc_email:
            message['Cc'] = cc_email

        # Set reply threading headers
        if in_reply_to:
            message['In-Reply-To'] = in_reply_to
        if references:
            message['References'] = references
        elif message_id_header:
            message['References'] = message_id_header

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message, 'threadId': original_msg.get('threadId')}

        # Send the reply
        result = service.users().messages().send(
            userId="me",
            body=create_message
        ).execute()

        return result.get('id')

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def add_labels(message_id: str, labels: List[str]) -> bool:
    """Add labels to a message.

    Args:
        message_id: The ID of the message
        labels: List of label names to add (will be resolved to label IDs)

    Returns:
        True if successful, False otherwise.
    """
    service = get_service()
    if not service:
        return False

    try:
        # Resolve label names to label IDs
        label_ids = []
        for label_name in labels:
            label_id = get_label_id(label_name)
            if label_id:
                label_ids.append(label_id)
            else:
                print(f"⚠️  Label not found: {label_name}")

        if not label_ids:
            return False

        result = service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'addLabelIds': label_ids}
        ).execute()

        return 'labelIds' in result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return False


def remove_labels(message_id: str, labels: List[str]) -> bool:
    """Remove labels from a message.

    Args:
        message_id: The ID of the message
        labels: List of label names to remove

    Returns:
        True if successful, False otherwise.
    """
    service = get_service()
    if not service:
        return False

    try:
        result = service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': labels}
        ).execute()

        return 'labelIds' in result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return False


def mark_as_read(message_id: str) -> bool:
    """Mark a message as read by removing the UNREAD label.

    Args:
        message_id: The ID of the message

    Returns:
        True if successful, False otherwise.
    """
    return remove_labels(message_id, ['UNREAD'])


def list_emails(max_results: int = 10, query: Optional[str] = None) -> List[dict]:
    """List recent emails.

    Args:
        max_results: Maximum number of emails to return
        query: Gmail search query (e.g., "label:JOB REJECT", "from:someone@example.com")

    Returns:
        List of email dictionaries with id, snippet, sender, subject, date.
    """
    service = get_service()
    if not service:
        return []

    try:
        list_params = {
            'userId': 'me',
            'maxResults': max_results
        }
        if query:
            list_params['q'] = query

        results = service.users().messages().list(**list_params).execute()

        messages = results.get('messages', [])
        emails = []

        for msg in messages:
            msg_data = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date', 'X-Gmail-Labels']
            ).execute()

            headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}

            emails.append({
                'id': msg['id'],
                'snippet': msg_data.get('snippet', ''),
                'from': headers.get('From', ''),
                'subject': headers.get('Subject', ''),
                'date': headers.get('Date', ''),
                'labels': headers.get('X-Gmail-Labels', '')
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

    # List emails command
    list_parser = subparsers.add_parser('list', help='List recent emails')
    list_parser.add_argument('--max', type=int, default=10, help='Maximum emails to list')
    list_parser.add_argument('--query', type=str, help='Gmail search query (e.g., "label:JOB REJECT")')
    list_parser.add_argument('--label', type=str, help='Search by Gmail label')

    # Process job rejects command
    reject_parser = subparsers.add_parser('process-rejects', help='Process JOB REJECT messages')
    reject_parser.add_argument('--template', type=str, required=True, help='Path to reply template file')
    reject_parser.add_argument('--dry-run', action='store_true', help='Show what would happen without sending')

    args = parser.parse_args()

    if args.command == 'send':
        message_id = send_email(args.to, args.subject, args.body)
        if message_id:
            print(f"✓ Email sent successfully! Message ID: {message_id}")
        else:
            print("✗ Failed to send email")
    elif args.command == 'list':
        query = args.query
        if args.label:
            query = f'label:{args.label}'
        emails = list_emails(args.max, query)
        if emails:
            query_desc = f" (query: {query})" if query else ""
            print(f"\n📧 Recent emails ({len(emails)}){query_desc}:")
            for email in emails:
                print(f"  From: {email['from'][:50]}")
                print(f"  Subject: {email['subject'][:50]}")
                print(f"  Date: {email['date']}")
                print(f"  ID: {email['id']}")
                print()
        else:
            query_desc = f" matching '{query}'" if query else ""
            print(f"No emails found{query_desc}.")

    elif args.command == 'process-rejects':
        dry_run = args.dry_run

        # Load template
        template_path = Path(args.template)
        if not template_path.exists():
            print(f"✗ Template file not found: {template_path}")
            sys.exit(1)

        with open(template_path, 'r') as f:
            template_body = f.read().strip()

        mode_msg = "🔍 [DRY RUN] Finding JOB REJECT messages..." if dry_run else "\n🔍 Finding JOB REJECT messages without JOB RESPONDED label (last 10 days)..."
        print(mode_msg)

        reject_emails = list_emails(max_results=50, query='label:JOB REJECT newer_than:10d')

        if not reject_emails:
            print("✓ No JOB REJECT messages found.")
            sys.exit(0)

        print(f"Found {len(reject_emails)} JOB REJECT message(s).\n")

        if dry_run:
            print("=" * 60)
            print("DRY RUN MODE - No emails will be sent")
            print("=" * 60)
            print()

        processed_count = 0
        skipped_count = 0

        for email in reject_emails:
            msg_id = email['id']
            labels = get_message_labels(msg_id)

            # Check if already responded
            if 'JOB RESPONDED' in labels:
                print(f"⏭️  Skipping (already responded): {email['subject'][:50]}")
                skipped_count += 1
                continue

            # Show what would happen
            print(f"📝 Would reply to: {email['subject'][:50]}")
            print(f"   From: {email['from'][:50]}")
            print(f"   Message ID: {msg_id}")

            if not dry_run:
                # Actually send reply
                reply_id = reply_to_message(msg_id, template_body)

                if reply_id:
                    # Add JOB RESPONDED label
                    add_labels(msg_id, ['JOB RESPONDED'])
                    # Mark as read
                    mark_as_read(msg_id)
                    print(f"   ✓ Reply sent (ID: {reply_id[:20]}...)")
                    print(f"   ✓ Added JOB RESPONDED label")
                    print(f"   ✓ Marked as read")
                    processed_count += 1
                else:
                    print(f"   ✗ Failed to send reply")
            else:
                # Dry run - just show template
                print(f"   Reply preview:")
                print(f"   {'─' * 40}")
                for line in template_body.split('\n'):
                    print(f"   {line}")
                print(f"   {'─' * 40}")
                print(f"   [DRY RUN] Would add JOB RESPONDED label")
                print(f"   [DRY RUN] Would mark as read")
                processed_count += 1

            print()

        print(f"\n✅ {'Dry run ' if dry_run else ''}Processing complete:")
        print(f"   - Would process: {processed_count}")
        print(f"   - Would skip: {skipped_count}")
        if dry_run:
            print(f"\nRun without --dry-run to actually send replies.")
    else:
        parser.print_help()

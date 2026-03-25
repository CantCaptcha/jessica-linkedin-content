#!/usr/bin/env python3
"""
Google Calendar API Helper Script

This script provides functions to interact with Google Calendar API.
It supports:
- Listing events
- Checking free/busy
- Creating events
- Updating events
- Deleting events
"""

import sys
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Optional, Any

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


def get_credentials():
    """Load or refresh Google Calendar credentials."""
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
    """Get authenticated Google Calendar service."""
    creds = get_credentials()
    if not creds:
        return None

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(f"Error creating service: {e}")
        return None


def parse_datetime(date_str: str) -> datetime:
    """Parse datetime string (various formats)."""
    formats = [
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S%z',
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    raise ValueError(f"Could not parse datetime: {date_str}")


def list_events(calendar_id: str = 'primary',
                time_min: Optional[str] = None,
                time_max: Optional[str] = None,
                max_results: int = 10,
                query: Optional[str] = None) -> List[Dict]:
    """
    List events from a calendar.

    Args:
        calendar_id: Calendar ID (default 'primary')
        time_min: Start time (ISO format or YYYY-MM-DD HH:MM)
        time_max: End time (ISO format or YYYY-MM-DD HH:MM)
        max_results: Maximum number of events
        query: Search query for events

    Returns:
        List of event dictionaries
    """
    service = get_service()
    if not service:
        return []

    try:
        # Parse time strings if provided
        if time_min:
            try:
                time_min = parse_datetime(time_min).isoformat()
            except ValueError:
                pass  # Already in ISO format

        if time_max:
            try:
                time_max = parse_datetime(time_max).isoformat()
            except ValueError:
                pass  # Already in ISO format

        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            q=query,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return events

    except HttpError as e:
        print(f"Error listing events: {e}")
        return []


def check_freebusy(calendar_ids: List[str],
                   time_min: str,
                   time_max: str) -> Dict[str, Any]:
    """
    Check free/busy time for calendars.

    Args:
        calendar_ids: List of calendar IDs to check
        time_min: Start time (ISO format or YYYY-MM-DD HH:MM)
        time_max: End time (ISO format or YYYY-MM-DD HH:MM)

    Returns:
        Free/busy response
    """
    service = get_service()
    if not service:
        return {}

    try:
        # Parse time strings
        try:
            time_min = parse_datetime(time_min).isoformat()
        except ValueError:
            pass  # Already in ISO format

        try:
            time_max = parse_datetime(time_max).isoformat()
        except ValueError:
            pass  # Already in ISO format

        body = {
            'timeMin': time_min,
            'timeMax': time_max,
            'items': [{'id': cal_id} for cal_id in calendar_ids]
        }

        freebusy_result = service.freebusy().query(body=body).execute()
        return freebusy_result

    except HttpError as e:
        print(f"Error checking free/busy: {e}")
        return {}


def create_event(calendar_id: str = 'primary',
                  title: str = '',
                  start: str = '',
                  end: str = '',
                  description: str = '',
                  location: str = '',
                  attendees: Optional[List[str]] = None) -> Dict:
    """
    Create a new calendar event.

    Args:
        calendar_id: Calendar ID (default 'primary')
        title: Event title
        start: Start time (ISO format or YYYY-MM-DD HH:MM)
        end: End time (ISO format or YYYY-MM-DD HH:MM)
        description: Event description
        location: Event location
        attendees: List of email addresses for attendees

    Returns:
        Created event dictionary
    """
    service = get_service()
    if not service:
        return {}

    try:
        # Parse datetime strings
        start_dt = parse_datetime(start)
        end_dt = parse_datetime(end)

        # Determine if it's an all-day event
        all_day = (start_dt.hour == 0 and start_dt.minute == 0 and
                   end_dt.hour == 0 and end_dt.minute == 0)

        if all_day:
            event_body = {
                'summary': title,
                'description': description,
                'location': location,
                'start': {'date': start_dt.strftime('%Y-%m-%d')},
                'end': {'date': end_dt.strftime('%Y-%m-%d')},
            }
        else:
            event_body = {
                'summary': title,
                'description': description,
                'location': location,
                'start': {'dateTime': start_dt.isoformat()},
                'end': {'dateTime': end_dt.isoformat()},
            }

        if attendees:
            event_body['attendees'] = [{'email': email} for email in attendees]

        event = service.events().insert(
            calendarId=calendar_id,
            body=event_body
        ).execute()

        return event

    except HttpError as e:
        print(f"Error creating event: {e}")
        return {}


def update_event(calendar_id: str = 'primary',
                  event_id: str = '',
                  **kwargs) -> Dict:
    """
    Update an existing calendar event.

    Args:
        calendar_id: Calendar ID
        event_id: Event ID to update
        **kwargs: Fields to update (title, description, location, start, end, etc.)

    Returns:
        Updated event dictionary
    """
    service = get_service()
    if not service:
        return {}

    try:
        # Get current event
        event = service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()

        # Update fields
        if 'title' in kwargs:
            event['summary'] = kwargs['title']
        if 'description' in kwargs:
            event['description'] = kwargs['description']
        if 'location' in kwargs:
            event['location'] = kwargs['location']

        # Update times if provided
        if 'start' in kwargs:
            start_dt = parse_datetime(kwargs['start'])
            if start_dt.hour == 0 and start_dt.minute == 0:
                event['start'] = {'date': start_dt.strftime('%Y-%m-%d')}
            else:
                event['start'] = {'dateTime': start_dt.isoformat()}

        if 'end' in kwargs:
            end_dt = parse_datetime(kwargs['end'])
            if end_dt.hour == 0 and end_dt.minute == 0:
                event['end'] = {'date': end_dt.strftime('%Y-%m-%d')}
            else:
                event['end'] = {'dateTime': end_dt.isoformat()}

        # Update attendees if provided
        if 'attendees' in kwargs:
            event['attendees'] = [{'email': email} for email in kwargs['attendees']]

        # Save the update
        updated_event = service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=event
        ).execute()

        return updated_event

    except HttpError as e:
        print(f"Error updating event: {e}")
        return {}


def delete_event(calendar_id: str, event_id: str) -> bool:
    """
    Delete a calendar event.

    Args:
        calendar_id: Calendar ID
        event_id: Event ID to delete

    Returns:
        True if successful, False otherwise
    """
    service = get_service()
    if not service:
        return False

    try:
        service.events().delete(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        return True

    except HttpError as e:
        print(f"Error deleting event: {e}")
        return False


def format_event(event: Dict) -> str:
    """Format an event dictionary for display."""
    summary = event.get('summary', 'No title')
    event_id = event.get('id', '')

    start = event.get('start', {})
    end = event.get('end', {})

    # Get start/end times
    start_time = start.get('dateTime', start.get('date', ''))
    end_time = end.get('dateTime', end.get('date', ''))

    # Parse for nicer display
    try:
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))

        if 'date' in start:  # All-day event
            start_str = start_dt.strftime('%Y-%m-%d')
            end_str = end_dt.strftime('%Y-%m-%d')
        else:
            start_str = start_dt.strftime('%Y-%m-%d %H:%M')
            end_str = end_dt.strftime('%Y-%m-%d %H:%M')
    except:
        start_str = start_time
        end_str = end_time

    location = event.get('location', '')
    description = event.get('description', '')

    output = [f"📅 {summary}"]
    output.append(f"   Time: {start_str} - {end_str}")
    output.append(f"   ID: {event_id}")

    if location:
        output.append(f"   Location: {location}")

    if description:
        desc_preview = description[:100] + '...' if len(description) > 100 else description
        output.append(f"   Description: {desc_preview}")

    return '\n'.join(output)


def format_freebusy(freebusy_result: Dict, calendar_id: str = 'primary') -> str:
    """Format free/busy result for display."""
    calendars = freebusy_result.get('calendars', {})
    busy = calendars.get(calendar_id, {}).get('busy', [])

    if not busy:
        return "✓ No busy times - all available!"

    output = ["📅 Busy times:"]
    for busy_time in busy:
        start = datetime.fromisoformat(busy_time['start'].replace('Z', '+00:00'))
        end = datetime.fromisoformat(busy_time['end'].replace('Z', '+00:00'))
        output.append(f"   {start.strftime('%Y-%m-%d %H:%M')} - {end.strftime('%H:%M')}")

    return '\n'.join(output)


def main():
    """CLI interface for testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Google Calendar API Helper')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # List command
    list_parser = subparsers.add_parser('list', help='List events')
    list_parser.add_argument('--calendar', default='primary', help='Calendar ID')
    list_parser.add_argument('--from', dest='time_min', help='Start time')
    list_parser.add_argument('--to', dest='time_max', help='End time')
    list_parser.add_argument('--max', type=int, default=10, help='Max results')
    list_parser.add_argument('--query', help='Search query')

    # Freebusy command
    freebusy_parser = subparsers.add_parser('freebusy', help='Check free/busy')
    freebusy_parser.add_argument('--calendars', nargs='+', default=['primary'], help='Calendar IDs')
    freebusy_parser.add_argument('--from', dest='time_min', required=True, help='Start time')
    freebusy_parser.add_argument('--to', dest='time_max', required=True, help='End time')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create event')
    create_parser.add_argument('--calendar', default='primary', help='Calendar ID')
    create_parser.add_argument('--title', required=True, help='Event title')
    create_parser.add_argument('--start', required=True, help='Start time')
    create_parser.add_argument('--end', required=True, help='End time')
    create_parser.add_argument('--description', help='Description')
    create_parser.add_argument('--location', help='Location')
    create_parser.add_argument('--attendees', nargs='+', help='Attendee emails')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'list':
        events = list_events(
            calendar_id=args.calendar,
            time_min=args.time_min,
            time_max=args.time_max,
            max_results=args.max,
            query=args.query
        )
        for event in events:
            print(format_event(event))
            print()

    elif args.command == 'freebusy':
        result = check_freebusy(args.calendars, args.time_min, args.time_max)
        for cal_id in args.calendars:
            print(f"Calendar: {cal_id}")
            print(format_freebusy(result, cal_id))
            print()

    elif args.command == 'create':
        event = create_event(
            calendar_id=args.calendar,
            title=args.title,
            start=args.start,
            end=args.end,
            description=args.description,
            location=args.location,
            attendees=args.attendees
        )
        if event:
            print("✓ Event created:")
            print(format_event(event))


if __name__ == '__main__':
    main()

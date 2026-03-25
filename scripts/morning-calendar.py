#!/usr/bin/env python3
"""Get schedule for today or tomorrow from all calendars and highlight overlaps."""

import sys
import subprocess
import json
import re
sys.path.insert(0, '/home/rwhitaker/.openclaw/workspace/skills/google-calendar')

from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timezone, timedelta

# Credential paths
WORK_CRED_DIR = Path('/home/rwhitaker/.openclaw/workspace/skills/google-calendar/config')
WORK_TOKEN = WORK_CRED_DIR / 'token.json'

# All calendars now read from DCG work account (shared calendars)
CALENDARS = [
    ('DCG', 'primary', WORK_TOKEN),
    ('United', 'teq6qq3e0q1l0nr1leu7kkr78ppju73t@import.calendar.google.com', WORK_TOKEN),
]

def get_weather():
    """Get current weather for Union, KY using Open-Meteo API."""
    try:
        result = subprocess.run(
            ['curl', '-s', '--max-time', '3',
             'https://api.open-meteo.com/v1/forecast?latitude=39.33&longitude=-84.54&current_weather=true'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if 'current_weather' in data:
                cw = data['current_weather']
                temp_c = cw['temperature']
                temp_f = int(round((temp_c * 9/5) + 32))
                code = cw['weathercode']
                # Simple weather code to emoji mapping
                weather_map = {
                    0: '☀️', 1: '🌤️', 2: '⛅', 3: '☁️',
                    45: '🌫️', 48: '🌫️',
                    51: '🌦️', 53: '🌦️', 55: '🌦️',
                    61: '🌧️', 63: '🌧️', 65: '🌧️',
                    71: '🌨️', 73: '🌨️', 75: '🌨️', 77: '🌨️',
                    80: '🌦️', 81: '🌦️', 82: '🌦️',
                    85: '🌨️', 86: '🌨️',
                    95: '⛈️', 96: '⛈️', 99: '⛈️'
                }
                emoji = weather_map.get(code, '🌤️')
                return f"🌤️ Union, KY: {emoji} {temp_f}°F"
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception, json.JSONDecodeError):
        pass
    return None


def get_backup_status():
    """Check the status of the most recent backup."""
    backup_log = Path('/home/rwhitaker/.openclaw/logs/backup.log')
    
    if not backup_log.exists():
        return None
    
    try:
        content = backup_log.read_text()
        
        # Find the last backup entry (look for the last "🦞 OpenClaw Backup" line)
        lines = content.split('\n')
        
        # Find all backup starts
        backup_starts = [i for i, line in enumerate(lines) if '🦞 OpenClaw Backup' in line]
        
        if not backup_starts:
            return None
        
        # Get the last backup
        last_backup_idx = backup_starts[-1]
        backup_lines = lines[last_backup_idx:last_backup_idx + 50]  # Get up to 50 lines of the backup
        
        # Check for success
        backup_text = '\n'.join(backup_lines)
        
        if '✅ Backup complete!' in backup_text:
            # Extract the backup name and date
            for line in backup_lines:
                if line.startswith('Backup:'):
                    backup_name = line.split(':', 1)[1].strip()
                    # Extract the date from the backup name (format: YYYYMMDD)
                    match = re.search(r'(\d{8})', backup_name)
                    if match:
                        date_str = match.group(1)
                        date_formatted = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
                        return f"💾 Backup: ✅ Success ({date_formatted})"
            return f"💾 Backup: ✅ Success"
        
        # Check for errors
        if any('Error' in line or 'error' in line or 'Failed' in line for line in backup_lines):
            return f"💾 Backup: ❌ Failed"
        
        # If still running or incomplete
        return f"💾 Backup: ⏳ Incomplete"
    
    except Exception:
        return None


def get_bloom_tasks():
    """Read and parse Bloom Growth tasks from tasks/bloom-tasks.md."""
    task_file = Path('/home/rwhitaker/.openclaw/workspace/tasks/bloom-tasks.md')

    if not task_file.exists():
        return []

    content = task_file.read_text()

    # Parse active tasks section
    # Look for "### Task Name" followed by metadata
    active_tasks = []
    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Look for task headers (###)
        if line.startswith('### ') and i < len(lines) - 1:
            task_name = line.replace('###', '').strip()

            # Look for metadata in next lines
            task_info = {'name': task_name, 'due': None, 'days_until': None}
            j = i + 1

            while j < len(lines) and lines[j].startswith('-'):
                if '**Due:**' in lines[j]:
                    # Extract due date
                    match = re.search(r'\*\*Due:\*\*\s*(\d{4}-\d{2}-\d{2})', lines[j])
                    if match:
                        due_date_str = match.group(1)
                        try:
                            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                            today = datetime.now().date()
                            days_until = (due_date - today).days
                            task_info['due'] = due_date_str
                            task_info['days_until'] = days_until
                        except ValueError:
                            pass
                    # Also try MM/DD/YYYY format
                    match = re.search(r'\*\*Due:\*\*\s*(\d{1,2}/\d{1,2}/\d{4})', lines[j])
                    if match:
                        due_date_str = match.group(1)
                        try:
                            due_date = datetime.strptime(due_date_str, '%m/%d/%Y').date()
                            today = datetime.now().date()
                            days_until = (due_date - today).days
                            task_info['due'] = due_date_str
                            task_info['days_until'] = days_until
                        except ValueError:
                            pass
                j += 1

            # Check if this is in Active Tasks section
            # Look back to see if we're in the right section
            in_active = False
            k = i - 1
            while k >= 0:
                if lines[k].startswith('##'):
                    if lines[k] == '## Active Tasks':
                        in_active = True
                    break
                k -= 1

            if in_active:
                active_tasks.append(task_info)

        i += 1

    return active_tasks

def get_united_tasks():
    """Read and parse United tasks from tasks/united-tasks.md."""
    task_file = Path('/home/rwhitaker/.openclaw/workspace/tasks/united-tasks.md')

    if not task_file.exists():
        return []

    content = task_file.read_text()
    lines = content.split('\n')

    active_tasks = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Look for task lines (start with - **)
        if line.startswith('- ') and '**' in line and i < len(lines) - 1:
            # Extract task name (between ** and ** or end of line)
            task_name = line.split('**')[1].strip() if len(line.split('**')) > 1 else line[2:].strip()
            task_name = task_name.rstrip(')**').strip()

            # Look for metadata in next lines
            task_info = {'name': task_name, 'due': None, 'days_until': None, 'category': None}
            j = i + 1

            while j < len(lines) and lines[j].startswith('###'):
                break

            # Check for due dates
            if '**Due:**' in lines[j]:
                match = re.search(r'\*\*Due:\*\*\s*([^\*\*]+)', lines[j])
                if match:
                    due_text = match.group(1).strip()
                    try:
                        # Try MM/DD/YYYY format
                        due_date = datetime.strptime(due_text, '%m/%d/%Y').date()
                        today = datetime.now().date()
                        days_until = (due_date - today).days
                        task_info['due'] = due_text
                        task_info['days_until'] = days_until
                    except ValueError:
                        pass
                j += 1

            # Determine category (Priority, Later Today, Next Week)
            category = None
            k = i - 1
            while k >= 0:
                if lines[k].startswith('###'):
                    section_header = lines[k].lower()
                    if 'priority tasks' in section_header:
                        category = 'Priority Tasks'
                    elif 'later today' in section_header:
                        category = 'Later Today'
                    elif 'next week' in section_header:
                        category = 'Next Week'
                    break
                k -= 1

            if category:
                task_info['category'] = category

            # Check if we're in Active Tasks or Later Today section
            in_active_section = False
            k = i - 1
            while k >= 0:
                if lines[k].startswith('##'):
                    if '## Active Tasks' in lines[k] or '## Today' in lines[k]:
                        in_active_section = True
                    elif lines[k].startswith('###') or lines[k].startswith('####'):
                        break
                k -= 1

            if in_active_section and category in ['Priority Tasks', 'Later Today']:
                active_tasks.append(task_info)

        i += 1

    return active_tasks

def display_bloom_tasks(tasks):
    """Display Bloom Growth tasks with urgency indicators."""
    if not tasks:
        return False

    print("📋 Bloom Growth Action Items")

    # Sort by days until due
    tasks.sort(key=lambda x: x['days_until'] if x['days_until'] is not None else 999)

    for task in tasks:
        days = task['days_until']

        if days is None:
            urgency = "⏳"
            time_str = "No due date"
        elif days < 0:
            urgency = "❌"
            time_str = f"{abs(days)} day(s) overdue!"
        elif days == 0:
            urgency = "🔴"
            time_str = "DUE TODAY"
        elif days == 1:
            urgency = "🟠"
            time_str = "Due tomorrow"
        elif days <= 3:
            urgency = "🟡"
            time_str = f"Due in {days} days"
        elif days <= 7:
            urgency = "⏳"
            time_str = f"Due in {days} days"
        else:
            urgency = "⏳"
            time_str = f"Due in {days} days"

        print(f"   {urgency} {task['name']}")
        if task['due']:
            print(f"      Due: {task['due']} ({time_str})")
        else:
            print(f"      {time_str}")
        print()

    return True

def display_united_tasks(tasks):
    """Display United tasks with urgency indicators."""
    if not tasks:
        return False

    print("🏢 United Tasks")

    # Sort by category (Priority, Later Today, Next Week)
    category_order = {'Priority Tasks': 0, 'Later Today': 1, 'Next Week': 2}
    tasks.sort(key=lambda x: category_order.get(x.get('category', ''), 999))

    # Track what's been displayed
    displayed_categories = []

    for task in tasks:
        category = task.get('category', 'Unknown')
        days = task.get('days_until')

        # Only show category header once
        if category not in displayed_categories:
            if category == 'Priority Tasks':
                print("\n### Priority Tasks")
            elif category == 'Later Today':
                print("\n### Later Today")
            elif category == 'Next Week':
                print("\n### Next Week")
            displayed_categories.append(category)

        # Due date logic
        if days is not None:
            if days < 0:
                urgency = "❌"
                time_str = f"{abs(days)} day(s) overdue!"
            elif days == 0:
                urgency = "🔴"
                time_str = "DUE TODAY"
            elif days == 1:
                urgency = "🟠"
                time_str = "Due tomorrow"
            elif days <= 3:
                urgency = "🟡"
                time_str = f"Due in {days} days"
            else:
                urgency = "⏳"
                time_str = f"Due in {days} days"
        else:
            urgency = "⏳"
            time_str = "No due date"

        # Task name
        print(f"   {urgency} {task['name']}")
        if task.get('due'):
            print(f"      Due: {task['due']}")
        print()

    return True

def get_credentials(token_file):
    """Load credentials from token file. Returns None on any error."""
    if token_file.exists():
        try:
            creds = Credentials.from_authorized_user_file(token_file)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return creds
        except Exception:
            return None
    return None

def parse_time(time_str):
    """Parse time string to datetime."""
    if 'T' in time_str:
        try:
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            return dt.astimezone()
        except:
            return None
    else:
        try:
            dt = datetime.fromisoformat(time_str)
            dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except:
            return None

def should_filter_event(summary):
    """Check if event should be filtered out (cancelled or personal)."""
    if not summary:
        return False

    summary_lower = summary.lower()

    # Filter out cancelled events (both spellings)
    if 'cancelled' in summary_lower or 'canceled' in summary_lower:
        return True

    # Filter out personal events (conservative list)
    personal_keywords = [
        'doctor', 'dentist', 'medical', 'appointment',
        'personal', 'pharmacy', 'prescription', 'therapy',
        'physical therapy', 'chiropractor', 'optometrist',
        'eye doctor', 'dermatologist', 'specialist'
    ]

    for keyword in personal_keywords:
        if keyword in summary_lower:
            return True

    return False

def should_filter_united_event(summary):
    """Check if United calendar event should be filtered out (personal/non-work)."""
    if not summary:
        return False

    summary_lower = summary.lower()

    # Filter out office hours (already done separately, but keep for completeness)
    if 'office hours' in summary_lower:
        return True

    # Expanded personal keywords for United calendar (more aggressive)
    united_personal_keywords = [
        # Medical
        'doctor', 'dentist', 'medical', 'appointment',
        'pharmacy', 'prescription', 'therapy', 'chiropractor',
        'optometrist', 'eye doctor', 'dermatologist', 'specialist',
        # Personal services
        'hair', 'nail', 'massage', 'spa', 'salon',
        'gym', 'fitness', 'yoga', 'pilates',
        # Family/home
        'school', 'parent-teacher', 'pta', 'school pickup',
        'vet', 'veterinary', 'pet',
        'car service', 'oil change', 'auto repair',
        'real estate', 'inspection', 'contractor',
        # General personal
        'personal', 'lunch', 'break', 'coffee',
        'birthday', 'anniversary', 'holiday',
        'vacation', 'pto', 'day off',
        # Common personal appointment patterns
        'follow-up', 'checkup', 'check-up',
    ]

    for keyword in united_personal_keywords:
        if keyword in summary_lower:
            return True

    # Filter out events that look like "Name: appointment type"
    # Example: "Johanna: Dentist", "Richard: Doctor"
    if ':' in summary:
        parts = summary.split(':', 1)
        if len(parts) == 2:
            # Check if the second part looks like a personal appointment
            after_colon = parts[1].strip().lower()
            for keyword in united_personal_keywords:
                if keyword in after_colon:
                    return True

    return False

def get_all_events(date):
    """Get events from all calendars for a specific date."""
    all_events = []

    for cal_name, cal_id, token_file in CALENDARS:
        creds = get_credentials(token_file)
        if not creds:
            continue

        try:
            service = build('calendar', 'v3', credentials=creds)

            time_min = f"{date}T00:00:00Z"
            time_max = f"{date}T23:59:59Z"

            events_result = service.events().list(
                calendarId=cal_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime',
                maxResults=100
            ).execute()

            events = events_result.get('items', [])

            for event in events:
                summary = event.get('summary', 'No title')

                # Skip filtered events (cancelled, personal, etc.)
                if should_filter_event(summary):
                    continue

                # Skip United calendar events that look like personal/non-work appointments
                if cal_name == 'United' and should_filter_united_event(summary):
                    continue

                start = event.get('start', {})
                end = event.get('end', {})

                if 'dateTime' in start:
                    start_dt = parse_time(start['dateTime'])
                    end_dt = parse_time(end['dateTime'])
                elif 'date' in start:
                    start_dt = parse_time(start['date'])
                    end_dt = parse_time(end['date'])
                else:
                    continue

                if start_dt and end_dt:
                    all_events.append({
                        'calendar': cal_name,
                        'summary': summary,
                        'start': start_dt,
                        'end': end_dt
                    })

        except HttpError as e:
            pass

    all_events.sort(key=lambda x: x['start'])
    return all_events

def check_overlaps(events):
    """Check for overlapping events and mark them."""
    if not events:
        return []

    n = len(events)
    overlaps = [False] * n

    for i in range(n):
        for j in range(i + 1, n):
            e1 = events[i]
            e2 = events[j]

            e1_start = e1['start'].astimezone(timezone.utc)
            e1_end = e1['end'].astimezone(timezone.utc)
            e2_start = e2['start'].astimezone(timezone.utc)
            e2_end = e2['end'].astimezone(timezone.utc)

            e1_duration = (e1_end - e1_start).total_seconds() / 3600
            e2_duration = (e2_end - e2_start).total_seconds() / 3600
            is_e1_all_day = (e1_duration >= 20)
            is_e2_all_day = (e2_duration >= 20)

            if is_e1_all_day != is_e2_all_day:
                continue

            if max(e1_start, e2_start) < min(e1_end, e2_end):
                overlaps[i] = True
                overlaps[j] = True

    return overlaps

def format_events(events, overlaps):
    """Format events for display."""
    if not events:
        print("No events found.")
        return

    seen = {}
    deduped_events = []
    deduped_overlaps = []

    for i, event in enumerate(events):
        if (event['start'].hour == 0 and event['start'].minute == 0 and
            (event['end'] - event['start']).days >= 1):
            key = (event['summary'], event['start'].date())
            if key in seen:
                continue
            seen[key] = i

        deduped_events.append(event)
        deduped_overlaps.append(overlaps[i])

    for i, event in enumerate(deduped_events):
        cal_name = event['calendar']
        summary = event['summary']
        start = event['start']
        end = event['end']

        if (start.hour == 0 and start.minute == 0 and
            (end - start).days >= 1):
            time_str = "All Day"
        else:
            time_str = f"{start.strftime('%-I:%M %p')} — {end.strftime('%-I:%M %p')}"

        if deduped_overlaps[i]:
            prefix = "⚠️  "
        else:
            prefix = "✅ "

        print(f"{prefix}{time_str}")
        print(f"   {summary}")
        print(f"   [{cal_name}]")
        print()

def main():
    # Parse command line args
    target_day = 'today'
    if len(sys.argv) > 1:
        target_day = sys.argv[1].lower()

    # Determine date
    if target_day == 'tomorrow':
        date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        day_name = "Tomorrow"
    else:
        date = datetime.now().strftime('%Y-%m-%d')
        day_name = "Today"

    print(f"📅 {day_name}'s Schedule: {date}")
    print()

    # Get and display weather (only for today, not tomorrow)
    if target_day == 'today':
        weather = get_weather()
        if weather:
            print(weather)
            print()

        # Display backup status (only for today)
        backup_status = get_backup_status()
        if backup_status:
            print(backup_status)
            print()

        # Display Bloom Growth tasks (only for today)
        bloom_tasks = get_bloom_tasks()
        if bloom_tasks:
            display_bloom_tasks(bloom_tasks)

        # Display United tasks (only for today)
        united_tasks = get_united_tasks()
        if united_tasks:
            display_united_tasks(united_tasks)

    try:
        events = get_all_events(date)
        overlaps = check_overlaps(events)
    except Exception:
        events = []
        overlaps = []

    if events:
        has_overlap = any(overlaps)
        if has_overlap:
            print("⚠️  TIME CONFLICTS DETECTED")
            print()
        else:
            print("✅ No conflicts today")
            print()
        print()

        format_events(events, overlaps)
    else:
        print("No events found.")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Extract action items from Bloom Growth emails and update task tracking.

This script:
1. Fetches the most recent Bloom Growth email mentioning Richard
2. Parses action items assigned to Richard
3. Updates tasks/bloom-tasks.md with current tasks
4. Alerts if tasks are due within 3 days
"""

import re
from pathlib import Path
from datetime import datetime, timedelta
from html import unescape

# Import Gmail helper
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from gmail import get_service

# Paths
WORKSPACE = Path(__file__).parent.parent.parent
TASK_FILE = WORKSPACE / 'tasks' / 'bloom-tasks.md'

# Alert threshold in days
ALERT_THRESHOLD_DAYS = 3

def get_most_recent_task_email():
    """Fetch the most recent Bloom Growth email that mentions Richard."""
    service = get_service()
    if not service:
        return None

    try:
        # Search for Bloom Growth emails mentioning Richard, get the most recent
        results = service.users().messages().list(
            userId='me',
            q='from:bloomgrowth.com Whitaker',
            maxResults=10
        ).execute()

        messages = results.get('messages', [])
        if not messages:
            return None

        # Get the most recent message
        msg_id = messages[0]['id']
        msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        return msg
    except Exception as e:
        print(f"Error fetching Bloom Growth email: {e}")
        return None

def extract_body(payload):
    """Extract email body from Gmail message payload."""
    if 'parts' in payload:
        for part in payload['parts']:
            body = extract_body(part)
            if body:
                return body
    else:
        if payload.get('body', {}).get('data'):
            import base64
            data = payload['body']['data']
            return base64.urlsafe_b64decode(data).decode('utf-8')
    return None

def parse_action_items(msg_body, email_date):
    """
    Parse action items from Bloom Growth email.

    Returns list of dicts: {task, assignee, due_date, email_date}
    """
    # Clean HTML
    clean_text = unescape(re.sub(r'<[^>]+>', '\n', msg_body))
    lines = [l.strip() for l in clean_text.split('\n') if l.strip()]

    # Find action items
    action_items = []

    for i, line in enumerate(lines):
        # Look for assignee names followed by tasks (usually starting with •)
        if line and not line.startswith('•') and i + 1 < len(lines):
            next_line = lines[i + 1]

            # Check if next line is a task (starts with bullet and has content)
            if next_line.startswith('•') and len(next_line) > 15:
                assignee = line
                task = next_line.replace('•', '').strip()

                # Look for due date in next few lines
                due_date = None
                for j in range(i + 2, min(i + 6, len(lines)):
                    if re.match(r'\d{1,2}/\d{1,2}/\d{4}', lines[j]):
                        due_date = lines[j]
                        break

                action_items.append({
                    'task': task,
                    'assignee': assignee,
                    'due_date': due_date,
                    'email_date': email_date
                })

    return action_items

def get_email_date(headers):
    """Parse email date from headers."""
    for header in headers:
        if header['name'] == 'Date':
            # Parse date like "Wed, 04 Mar 2026 17:00:13 +0000"
            date_str = header['value']
            try:
                # Extract date portion
                match = re.search(r'\d{2} \w{3} \d{4}', date_str)
                if match:
                    return datetime.strptime(match.group(), '%d %b %Y').strftime('%Y-%m-%d')
            except:
                pass
    return datetime.now().strftime('%Y-%m-%d')

def update_tasks_file(richard_tasks, msg_date):
    """Update tasks/bloom-tasks.md with Richard's active tasks, respecting completed items."""

    existing_content = TASK_FILE.read_text() if TASK_FILE.exists() else ""
    header_section = existing_content.split('## Active Tasks')[0] if '## Active Tasks' in existing_content else ""
    
    # Parse existing completed tasks from file
    completed_tasks_text = ""
    existing_completed_task_names = set()
    if '## Completed Tasks' in existing_content:
        completed_start = existing_content.find('## Completed Tasks')
        archive_start = existing_content.find('## Archive')
        
        if archive_start != -1 and archive_start > completed_start:
            completed_tasks_text = existing_content[completed_start:archive_start]
        else:
            completed_tasks_text = existing_content[completed_start:]
        
        # Extract task names from completed section
        for line in completed_tasks_text.split('\n'):
            match = re.match(r'###\s*(.*)', line)
            if match:
                existing_completed_task_names.add(match.group(1).strip())

    # Filter incoming tasks: only keep tasks not already marked as completed
    truly_active_tasks = [
        task for task in richard_tasks
        if task['task'].strip() not in existing_completed_task_names
    ]

    # Build new Active Tasks section
    now = datetime.now().strftime('%Y-%m-%d')
    new_header = header_section.replace('{date}', now) if '{date}' in header_section else header_section

    active_section = "## Active Tasks\n\n"
    if not truly_active_tasks:
        active_section += "*No active tasks assigned to Richard*\n\n"
    else:
        for task in truly_active_tasks:
            # Format task info
            due_str = task['due_date'] or 'No due date'
            status_line = f"""### {task['task']}
- **Assigned to:** Richard Whitaker
- **Due:** {due_str}
- **Source:** Bloom Growth email ({task['email_date']})
- **Status:** ⏳ Active

"""
            active_section += status_line

    # Reconstruct the full content with proper ordering
    # Header -> Active -> Completed -> Archive
    # But preserve any pre-existing content before ## Active Tasks
    pre_active_start = existing_content.find('## Active Tasks')
    
    if pre_active_start != -1:
        # Keep everything before Active Tasks
        pre_content = existing_content[:pre_active_start]
        final_content = pre_content + new_header + active_section
    else:
        final_content = new_header + active_section
    
    # Append existing Completed and Archive sections
    if '## Completed Tasks' in existing_content:
        completed_start = existing_content.find('## Completed Tasks')
        final_content += existing_content[completed_start:]
    else:
        final_content += """## Completed Tasks

*No completed tasks yet*

---

## Archive

*No archived items yet*
"""

    # Write the updated file
    TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    TASK_FILE.write_text(final_content)

    return len(truly_active_tasks), truly_active_tasks

def check_due_dates(richard_tasks):
    """Check if any tasks are due soon or overdue and return alerts."""
    alerts = []
    now = datetime.now()
    
    for task in richard_tasks:
        if not task['due_date']:
            continue

        try:
            due_date = datetime.strptime(task['due_date'], '%m/%d/%Y')
            days_until_due = (due_date - now).days

            # Only alert on tasks that are approaching (within ALERT_THRESHOLD_DAYS)
            # Do NOT alert on overdue tasks (negative days)
            if 0 <= days_until_due <= ALERT_THRESHOLD_DAYS:
                urgency = "📋" if days_until_due > 1 else "🚨"
                alerts.append({
                    'task': task['task'],
                    'due_date': task['due_date'],
                    'days_until': days_until_due,
                    'urgency': urgency
                })
        except ValueError:
            # Invalid date format
            pass

    return alerts

def main():
    """Main function."""
    print("Checking Bloom Growth emails for Richard's action items...")

    # Fetch the most recent Bloom Growth email mentioning Richard
    msg = get_most_recent_task_email()
    if not msg:
        print("No Bloom Growth emails found.")
        return

    # Extract body and parse action items
    body = extract_body(msg['payload'])
    if not body:
        print("Could not extract email body.")
        return

    email_date = get_email_date(msg['payload']['headers'])
    action_items = parse_action_items(body, email_date)

    # Filter for Richard's tasks only
    richard_tasks = [
        item for item in action_items
        if 'Richard' in item['assignee'] and 'Whitaker' in item['assignee']
    ]

    if not richard_tasks:
        print("No active tasks assigned to Richard found.")
        return

    # Update tasks file
    count, truly_active_tasks = update_tasks_file(richard_tasks, email_date)

    print(f"✓ Updated {count} active task(s) for Richard in tasks/bloom-tasks.md")

    # Check for approaching due dates (only on truly active tasks)
    alerts = check_due_dates(truly_active_tasks)
    if alerts:
        print("\n🚨 Upcoming due dates:")
        for alert in alerts:
            time_str = "TODAY" if alert['days_until'] == 0 else f"{alert['days_until']} day(s)"
            print(f"  {alert['urgency']} {alert['task']}")
            print(f"     Due: {alert['due_date']} ({time_str})")
        print("\nThese tasks should be prioritized!")

    # Print summary
    if not alerts:
        print("\nCurrent tasks:")
        for task in truly_active_tasks:
            print(f"  • {task['task']}")
            if task['due_date']:
                print(f"    Due: {task['due_date']}")

if __name__ == '__main__':
    main()

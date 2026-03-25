#!/home/rwhitaker/.openclaw/workspace/skills/google-calendar/venv/bin/python3
"""
Extract action items from Bloom Growth emails and update task tracking.

This script:
1. Fetches most recent Bloom Growth email mentioning Richard
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
    """Fetches most recent Bloom Growth email that mentions Richard."""
    service = get_service()
    if not service:
        return None

    try:
        # Search for Bloom Growth emails mentioning Richard, get most recent
        results = service.users().messages().list(
            userId='me',
            q='from:bloomgrowth.com Whitaker',
            maxResults=10
        ).execute()

        messages = results.get('messages', [])
        if not messages:
            return None

        # Get most recent message
        msg_id = messages[0]['id']
        msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        return msg
    except Exception as e:
        print(f"Error fetching Bloom Growth email: {e}")
        return None

def extract_body(payload):
    """Extracts email body from Gmail message payload."""
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

def extract_due_date(line, start_idx):
    """Extracts due date from a line at or after start_idx.
    
    Looks at lines[start_idx:start_idx+6] for pattern MM/DD/YYYY.
    Returns: (due_date, new_idx) or (None, start_idx)
    """
    for j in range(start_idx + 2, min(start_idx + 6, len(line_lines))):
        match = re.match(r'\d{1,2}/\d{1,2}/\d{4}', line_lines[j])
        if match:
            return match.group(), start_idx + j
    return None, start_idx

def extract_status_info(next_line, line_lines, current_idx):
    """
    Extracts task name and status from next_line or surrounding lines.
    
    Returns: (task_name, status)
    """
    task_name = None
    status = '⏳ Active'  # Default
    
    # Case 1: Header line with ### task name
    if next_line.startswith('###'):
        task_name = re.sub(r'^###\s*', '', next_line).strip()
        return task_name, status
    
    # Case 2: Status: line with status
    if 'Status:' in next_line:
        # Extract task name (everything before Status:)
        task_name = next_line.split('Status:')[0].strip()
        # Get status from next line (should be on same line or next few lines)
        # Look at next_line and up to 5 lines ahead for status
        for offset in range(6):
            if current_idx + offset < len(line_lines):
                check_line = line_lines[current_idx + offset]
                if check_line.strip() and (
                    'Status:' in check_line or 
                    'status' in check_line.lower()
                ):
                    status_lower = check_line.lower()
                    if 'completed' in status_lower or 'completed (' in status_lower:
                        status = '✅ Completed'
                    else:
                        status = '⏳ Active'
                    break
        return task_name, status
    
    # Case 3: Just a task line (bullet point)
    task_name = None
    status = '⏳ Active'  # Default
    
    if next_line.startswith('•') and len(next_line) > 15:
        task_name = next_line.replace('•', '').strip()
        return task_name, status
    
    return task_name, status

def parse_action_items(msg_body, email_date):
    """
    Parses action items from Bloom Growth email.

    Returns list of dicts: {task, assignee, due_date, email_date, status}
    """
    # Clean HTML
    clean_text = unescape(re.sub(r'<[^>]+>', '\n', msg_body))
    line_lines = [l.strip() for l in clean_text.split('\n') if l.strip()]

    # Find action items
    action_items = []

    for i, line in enumerate(line_lines):
        # Look for assignee names followed by tasks (usually starting with •)
        if line and not line.startswith('•') and i + 1 < len(line_lines):
            next_line = line_lines[i + 1]

            # Check if next line is a task (starts with bullet and has content)
            if next_line.startswith('•') and len(next_line) > 15:
                assignee = line
                task_name = next_line.replace('•', '').strip()
                
                # Look for due date in next few lines
                due_date, new_idx = extract_due_date(line_lines, i)
                if new_idx is None:
                    # No due date found
                    new_idx = i + 6  # Advance past this section
                    status = '⏳ Active'
                else:
                    # Found due date, now check status
                    task_name, status = extract_status_info(next_line, line_lines, new_idx)
                
                if task_name:
                    action_items.append({
                        'task': task_name,
                        'assignee': assignee,
                        'due_date': due_date,
                        'email_date': email_date,
                        'status': status
                    })
        
        return action_items

def get_email_date(headers):
    """Parses email date from headers."""
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
    """Updates tasks/bloom-tasks.md with Richard's active tasks, respecting completed items."""

    existing_content = TASK_FILE.read_text() if TASK_FILE.exists() else ""
    
    # Parse existing completed tasks from file
    completed_tasks_text = ""
    existing_completed_task_names = set()
    existing_completed_tasks_with_status = {}  # Map task names to their statuses
    
    if '## Completed Tasks' in existing_content:
        completed_start = existing_content.find('## Completed Tasks')
        archive_start = existing_content.find('## Archive')
        
        if archive_start != -1 and archive_start > completed_start:
            completed_tasks_text = existing_content[completed_start:archive_start]
        else:
            completed_tasks_text = existing_content[completed_start:]
        
        # Extract task names AND statuses from completed section
        for line in completed_tasks_text.split('\n'):
            # Match patterns like:
            # - "### Task Name"
            # - "- Status: Completed"
            # - "- Status: Active"
            match = re.match(r'^###\s*(.+?)\s*$', line)
            if match:
                task_name = match.group(1).strip()
                existing_completed_task_names.add(task_name)
                # Default to completed if no status found
                existing_completed_tasks_with_status[task_name] = '✅ Completed'
            
            # Also look for standalone Status lines with task names
            status_match = re.match(r'^-\s*Status:\s*(.*?)\s*$', line)
            if status_match:
                task_name = status_match.group(1).strip()
                if task_name:
                    existing_completed_task_names.add(task_name)
                    # Extract status indicator
                    remaining = status_match.group(2).strip() if status_match.group(2) else ''
                    status_lower = remaining.lower()
                    if 'completed' in status_lower or 'completed (' in status_lower:
                        status = '✅ Completed'
                    else:
                        status = '⏳ Active'
                    existing_completed_tasks_with_status[task_name] = status

    # Filter incoming tasks: only keep tasks not already marked as completed
    truly_active_tasks = [
        task for task in richard_tasks
        if task['task'].strip() not in existing_completed_task_names
    ]

    # Build new Active Tasks section
    now = datetime.now().strftime('%Y-%m-%d')
    header = f"""# Bloom Growth Action Items

_Last updated: {now}

"""

    active_section = "## Active Tasks\n\n"
    if not truly_active_tasks:
        active_section += "*No active tasks assigned to Richard*\n\n"
    else:
        for task in truly_active_tasks:
            # Format task info
            due_str = task['due_date'] or 'No due date'
            status_display = task.get('status', '⏳ Active')
            
            active_section += f"""### {task['task']}
- **Assigned to:** Richard Whitaker
- **Due:** {due_str}
- **Source:** Bloom Growth email ({task['email_date']})
- **Status:** {status_display}

"""

    # Reconstruct full content with proper ordering
    final_content = header + active_section
    
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

    # Write updated file
    TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    TASK_FILE.write_text(final_content)

    return len(truly_active_tasks), truly_active_tasks

def check_due_dates(richard_tasks):
    """Checks if any tasks are due soon or overdue and returns alerts."""
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
            # Also check if task is not completed (has Active status)
            task_status = task.get('status', '')
            is_completed = 'Completed' in task_status or task_status == '✅ Completed'
            
            if 0 <= days_until_due <= ALERT_THRESHOLD_DAYS and not is_completed:
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

    # Fetch most recent Bloom Growth email mentioning Richard
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

#!/usr/bin/env python3
"""
Job Rejection Workflow
Sends rejection email via personal Gmail and labels original message as JOB RESPONDED
"""

import sys
from pathlib import Path

# Add skill directory to path
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / 'skills' / 'gmail-personal'))

from gmail import (
    send_email,
    add_labels,
    mark_as_read,
    get_message_by_id,
    get_label_id
)

JOB_RESPONDED_LABEL = 'JOB RESPONDED'

def send_rejection(original_message_id: str, to_email: str, original_subject: str):
    """Send rejection email and label original message as JOB RESPONDED.

    Args:
        original_message_id: Gmail message ID of original email
        to_email: Recipient email address
        original_subject: Original email subject (for reply)
    """
    # Read template
    template_path = Path.home() / '.openclaw' / 'workspace' / 'templates' / 'job-reject-reply.txt'
    with open(template_path, 'r') as f:
        template = f.read()

    # Send rejection via personal Gmail
    reply_subject = f"Re: {original_subject}"

    print(f"📤 Sending rejection to {to_email}...")
    send_email(
        to=to_email,
        subject=reply_subject,
        body=template
    )
    print("✅ Email sent from richwhit@gmail.com")

    # Label original message as JOB RESPONDED
    print(f"🏷️ Labeling original message as JOB RESPONDED...")
    job_responded_label_id = get_label_id(JOB_RESPONDED_LABEL)

    if job_responded_label_id:
        add_labels(original_message_id, [job_responded_label_id])
        print("✅ Original message labeled as JOB RESPONDED")
    else:
        print("⚠️ JOB RESPONDED label not found - you may need to create it")

    # Mark as read
    mark_as_read(original_message_id)
    print("✅ Original message marked as read")

    print("\n✅ Job rejection complete")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: job_reject.py <message-id> <to-email> <original-subject>")
        print("Example: job_reject.py '12345' 'recruiter@example.com' 'Subject Line'")
        sys.exit(1)

    original_message_id = sys.argv[1]
    to_email = sys.argv[2]
    original_subject = sys.argv[3]

    send_rejection(original_message_id, to_email, original_subject)

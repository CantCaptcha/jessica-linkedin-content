#!/usr/bin/env python3
"""
Send email with attachment using Richard's personal Gmail
"""

import sys
sys.path.insert(0, '/home/rwhitaker/.openclaw/workspace/skills/gmail-personal/venv/lib/python3.12/site-packages')

import subprocess

# Read Excel file
excel_path = '/home/rwhitaker/.openclaw/workspace/NIST-CMMC-Artifacts-by-Level.xlsx'

with open(excel_path, 'rb') as f:
    excel_content = f.read()

# Read Excel content as text for reference
with open(excel_path, 'rb') as f:
    import base64
    excel_base64 = base64.b64encode(f.read()).decode()

# Create email body with attachment info
body = f'''Hi Jessica,

Attached is the NIST-CMMC Artifacts spreadsheet organized by Level 1 and Level 2.

This Excel file contains:
- Overview (Level summaries & timelines)
- Domain Comparison (controls per domain)
- Level 1 Artifacts (17 controls with recommended evidence)
- Level 2 Artifacts (72 controls with recommended evidence)
- Critical Documents (required at each level with priorities)
- Implementation Roadmap (11 phases with timelines)

File Details:
- Filename: NIST-CMMC-Artifacts-by-Level.xlsx
- Size: 6.5KB
- Created: 2026-03-31

The spreadsheet was created from the DCG CMMC Tracking file and includes comprehensive artifact recommendations for CMMC/NIST 800-171 compliance.

Let me know if you have any questions or need help with specific controls!

Best,
Stevie
'''

# Create Gmail API message with attachment
import json

# Construct the message with attachment
message = {
    "raw": f'''From: Richard Whitaker <richwhit@gmail.com>
To: Jessica Allen <jessica.allen@cybersecgru.com>
Subject: NIST-CMMC Artifacts by Level (Excel Spreadsheet)
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="===============boundary=="

--===============boundary==
Content-Type: text/plain; charset="utf-8"

{body}

--===============boundary==
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="NIST-CMMC-Artifacts-by-Level.xlsx"

{excel_base64}
--===============boundary==--
'''
}

# Save message to file
with open('/tmp/gmail_message.json', 'w') as f:
    json.dump(message, f)

# Send using Gmail API with raw message
result = subprocess.run([
    '/home/rwhitaker/.openclaw/workspace/skills/gmail-personal/venv/bin/python3',
    '-c',
    '''
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

# Load credentials
creds = Credentials.from_authorized_user_file('/home/rwhitaker/.openclaw/workspace/skills/gmail-personal/config/token.json')

# Build service
service = build('gmail', 'v1', credentials=creds)

# Read message
with open('/tmp/gmail_message.json', 'r') as f:
    message = json.load(f)

# Send
result = service.users().messages().send(
    userId="me",
    body=message
).execute()

print(f"Message ID: {{result.get('id')}}")
print("✅ Email sent with attachment!")
'''
], capture_output=True, text=True)

print(result.stdout)
print(result.stderr)

if result.returncode == 0:
    print("✅ Email sent successfully from Richard's personal Gmail with attachment!")
else:
    print(f"❌ Error sending email. Return code: {result.returncode}")

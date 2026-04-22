#!/usr/bin/env python3
"""
Send email with attachment using Gmail API
"""

import sys
sys.path.insert(0, '/home/rwhitaker/.openclaw/workspace/skills/gmail-personal/venv/lib/python3.12/site-packages')

import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load credentials
creds = Credentials.from_authorized_user_file('/home/rwhitaker/.openclaw/workspace/skills/gmail-personal/config/token.json')

# Build service
service = build('gmail', 'v1', credentials=creds)

# Read Excel file
excel_path = '/home/rwhitaker/.openclaw/workspace/NIST-CMMC-Artifacts-by-Level.xlsx'
with open(excel_path, 'rb') as f:
    excel_content = f.read()
    excel_base64 = base64.b64encode(excel_content).decode()

# Email body
body = '''Hi Jessica,

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

# Create message with attachment
message = {
    'raw': f'''From: Richard Whitaker <richwhit@gmail.com>
To: Jessica Allen <jessica.allen@cybersecgru.com>
Subject: NIST-CMMC Artifacts by Level (Excel Spreadsheet)
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="===============1234567890=="

--===============1234567890==
Content-Type: text/plain; charset="utf-8"

{body}

--===============1234567890==
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="NIST-CMMC-Artifacts-by-Level.xlsx"

{excel_base64}
--===============1234567890==--
'''
}

try:
    result = service.users().messages().send(userId='me', body=message).execute()
    print(f"✅ Email sent successfully!")
    print(f"Message ID: {result.get('id')}")
    print("File attached: NIST-CMMC-Artifacts-by-Level.xlsx")
except HttpError as error:
    print(f"❌ Error sending email: {error}")
    print(f"Details: {error}")
    sys.exit(1)

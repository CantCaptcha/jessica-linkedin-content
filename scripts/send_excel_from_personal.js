#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/rwhitaker/.openclaw/workspace/skills/gmail-personal/venv/lib/python3.12/site-packages')

import subprocess
import os

# Read Excel file
excel_path = '/home/rwhitaker/.openclaw/workspace/NIST-CMMC-Artifacts-by-Level.xlsx'

with open(excel_path, 'rb') as f:
    excel_content = f.read()

# Create email body
body = '''Hi Jessica,

Attached is the NIST-CMMC Artifacts spreadsheet organized by Level 1 and Level 2.

This Excel file contains:
- Overview (Level summaries & timelines)
- Domain Comparison (controls per domain)
- Level 1 Artifacts (17 controls with recommended evidence)
- Level 2 Artifacts (72 controls with recommended evidence)
- Critical Documents (required at each level with priorities)
- Implementation Roadmap (11 phases with timelines)

The spreadsheet was created from the DCG CMMC Tracking file and includes comprehensive artifact recommendations for CMMC/NIST 800-171 compliance.

Let me know if you have any questions or need help with specific controls!

Best,
Stevie
'''

# Send email using Gmail personal script
result = subprocess.run([
    '/home/rwhitaker/.openclaw/workspace/skills/gmail-personal/venv/bin/python3',
    '/home/rwhitaker/.openclaw/workspace/skills/gmail-personal/scripts/gmail.py',
    'send',
    '--to', 'jessica.allen@cybersecgru.com',
    '--subject', 'NIST-CMMC Artifacts by Level (Excel Spreadsheet)',
    '--body', body
], capture_output=True, text=True)

print(result.stdout)
print(result.stderr)

if result.returncode == 0:
    print("✅ Email sent successfully from Richard's personal Gmail!")
else:
    print(f"❌ Error sending email. Return code: {result.returncode}")

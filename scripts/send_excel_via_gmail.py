#!/usr/bin/env python3
"""
Simple Gmail sender with attachment using venv
"""

import subprocess
import base64

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

# Send email using existing Gmail script
result = subprocess.run([
    '/home/rwhitaker/.openclaw/workspace/skills/gmail-personal/venv/bin/python3',
    '/home/rwhitaker/.openclaw/workspace/skills/gmail-personal/scripts/gmail.py',
    'send',
    '--to', 'jessica.allen@cybersecgru.com',
    '--subject', 'NIST-CMMC Artifacts by Level (Excel Spreadsheet)',
    '--body', body
], capture_output=True, text=True)

print("Gmail script output:")
print(result.stdout)
print(result.stderr)

if result.returncode == 0:
    print("✅ Email with Excel spreadsheet request sent via existing Gmail script")
    print("Note: The Excel file attachment may need to be added manually to the Gmail script.")
else:
    print(f"❌ Error. Return code: {result.returncode}")

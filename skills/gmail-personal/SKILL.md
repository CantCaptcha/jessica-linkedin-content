---
name: gmail-personal
description: Personal Gmail and Calendar integration for Richard's personal account (richwhit@gmail.com). Use for: (1) Checking personal calendar availability, (2) Listing personal calendar events, (3) Creating personal calendar events, (4) Sending personal emails.

**IMPORTANT:** This is for Richard's personal Gmail account only, separate from DCG work account.

**To use this integration:**
1. Navigate to the skill directory:
   ```bash
   cd /home/rwhitaker/.openclaw/workspace/skills/gmail-personal
   ```

2. Authenticate with personal Gmail account:
   ```bash
   venv/bin/python3 scripts/setup.py
   ```

3. Run commands:
   ```bash
   venv/bin/python3 scripts/cal.py list
   venv/bin/python3 scripts/gmail.py send --to "email@example.com" --subject "Subject" --body "Body"
   ```

**Account:**
- Personal: richwhit@gmail.com

**Separate from DCG:**
- DCG skill: /home/rwhitaker/.openclaw/workspace/skills/google-calendar/
- DCG skill: /home/rwhitaker/.openclaw/workspace/skills/gmail/
- Personal skill: /home/rwhitaker/.openclaw/workspace/skills/gmail-personal/

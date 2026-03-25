---
name: google-calendar
description: Google Calendar integration for reading events, checking free/busy availability, and creating/managing calendar events. Use when the user asks to: (1) Check calendar availability or "when is Richard free", (2) List, view, or summarize calendar events, (3) Schedule meetings or create events, (4) Check for scheduling conflicts, (5) Help others book time with the user, (6) Any task involving Google Calendar access or management.

**IMPORTANT: This skill requires access to workspace at /home/rwhitaker/.openclaw/workspace/skills/google-calendar/**

**To use this calendar integration:**
1. Navigate to the skill directory first:
   ```bash
   cd /home/rwhitaker/.openclaw/workspace/skills/google-calendar
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Run calendar commands using venv python:
   ```bash
   venv/bin/python3 scripts/cal.py list
   venv/bin/python3 scripts/cal.py freebusy --from "2026-02-10 09:00" --to "2026-02-10 18:00"
   ```

**Configuration files:**
- Credentials: config/credentials.json (OAuth client credentials)
- Token: config/token.json (Authenticated access tokens - DO NOT COMMIT)

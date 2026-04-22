# Morning calendar display (AUTO: Every 6am via crontab)
# - Script: /home/rwhitaker/.openclaw/workspace/scripts/morning.sh
# - Shows today's schedule including:
#   * Local weather (Union, KY)
#   * Backup status (success/failure of last 3 AM backup)
#   * Bloom Growth action items with urgency indicators
#   * Both DCG and United calendars
#   * Highlights overlapping events
#   * Filters out personal events and cancelled items
# - Runs automatically at 6 AM daily via cron
# - Available manually: ./scripts/morning.sh today or ./scripts/morning.sh tomorrow

# Check AgentMail inbox for replies (AUTO: Every 30 mins via cron)
# - Cron job: "AgentMail Auto-Responder" (runs every 30 minutes)
# - Script: /home/rwhitaker/.openclaw/workspace/scripts/agentmail_autorespond.js
# - Monitors stevieai@agentmail.to for unread received messages
# - Auto-response rules:
#   * Polite greeting (minimal, from Stevie)
#   * Confirm meeting if valid time-slot in reply
#   * NEVER exceeds what Richard would reply (simple acknowledgement only)
# - Manual check still available: /home/rwhitaker/.openclaw/workspace/scripts/check-agentmail.sh

# Check calendar for travel events (AUTO: Daily at 6 AM via crontab)
# - Script: /home/rwhitaker/.openclaw/workspace/scripts/check-travel-events.py
# - Checks both DCG and United calendars for travel keywords
# - Travel keywords: travel, trip, flight, airport, fly, flying, vacation, holiday, departure, arrival, hotel, airbnb
# - Displays travel events for next 7 days

# Check for late-night work events on United calendar (AUTO: Daily at 9 PM EDT via crontab)
# - Events after 9 PM (after 21:00)
# - Keywords: "outage", "maintenance", "change", "Help Hub"
# - Alert 1 hour before event starts
# - Send Discord notification to #bot channel
# - Runs automatically daily at 9 PM via cron

# Bloom Growth task tracking (PAUSED - OAuth broken)
# - Run: /home/rwhitaker/.openclaw/workspace/skills/gmail/venv/bin/python3 scripts/check_bloom_tasks.py
# - Updates: tasks/bloom-tasks.md with active tasks
# - Proactively alert if tasks are due within 3 days
# - Requires DCG OAuth client (deleted for security)

# LinkedIn topic reminder for Jessica Allen (check Thursday mornings around 9am ET)
# - Send topic suggestion to #bot channel for her weekly LinkedIn post
# - Topics should focus on board positioning: leadership, strategy, hiring, ops learnings
# - Goal: Position her as a board-ready COO for startup/tech companies
# - Workflow: Topic → Jessica's paragraph → Draft post → Review → Post Tuesday morning

## HEARTBEAT FLOW

**IMPORTANT - Time-based heartbeat checks:**
- Only run checks at these times (EST): **6:00 AM, 12:00 PM, 5:00 PM**
- At all other times, reply HEARTBEAT_OK immediately without running checks
- This reduces redundant notifications while maintaining coverage

When Stevie receives a heartbeat poll:
1. Check current time - if NOT 6am/noon/5pm, reply HEARTBEAT_OK immediately
2. If AT 6am/noon/5pm:
   a. Read HEARTBEAT.md for checklist
   b. Rotate through checks (2-4 per heartbeat)
   c. If anything needs attention, send alert to Discord #Richard (channel ID: 1488952869603377243)
   d. If nothing needs attention, reply HEARTBEAT_OK

**IMPORTANT CALENDAR RULE:**
- ALWAYS use `/home/rwhitaker/.openclaw/workspace/scripts/morning-calendar.py` for calendar checks
- NEVER use `cal.py list` directly - it only checks primary calendar
- The morning-calendar.py script shows BOTH DCG and United calendars with conflict detection

**INBOX CHECK RULE:**
- Include "Notable in Inbox" section in ALL heartbeats (AM and PM)
- Check AgentMail only (DCG Gmail check paused - OAuth client deleted)
- List count of unread AgentMail messages and highlight anything needing attention

**DISCORD CHANNEL:**
- Send all heartbeat alerts to #Richard channel (ID: 1488952869603377243)
- #bot channel (ID: 1469388583239680136) is still available for others to interact

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

# Check for JOB REJECT messages in personal Gmail (check daily)
# - Run: /home/rwhitaker/.openclaw/workspace/scripts/check-job-rejects.sh
# - Replies to JOB REJECT messages without JOB RESPONDED label (last 10 days only)
# - Template declines positions requiring onsite outside KY/Cincinnati or not 100% remote
# - Alerts if new job rejects were replied to

# Check AgentMail inbox for replies (AUTO: Every 30 mins via cron)
# - Cron job: "AgentMail Auto-Responder" (runs every 30 minutes)
# - Script: /home/rwhitaker/.openclaw/workspace/scripts/agentmail_autorespond.js
# - Monitors stevieai@agentmail.to for unread received messages
# - Auto-response rules:
#   * Polite greeting (minimal, from Stevie)
#   * Confirm meeting if valid time-slot in reply
#   * NEVER exceeds what Richard would reply (simple acknowledgement only)
# - Manual check still available: /home/rwhitaker/.openclaw/workspace/scripts/check-agentmail.sh

# Check calendar for travel events (check daily)

# Check for late-night work events on United calendar (check every hour during day)
# - Events after 9 PM (after 21:00)
# - Keywords: "outage", "maintenance", "change", "Help Hub"
# - Alert 1 hour before event starts
# - Send Discord notification to #bot channel

# Check Bloom Growth emails for action items assigned to Richard (check daily)
# - Run: cd /home/rwhitaker/.openclaw/workspace/skills/gmail && venv/bin/python3 scripts/check_bloom_tasks.py
# - Updates: tasks/bloom-tasks.md with active tasks
# - Proactively alert if tasks are due within 3 days

# Check for JOB REJECT messages in personal Gmail (check daily)
# - Run: /home/rwhitaker/.openclaw/workspace/scripts/check-job-rejects.sh
# - Replies to JOB REJECT messages without JOB RESPONDED label (last 10 days only)
# - Template declines positions requiring onsite outside KY/Cincinnati or not 100% remote
# - Alerts if new job rejects were replied to

# LinkedIn topic reminder for Jessica Allen (check Thursday mornings around 9am ET)
# - Send topic suggestion to #bot channel for her weekly LinkedIn post
# - Topics should focus on board positioning: leadership, strategy, hiring, ops learnings
# - Goal: Position her as a board-ready COO for startup/tech companies
# - Workflow: Topic → Jessica's paragraph → Draft post → Review → Post Tuesday morning

## HEARTBEAT FLOW

When Stevie receives a heartbeat poll:
1. Read HEARTBEAT.md for checklist
2. Rotate through checks (2-4 per heartbeat):
   - AgentMail unread (auto via cron already)
   - DCG email alerts (auto via cron already)
   - Bloom Growth tasks (auto via cron already)
   - Late-night work events (auto via cron already)
   - Travel events (check daily)
   - JOB REJECT messages (check daily)
3. If anything needs attention, send alert to Discord #bot
4. If nothing needs attention, reply HEARTBEAT_OK

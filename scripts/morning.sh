#!/bin/bash
# Morning calendar check - shows all calendars with conflict highlighting
# Usage: ./morning.sh [today|tomorrow]

DAY=${1:-today}
/home/rwhitaker/.openclaw/workspace/skills/google-calendar/venv/bin/python3 /home/rwhitaker/.openclaw/workspace/scripts/morning-calendar.py "$DAY"

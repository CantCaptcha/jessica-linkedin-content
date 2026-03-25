#!/bin/bash
# Check for JOB REJECT messages and smart auto-reply

# This script now uses SMART processing that:
# 1. Parses job details from each email
# 2. Declines ONLY if position violates preferences:
#    - Requires onsite outside KY/Cincinnati
#    - AND is NOT 100% remote
# 3. Acknowledges (does not decline) if:
#    - 100% remote
#    - OR in KY/Cincinnati area

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GMAIL_SKILL_DIR="$HOME/.openclaw/workspace/skills/gmail-personal"
TEMPLATE="$HOME/.openclaw/workspace/templates/job-reject-reply.txt"
LOG_FILE="$HOME/.openclaw/logs/job-reject-check.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

echo "🔍 Checking for JOB REJECT messages (SMART PROCESSING)..." | tee -a "$LOG_FILE"
echo "=========================================" | tee -a "$LOG_FILE"
echo ""

# Run the smart job reject processor
cd "$GMAIL_SKILL_DIR"
venv/bin/python3 scripts/process_rejects_smart.py --template "$TEMPLATE" 2>&1 | tee -a "$LOG_FILE"

echo ""
echo "✅ JOB REJECT check complete" | tee -a "$LOG_FILE"
echo "   Log: $LOG_FILE"

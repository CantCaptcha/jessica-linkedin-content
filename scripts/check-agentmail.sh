#!/bin/bash
# Check AgentMail inbox for unread messages

echo "🔍 Checking AgentMail inbox..."
echo "========================================="

cd /home/rwhitaker/.openclaw/workspace
node scripts/agentmail_unread.js

echo ""
echo "✅ AgentMail check complete"

#!/bin/bash
cd /home/rwhitaker/.openclaw/workspace/skills/gmail
venv/bin/python3 /home/rwhitaker/.openclaw/workspace/scripts/check-dcg-email.py "$@"

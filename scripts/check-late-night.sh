#!/bin/bash
# Wrapper to run late-night event checker with proper Python venv

cd /home/rwhitaker/.openclaw/workspace/skills/google-calendar
./venv/bin/python3 /home/rwhitaker/.openclaw/workspace/scripts/check-late-night-events.py "$@"

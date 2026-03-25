#!/usr/bin/env python3
"""Manually add JOB RESPONDED label to the 3 processed messages."""

import sys
sys.path.insert(0, '.')

from scripts.gmail import add_labels

message_ids = [
    '19c76f7dcc268462',  # Suman Ranjan
    '19c71dec441a9836',  # Kalyan Karamsetty
    '19c6cc25e74ef17d',  # Srikanth Bhandari
]

print("Adding JOB RESPONDED label to processed messages...\n")

for msg_id in message_ids:
    result = add_labels(msg_id, ['JOB RESPONDED'])
    if result:
        print(f"✓ {msg_id}: Label added")
    else:
        print(f"✗ {msg_id}: Failed to add label")

print("\nDone!")

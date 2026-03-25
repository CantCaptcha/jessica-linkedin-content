#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from scripts.cal import get_service

service = get_service()
if service:
    calendars = service.calendarList().list().execute()

    print("Looking for United calendar...\n")
    found = False
    for cal in calendars.get('items', []):
        if 'united' in cal.get('summary', '').lower():
            print(f"✓ Found: {cal['summary']}")
            print(f"   ID: {cal['id']}")
            print(f"   Access: {cal.get('accessRole', 'N/A')}")
            found = True

    if not found:
        print("✗ No United calendar found in DCG account")

    print("\nAll calendars in DCG account:")
    for cal in calendars.get('items', []):
        print(f"  - {cal['summary']} ({cal.get('id', 'no-id')})")

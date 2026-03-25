#!/usr/bin/env python3
"""
Smart Job Reject Processor - ANALYSIS ONLY

Parses job details from JOB REJECT emails and logs analysis.
NEVER sends email replies — this is for Richard's tracking only.
"""

import re
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'skills' / 'gmail-personal'))
from gmail import list_emails


def parse_job_requirements(email_preview: str, email_subject: str) -> dict:
    """Parse job details to determine if it should be declined."""
    requirements = {
        'requires_onsite': False,
        'is_remote': False,
        'location': None,
        'violates_preferences': False
    }

    preview_lower = email_preview.lower()
    subject_lower = email_subject.lower()

    # Check if explicitly mentions remote work
    remote_keywords = ['100% remote', 'fully remote', 'remote position', 'remote work',
                    'work from home', 'wfh', 'telework', 'virtual', 'hybrid remote']
    requirements['is_remote'] = any(keyword in preview_lower for keyword in remote_keywords)

    # Check if mentions specific locations
    location_match = re.search(r'(?:in|at|located)\s+([A-Za-z\s]+(?:,\s*[A-Za-z\s]+)*)|([A-Z]{2})', preview_lower)
    if location_match:
        location = location_match.group(1) or location_match.group(2)
        requirements['location'] = location.strip()

        # Check if location is KY/Cincinnati
        ky_keywords = ['kentucky', 'ky', 'cincinnati', 'cincinnati, oh', 'northern kentucky',
                     'covington', 'florence', 'newport', 'alexandria', 'fort thomas',
                     'maysville', 'independence']
        requirements['requires_onsite'] = any(city in location.lower() for city in ky_keywords)

    # Check subject for onsite/hybrid indicators
    onsite_keywords = ['onsite', 'on-site', 'hybrid', 'hybrid:', 'in office',
                    'must be in office', 'on location', 'onsite role']
    requirements['requires_onsite'] = any(keyword in preview_lower or keyword in subject_lower
                                         for keyword in onsite_keywords)

    # Determine if this violates preferences
    # Reject if: requires onsite AND not in KY/Cincinnati
    # Keep if: 100% remote OR in KY/Cincinnati area
    requirements['violates_preferences'] = (
        requirements['requires_onsite'] and
        (not requirements['is_remote'] and
         not requirements['location'] or
         (requirements['location'] and not any(city in requirements['location'].lower() for city in ['kentucky', 'ky', 'cincinnati', 'oh'])))
    )

    return requirements


def should_decline(requirements: dict) -> bool:
    """Determine if position should be declined based on preferences."""
    return requirements['violates_preferences']


def main():
    """Main processing function."""
    if len(sys.argv) < 2:
        print("Usage: python3 process_rejects_smart.py --template <template_path>")
        sys.exit(1)

    # Find JOB REJECT messages from last 10 days
    print("\n🔍 Finding JOB REJECT messages (last 10 days)...")
    print("NOTE: This is ANALYSIS ONLY — no emails will be sent.\n")
    reject_emails = list_emails(max_results=50, query='label:JOB REJECT newer_than:10d')

    if not reject_emails:
        print("✓ No JOB REJECT messages found.")
        return

    print(f"Found {len(reject_emails)} JOB REJECT message(s).\n")

    for email in reject_emails:
        msg_id = email['id']

        # Get full message body for parsing
        full_body = email.get('snippet', '') or email.get('preview', '')

        # Parse job requirements
        requirements = parse_job_requirements(full_body, email['subject'])

        print(f"\n📝 Analyzing: {email['subject'][:50]}")
        print(f"   From: {email['from'][:50]}")
        print(f"   Remote: {'✓' if requirements['is_remote'] else '✗'}")
        print(f"   Onsite: {'✓' if requirements['requires_onsite'] else '✗'}")
        print(f"   Location: {requirements['location'] or 'Not specified'}")

        if should_decline(requirements):
            print(f"   🚫 Would have declined: Violates preferences")
        else:
            print(f"   ✅ Would acknowledge: Good match!")

    print("\n" + "=" * 60)
    print("✅ Analysis complete")
    print("   No emails were sent — logged for review only.\n")


if __name__ == '__main__':
    main()

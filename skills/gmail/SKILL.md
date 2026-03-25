---
name: gmail
description: Gmail integration for sending emails, checking inbox, and managing email. Use when the user asks to: (1) Send an email to someone, (2) Send meeting invites or requests, (3) Check for unread emails, (4) Draft or manage emails.
---

# Gmail Integration

## Overview

This skill provides access to Gmail through the official Google API, enabling Stevie to send emails, check inbox, and manage email as an AI-powered email assistant.

## Core Capabilities

### 1. Send Emails

Send emails directly to recipients.

**When to use:**
- "Send an email to john@example.com"
- "Email Jessica about the meeting"
- "Send a meeting invitation"

**How to send an email:**
```bash
python3 scripts/gmail.py send \
  --to "recipient@example.com" \
  --subject "Meeting Request" \
  --body "Hi, would you like to schedule a meeting?"
```

### 2. Check Inbox

View unread or recent emails.

**When to use:**
- "Do I have any unread emails?"
- "Check my inbox"
- "Any important emails?"

**How to check inbox:**
```bash
python3 scripts/gmail.py list --max 10
```

## Authentication

### OAuth Scopes

Gmail integration uses these OAuth scopes:
- `https://www.googleapis.com/auth/gmail.send` - Send emails
- `https://www.googleapis.com/auth/gmail.readonly` - Read emails (optional)

These are minimal scopes to limit access to only sending emails (no inbox reading unless explicitly enabled).

### Setup

1. Enable Gmail API in Google Cloud Console (already enabled if using existing OAuth client)

2. Add Gmail scopes to existing credentials or create new OAuth client with Gmail scopes

3. Re-authenticate with Gmail scopes:
   ```bash
   cd /home/rwhitaker/.openclaw/workspace/skills/gmail
   venv/bin/python3 scripts/setup.py
   ```

## Best Practices

1. **Ask before sending** — Always confirm before sending important emails
2. **Use descriptive subjects** — Make emails easy to identify
3. **Keep it brief** — Short, clear emails are better
4. **Test first** — Send a test email to yourself first

## Security

- Never commit OAuth credentials or tokens
- Use minimal scopes (send-only when possible)
- Revoke access if compromised

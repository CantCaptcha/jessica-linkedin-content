---
name: gmail
description: Gmail integration for sending emails, checking inbox, and managing email. Use when user asks to: (1) Send an email to someone, (2) Send meeting invites or requests, (3) Check for unread emails, (4) Draft or manage emails.
---

# Gmail Integration

## Purpose

Gmail API integration for sending emails and checking inbox. Core capabilities:
- Send emails directly to recipients
- View unread or recent emails
- Manage email as AI-powered assistant

---

## Usage Examples

**Send email:**
```bash
python3 scripts/gmail.py send \
  --to "recipient@example.com" \
  --subject "Meeting Request" \
  --body "Hi, would you like to schedule a meeting?"
```

**Triggers:** "Send an email to john@example.com", "Email Jessica about meeting", "Send a meeting invitation"

**Check inbox:**
```bash
python3 scripts/gmail.py list --max 10
```

**Triggers:** "Do I have any unread emails?", "Check my inbox", "Any important emails?"

---

## Setup

**OAuth Scopes:**
- Send: `https://www.googleapis.com/auth/gmail.send` (minimal, send-only by default)
- Read: `https://www.googleapis.com/auth/gmail.readonly` (optional, for inbox checking)

**Steps:**
```bash
cd /home/rwhitaker/.openclaw/workspace/skills/gmail
venv/bin/python3 scripts/setup.py
```

**Docs:** https://developers.google.com/gmail/api/auth

---

## Best Practices

- Ask before sending important emails
- Use descriptive subjects
- Keep emails brief and clear
- Test by sending to yourself first

---

## Security

Never commit OAuth credentials, use minimal scopes, revoke access if compromised.

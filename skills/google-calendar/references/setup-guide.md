# Google Calendar Setup Guide

This guide walks you through setting up Google Calendar access for OpenClaw.

## Prerequisites

1. **Google Account**: You need a Google account (e.g., @gmail.com or Google Workspace)
2. **Python libraries**: Install the required packages:
   ```bash
   pip3 install google-auth google-auth-oauthlib google-api-python-client
   ```

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click **Create Project** (or select existing)
4. Give it a name (e.g., "OpenClaw Calendar")
5. Click **Create**

## Step 2: Enable Google Calendar API

1. In your Google Cloud project, go to **APIs & Services** > **Library**
2. Search for "Google Calendar API"
3. Click on it, then click **Enable**

## Step 3: Create OAuth Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. If prompted, configure the OAuth consent screen first:
   - Choose **External** (for personal use) or **Internal** (for Google Workspace)
   - Fill in required fields (App name, User support email, etc.)
   - Click **Save and Continue**
4. Back to creating credentials:
   - Select **Desktop application**
   - Give it a name (e.g., "OpenClaw Desktop")
   - Click **Create**
5. Download the credentials file as JSON

## Step 4: Run Setup Script

1. Copy the downloaded `credentials.json` to the skill config directory:
   ```bash
   cp ~/Downloads/credentials.json /home/rwhitaker/.openclaw/workspace/skills/google-calendar/config/credentials.json
   ```

2. Run the setup script:
   ```bash
   python3 /home/rwhitaker/.openclaw/workspace/skills/google-calendar/scripts/setup.py
   ```

3. A browser window will open. Sign in to your Google account and authorize the app.

4. If successful, you'll see:
   ```
   ✓ Setup complete!
   Credentials saved to: /home/rwhitaker/.openclaw/workspace/skills/google-calendar/config/token.json
   ✓ Successfully connected! Found X calendars.
   ```

## Troubleshooting

### "No valid credentials found"
- Run the setup script again
- Make sure `credentials.json` is in the `config/` directory
- Check that the file is valid JSON

### "Error refreshing credentials"
- Delete `token.json` and run setup again
- Make sure your OAuth client ID is still valid

### "API has not been enabled"
- Make sure you enabled the Google Calendar API in Google Cloud Console
- Wait a few minutes for changes to propagate

### Calendar not found
- Verify the calendar ID
- Use `calendar id:primary` for your main calendar
- Check calendar sharing settings

## Testing

Test the connection:

```bash
python3 /home/rwhitaker/.openclaw/workspace/skills/google-calendar/scripts/calendar.py list --max 5
```

This should list your next 5 calendar events.

## Security Notes

- **Never commit credentials.json or token.json to version control**
- Add `config/` to your `.gitignore` file
- Token.json contains refresh tokens - keep it secure
- You can revoke access at any time from [Google Account Settings](https://myaccount.google.com/permissions)

## Next Steps

Once set up, you can:
- Ask Stevie to check your calendar
- Request availability for specific times
- Have others ask "When is Richard free?"
- Create and manage events

Stevie will use the calendar integration to help schedule meetings!

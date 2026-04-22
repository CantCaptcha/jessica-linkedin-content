---
name: bitwarden
description: Secure Bitwarden vault integration for managing sensitive information like travel accounts, credentials, and secure notes. Use when retrieving loyalty program numbers, passwords, or storing new sensitive data. Ideal for travel booking workflows where account numbers should never be stored in plain text.
---

# Bitwarden

## Stevie's Hybrid Security Model 🔐

**IMPORTANT:** Stevie uses a hybrid approach for Bitwarden access:

### Workflow
1. **You export** travel accounts from "Stevie" folder → `skills/bitwarden/scripts/export-travel-accounts.sh`
2. **Stevie reads** from `secure/travel-accounts.json` → fast, automated, no unlock prompts
3. **Re-export** when you update account numbers

### Folder ID
`X1jL68Rkg5iFufrQMDXVywqeVXxgyk4NFUwJfNFLG488+y232YvBkkHXGFuh71CoODZMsCfhXSuT9fLJbQgNCA==`

### Restrictions
- ✅ Stevie reads ONLY from secure export file (never Bitwarden directly)
- ✅ READ-ONLY access to `secure/travel-accounts.json`
- ❌ Stevie CANNOT write to secure directory
- ❌ Stevie CANNOT access other Bitwarden folders

### Why This Model?
Security: Your vault stays locked. Automation: I work independently. Simplicity: No repeated unlock prompts.

See `secure/README.md` for full workflow documentation.

---

## Bitwarden CLI Setup

**Install:** https://bitwarden.com/help/cli/

**Login/Unlock:**
```bash
bw login               # Interactive (email + password)
bw login --apikey       # API key for automation
bw unlock              # Returns session key
export BW_SESSION="..." # Commands auto-use this variable
```

**Session Management:** Session key expires after inactivity or explicit lock. Re-run `bw unlock` when needed.

---

## Stevie's Commands (Travel Data)

```bash
# List all travel accounts
python3 skills/bitwarden/scripts/travel_accounts.py list

# Get full account details
python3 skills/bitwarden/scripts/travel_accounts.py get "United Mileage Plus"

# Get specific login field (default: username)
python3 skills/bitwarden/scripts/travel_accounts.py login "United Mileage Plus"
python3 skills/bitwarden/scripts/travel_accounts.py login "United Mileage Plus" password

# Get account notes
python3 skills/bitwarden/scripts/travel_accounts.py notes "Marriott Bonvoy"
```

**For Richard (Export to secure file):**
```bash
bw unlock && export BW_SESSION="..."
skills/bitwarden/scripts/export-travel-accounts.sh
```

---

## Core Bitwarden Commands

### List Items
```bash
bw list items                          # All items
bw list items --search "United"          # Filter by name
```

### Get Item
```bash
bw get item "United Mileage Plus"       # By name
bw get item <item-id>                  # By ID
bw get password "Marriott Bonvoy"        # Specific field
```

### Create Item
```bash
# Login item
bw create item '{
  "type": 1,
  "name": "American AAdvantage",
  "login": {"username": "1W87X74", "uri": "https://www.aa.com"},
  "notes": "Account type: Airline Loyalty"
}'

# Secure note
bw create item '{
  "type": 2,
  "name": "Flight Confirmation",
  "secureNote": {"notes": "Booking: XYZ123\nDate: Apr 6, 2026"}
}'

# Using templates
bw get template item | jq '.name = "New"' | bw encode | bw create item
```

### Edit/Delete
```bash
bw get item "Name" | jq '.login.username = "NEW"' | bw encode | bw edit item <id>
bw delete item <id>                           # Moves to Trash (30-day auto-delete)
bw sync                                     # Ensure vault up-to-date
```

---

## Travel Account Patterns

### Naming Convention (Searchable)
"United Mileage Plus", "American AAdvantage", "Delta SkyMiles", "Marriott Bonvoy", "Hilton Honors", "National Car Rental", "Hertz Gold Plus Rewards", "TSA PreCheck"

### Common Patterns
- **Retrieve for booking:** `bw unlock` → `bw get item "Name"` → Use → `bw lock`
- **Add new account:** `bw create item` (type 1 for login, type 2 for note)
- **Batch operations:** Pipe to `jq` for JSON parsing

### Item Types
1 = Login, 2 = Secure Note, 3 = Card, 4 = Identity

---

## Troubleshooting

**"Session not found":** `bw unlock` and re-export `BW_SESSION`
**"Item not found":** `bw list items --search "name"` to check exact naming
**CLI not installed:** Download from https://bitwarden.com/help/cli/

---

## Additional Resources

**Stevie Scripts:**
- `skills/bitwarden/scripts/travel_accounts.py` - Read travel accounts from secure file
- `skills/bitwarden/scripts/export-travel-accounts.sh` - Export from Bitwarden (Richard uses)
- `skills/bitwarden/scripts/bw-stevie.sh` - Safety wrapper for Bitwarden commands

**Bitwarden Docs:**
- Official: https://bitwarden.com/help/cli/
- Self-documented: `bw --help`, `bw list --help`, `bw get item --help`

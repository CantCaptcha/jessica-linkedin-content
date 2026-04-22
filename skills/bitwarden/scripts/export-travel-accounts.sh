#!/bin/bash
# Export travel accounts from Bitwarden to Stevie's secure workspace
# Run this to update travel data after you change account numbers

set -e

echo "📤 Exporting travel accounts from Bitwarden..."
echo ""

# Check if vault is unlocked
if [ -z "$BW_SESSION" ]; then
  echo "❌ ERROR: BW_SESSION not set"
  echo "   Run: bw unlock && export BW_SESSION='...'"
  exit 1
fi

# Stevie folder ID
STEVIE_FOLDER="X1jL68Rkg5iFufrQMDXVywqeVXxgyk4NFUwJfNFLG488+y232YvBkkHXGFuh71CoODZMsCfhXSuT9fLJbQgNCA=="

# Output file
OUTPUT_FILE="/home/rwhitaker/.openclaw/workspace/secure/travel-accounts.json"

# Export items from Stevie folder
echo "Fetching items from Stevie folder..."
bw list items --folderid "$STEVIE_FOLDER" --session "$BW_SESSION" > "$OUTPUT_FILE"

# Count items
ITEM_COUNT=$(jq '. | length' "$OUTPUT_FILE")

echo ""
echo "✅ Export complete!"
echo "   Location: $OUTPUT_FILE"
echo "   Items exported: $ITEM_COUNT"
echo ""
echo "Stevie will now use this file for travel account lookups."
echo "Run this script again when you update account numbers."

#!/bin/bash
# Bitwarden CLI Helper for Stevie
# RESTRICTED: Only accesses "Stevie" folder
# NEVER run commands without --folderid

# STEVIE FOLDER ID - NEVER CHANGE THIS WITHOUT RICHARD'S PERMISSION
STEVIE_FOLDER_ID="X1jL68Rkg5iFufrQMDXVywqeVXxgyk4NFUwJfNFLG488+y232YvBkkHXGFuh71CoODZMsCfhXSuT9fLJbQgNCA=="

# Export for use in other commands
export STEVIE_FOLDER_ID

# Safety check: Ensure BW_SESSION is set
if [ -z "$BW_SESSION" ]; then
  echo "❌ ERROR: BW_SESSION not set. Run: bw unlock && export BW_SESSION='...'"
  exit 1
fi

# Validate folder ID (basic check)
if [ -z "$STEVIE_FOLDER_ID" ]; then
  echo "❌ ERROR: STEVIE_FOLDER_ID not configured"
  exit 1
fi

# Run command with safety checks
case "$1" in
  list)
    # List items in Stevie folder ONLY
    bw list items --folderid "$STEVIE_FOLDER_ID" ${@:2}
    ;;
  create)
    # Create item - MUST include folderId in JSON
    # Usage: bw-stevie.sh create '<json-with-folderId>'
    if echo "$2" | grep -q '"folderId"' ; then
      bw create item "$2" --session "$BW_SESSION"
    else
      echo "❌ ERROR: JSON must include folderId. Add: \"folderId\": \"$STEVIE_FOLDER_ID\""
      exit 1
    fi
    ;;
  get)
    # Get item from Stevie folder
    bw get item "$2" --session "$BW_SESSION"
    ;;
  search)
    # Search within Stevie folder
    bw list items --folderid "$STEVIE_FOLDER_ID" --search "$2" --session "$BW_SESSION"
    ;;
  *)
    echo "❌ ERROR: Unknown command: $1"
    echo "Usage: bw-stevie.sh [list|create|get|search] [args]"
    exit 1
    ;;
esac

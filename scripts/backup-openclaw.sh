#!/bin/bash
# OpenClaw Backup Script
# Backs up all critical OpenClaw data for migration or disaster recovery

set -e

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/openclaw-backups"
BACKUP_NAME="openclaw-backup-${BACKUP_DATE}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

echo "🦞 OpenClaw Backup"
echo "=================="
echo "Backup: ${BACKUP_NAME}"
echo ""

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Create temporary directory for this backup
TEMP_DIR=$(mktemp -d)
trap "rm -rf ${TEMP_DIR}" EXIT

echo "📦 Packing backup..."

# 1. Configuration (most important - contains API keys, tokens, settings)
echo "  ✓ Configuration"
mkdir -p "${TEMP_DIR}/config"
cp ~/.openclaw/openclaw.json "${TEMP_DIR}/config/"
cp ~/.openclaw/*.bak "${TEMP_DIR}/config/" 2>/dev/null || true

# 2. Workspace (MEMORY.md, skills, identity, etc.)
echo "  ✓ Workspace"
cp -r ~/.openclaw/workspace "${TEMP_DIR}/workspace/"

# 3. Sessions (conversation history)
echo "  ✓ Sessions"
cp -r ~/.openclaw/agents/main/sessions "${TEMP_DIR}/sessions/" 2>/dev/null || true

# 4. Cron jobs (scheduled tasks)
echo "  ✓ Cron jobs"
cp -r ~/.openclaw/cron "${TEMP_DIR}/cron/" 2>/dev/null || true

# 5. Credentials (OAuth tokens, etc.)
echo "  ✓ Credentials"
cp -r ~/.openclaw/credentials "${TEMP_DIR}/credentials/" 2>/dev/null || true

# 6. Identity files
echo "  ✓ Identity"
cp -r ~/.openclaw/identity "${TEMP_DIR}/identity/" 2>/dev/null || true

# 7. Device pairings
echo "  ✓ Device pairings"
cp -r ~/.openclaw/devices "${TEMP_DIR}/devices/" 2>/dev/null || true

# 8. QMD (semantic search engine - models, index, collections)
echo "  ✓ QMD (semantic search)"
cp -r ~/.cache/qmd "${TEMP_DIR}/qmd/" 2>/dev/null || true

# 9. Obsidian Vault (personal notes, meeting notes, knowledge base)
echo "  ✓ Obsidian Vault"
cp -r ~/ObsidianVault "${TEMP_DIR}/obsidian/" 2>/dev/null || true

# 10. Create archive
echo ""
echo "📦 Creating compressed archive..."
cd "${TEMP_DIR}"
tar -czf "${BACKUP_PATH}.tar.gz" .
echo "  ✓ Created: ${BACKUP_PATH}.tar.gz"

# Get file size
SIZE=$(du -h "${BACKUP_PATH}.tar.gz" | cut -f1)

# 11. Cleanup old backups (keep last 3 backups)
echo ""
echo "🗑️  Cleaning up old backups (keeping last 3)..."
cd "${BACKUP_DIR}"
ls -t openclaw-backup-*.tar.gz | tail -n +4 | xargs rm -v 2>/dev/null || true
REMAINING=$(ls -1 openclaw-backup-*.tar.gz 2>/dev/null | wc -l)
echo "  ✓ Kept ${REMAINING} most recent backup(s)"

echo ""
echo "✅ Backup complete!"
echo "   Location: ${BACKUP_PATH}.tar.gz"
echo "   Size: ${SIZE}"
echo ""
echo "📝 To restore on a new system:"
echo "   1. Install OpenClaw: npm install -g openclaw"
echo "   2. Extract backup: tar -xzf ${BACKUP_NAME}.tar.gz -C ~/.openclaw/"
echo "   3. Restart OpenClaw: openclaw gateway restart"
echo ""
echo "💡 Keep backups safe! They contain API keys and sensitive data."

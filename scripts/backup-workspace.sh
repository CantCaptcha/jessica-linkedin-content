#!/bin/bash
# Backup OpenClaw workspace with retention policy

# Configuration
WORKSPACE="/home/rwhitaker/.openclaw/workspace"
BACKUP_DIR="/home/rwhitaker/backups"
RETENTION_DAYS=30
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M)
BACKUP_NAME="openclaw-workspace-${DATE}-${TIME}.tar.gz"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"
LOG_FILE="${BACKUP_DIR}/backup.log"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting workspace backup"

# Check if workspace exists
if [ ! -d "$WORKSPACE" ]; then
    log "ERROR: Workspace directory not found: $WORKSPACE"
    exit 1
fi

# Create the backup
log "Creating backup: $BACKUP_NAME"
tar -czf "$BACKUP_PATH" -C "$WORKSPACE" . 2>/dev/null

# Check if backup was successful
if [ $? -eq 0 ]; then
    SIZE=$(du -h "$BACKUP_PATH" | cut -f1)
    log "Backup created successfully: $SIZE"
else
    log "ERROR: Backup creation failed"
    exit 1
fi

# Remove backups older than RETENTION_DAYS
log "Removing backups older than $RETENTION_DAYS days"
DELETED=$(find "$BACKUP_DIR" -name "openclaw-workspace-*.tar.gz" -type f -mtime +$RETENTION_DAYS -delete -print 2>/dev/null | wc -l)

if [ "$DELETED" -gt 0 ]; then
    log "Deleted $DELETED old backup(s)"
else
    log "No old backups to delete"
fi

# List current backups
log "Current backups in $BACKUP_DIR:"
ls -lh "$BACKUP_DIR"/openclaw-workspace-*.tar.gz 2>/dev/null | awk '{print $9, $5}' | tee -a "$LOG_FILE"

log "Backup completed"

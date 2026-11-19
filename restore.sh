#!/bin/bash
# Restore RuView Project from backup
# Usage: bash restore.sh <backup.tar.gz>
# Example: bash restore.sh ~/RuView-Backup/RuView-Before-2026-01-01.tar.gz
echo "=== RESTORE POINT ==="
if [ -z "$1" ]; then
  echo "Usage: bash restore.sh <backup.tar.gz>"
  echo "Available backups:"
  ls -lh ~/RuView-Backup/*.tar.gz
  exit 1
fi
echo "Restoring from $1 ..."
tar -xzf $1 -C ~/
echo "Restore DONE. Project back in ~/RuView-APK-Final"
ls -lh ~/RuView-APK-Final/

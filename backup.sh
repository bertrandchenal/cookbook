# Stop on any error
set -euo pipefail
# Use english names
unset LANG

# Usage function
usage() {
    echo "Create Year, month and day-of-week backups"
    echo "Usage: $0 SOURCE_FILE BACKUP_DIR"
    exit 1
}

SOURCE_FILE="$1"
BACKUP_DIR="$2"

# Validate input
if [ -z "$SOURCE_FILE" ] || [ -z "$BACKUP_DIR" ]; then
    usage
fi
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: Source file does not exist: $SOURCE_FILE"
    exit 1
fi

# Create backup directories if they don't exist
mkdir -p "$BACKUP_DIR"

# Create symlinks
YEAR=$(date +%Y)
MONTH=$(date +%b)
DOW=$(date +%a)

# Copy source to $year and smlink others
cp  $SOURCE_FILE "$BACKUP_DIR/$YEAR"
ln --force "$BACKUP_DIR/$YEAR" "$BACKUP_DIR/$MONTH"
ln --force "$BACKUP_DIR/$YEAR" "$BACKUP_DIR/$DOW"

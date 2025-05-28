#!/bin/bash

# Function to process each Python file
process_file() {
    local file="$1"
    echo "Processing: $file"

    # Create a backup
    cp "$file" "${file}.bak"

    # Replace patterns that look like:
    # - GUIDs/UUIDs
    # - API keys (alphanumeric strings 20+ chars)
    # - Secret keys
    # - Access tokens
    # - Any string (quoted or not) with 20+ chars without spaces
    sed -i.tmp \
        -e 's/[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}/"<YOUR_SECRET_VALUE>"/gI' \
        -e 's/\b[A-Za-z0-9_-]\{20,\}\b/"<YOUR_SECRET_VALUE>"/g' \
        -e 's/["'"'"']\{1\}sk_[a-zA-Z0-9]\{20,\}["'"'"']\{1\}/"<YOUR_SECRET_VALUE>"/g' \
        -e 's/["'"'"']\{1\}[a-zA-Z0-9_-]\{40,\}["'"'"']\{1\}/"<YOUR_SECRET_VALUE>"/g' \
        -e 's/["'"'"']\{1\}[^ '"'"'"]\{50,\}["'"'"']\{1\}/"<YOUR_SECRET_VALUE>"/g' \
        "$file"

    # Remove temporary files
    rm "${file}.bak"
}

# Main script
echo "Starting secret sanitization..."

# Find all Python files in current directory and subdirectories, excluding venv directories
find . -type f -name "*.py" -not -path "*/venv/*" -not -path "*/.venv/*" | while read -r file; do
    process_file "$file"
done

echo "Sanitization complete! Backup files have been created with .bak extension"
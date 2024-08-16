#!/bin/bash
TARGET_DIR="your_path"

CURRENT_TIME=$(date +%s)

for dir in "$TARGET_DIR"/*; do

    if [ -d "$dir" ]; then

        dir_name=$(basename "$dir")

        if [[ "$dir_name" =~ ^[0-9]+$ ]]; then
            creation_time=$(stat -c %Y "$dir")

            age=$((CURRENT_TIME - creation_time))

            DAYS=3
            THRESHOLD=$((DAYS * 24 * 60 * 60))

            if [ "$age" -gt "$THRESHOLD" ]; then
                echo "Deleting directory: $dir (Age: $((age / 86400)) days)"
                rm -rf "$dir"
            fi
        fi
    fi
done
#!/bin/bash
cd "$(dirname "$0")"

echo "📦 Saving changes to GitHub at $(date)..."

# Add all modified and new files
git add .

# Commit with a timestamp message
git commit -m "📦 Auto-save at $(date +"%Y-%m-%d %H:%M:%S")"

# Push to the main branch
git push

echo "✅ Project saved to GitHub!"
read -p "Press [Enter] to close this window..."

#!/bin/bash
# AllMorphe Update Script
# Fetches the latest patches from morphe-patches.software and updates the bundle
# Can be run locally or by GitHub Actions

set -e

echo "📡 AllMorphe: Starting patch update process..."

# Run the Python fetch script
cd /workspace/chats/0249e006b34c1ec1eb4d28a3/allmorphe
python3 fetch_patches.py

echo "✅ AllMorphe update process complete."
echo "📌 Run 'git add patches-bundle.json && git commit -m \"Update AllMorphe patches\" && git push' to update Morphe"
echo "📱 Or push to GitHub and the Actions workflow will auto-update"
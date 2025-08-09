#!/bin/bash
# Manual trigger script for language statistics update
# Usage: ./trigger_update.sh

GITHUB_USERNAME="${GITHUB_USERNAME:-UniqeBd}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable not set"
    echo "Please set your GitHub personal access token:"
    echo "export GITHUB_TOKEN=your_token_here"
    exit 1
fi

echo "🚀 Triggering language statistics update for $GITHUB_USERNAME..."

curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$GITHUB_USERNAME/$GITHUB_USERNAME/dispatches" \
  -d '{"event_type":"update-stats","client_payload":{"triggered_manually":true}}'

if [ $? -eq 0 ]; then
    echo "✅ Update triggered successfully!"
    echo "📊 Check the Actions tab to see the progress"
else
    echo "❌ Failed to trigger update"
    exit 1
fi

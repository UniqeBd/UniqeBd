#!/bin/bash

# Script to trigger the test language statistics workflow
# Usage: ./trigger-test.sh [dry-run]

REPO="UniqeBd/UniqeBd"
WORKFLOW="test-language-stats.yml"

# Check if dry-run parameter is provided
if [ "$1" = "dry-run" ]; then
    DRY_RUN="true"
    echo "🧪 Triggering TEST workflow in DRY-RUN mode..."
else
    DRY_RUN="false"
    echo "🧪 Triggering TEST workflow (will create PR if changes detected)..."
fi

# Trigger the workflow using GitHub CLI
if command -v gh &> /dev/null; then
    gh workflow run "$WORKFLOW" \
        --repo "$REPO" \
        --field dry_run="$DRY_RUN"
    
    echo "✅ Test workflow triggered successfully!"
    echo "📋 You can monitor the progress at:"
    echo "   https://github.com/$REPO/actions"
    echo ""
    echo "⏰ The workflow will take a few minutes to complete."
    
    if [ "$DRY_RUN" = "true" ]; then
        echo "🔍 Running in dry-run mode - no commits or PRs will be created"
    else
        echo "🚀 Running in full mode - will create a test PR if changes are detected"
    fi
else
    echo "❌ GitHub CLI (gh) not found. Please install it first:"
    echo "   https://cli.github.com/"
    echo ""
    echo "🔄 Alternative: Manually trigger the workflow from GitHub:"
    echo "   1. Go to https://github.com/$REPO/actions"
    echo "   2. Click on 'Test Language Statistics Update'"
    echo "   3. Click 'Run workflow'"
    echo "   4. Set dry_run to $DRY_RUN"
    echo "   5. Click 'Run workflow'"
fi

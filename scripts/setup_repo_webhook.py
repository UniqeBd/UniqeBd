#!/usr/bin/env python3
"""
Helper script to set up automatic language statistics updates from other repositories.
This script helps configure repository webhooks to trigger immediate updates.
"""

import os
import tempfile

def create_webhook_action_file():
    """Create a GitHub Action file that can be added to other repositories"""
    action_content = """name: Trigger Language Stats Update

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  trigger-stats-update:
    runs-on: ubuntu-latest
    
    steps:
    - name: Trigger language statistics update
      run: |
        curl -X POST \\
          -H "Authorization: token ${{ secrets.PERSONAL_ACCESS_TOKEN }}" \\
          -H "Accept: application/vnd.github.v3+json" \\
          https://api.github.com/repos/${{ github.repository_owner }}/${{ github.repository_owner }}/dispatches \\
          -d '{"event_type":"update-stats","client_payload":{"repository":"${{ github.repository }}","ref":"${{ github.ref }}"}}'
"""
    
    # Use cross-platform temporary directory
    temp_dir = os.path.join(tempfile.gettempdir(), 'webhook-setup')
    os.makedirs(temp_dir, exist_ok=True)
    
    action_file_path = os.path.join(temp_dir, 'trigger-language-stats.yml')
    with open(action_file_path, 'w') as f:
        f.write(action_content)
    
    print("✅ Created trigger-language-stats.yml action file")
    print(f"📁 Location: {action_file_path}")
    print()
    print("📋 To use this in your other repositories:")
    print("1. Copy this file to .github/workflows/ in your other repositories")
    print("2. Add a PERSONAL_ACCESS_TOKEN secret with repo access")
    print("3. This will trigger language stats updates when you push code")

def create_manual_trigger_script():
    """Create a manual trigger script for immediate updates"""
    script_content = """#!/bin/bash
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

curl -X POST \\
  -H "Authorization: token $GITHUB_TOKEN" \\
  -H "Accept: application/vnd.github.v3+json" \\
  "https://api.github.com/repos/$GITHUB_USERNAME/$GITHUB_USERNAME/dispatches" \\
  -d '{"event_type":"update-stats","client_payload":{"triggered_manually":true}}'

if [ $? -eq 0 ]; then
    echo "✅ Update triggered successfully!"
    echo "📊 Check the Actions tab to see the progress"
else
    echo "❌ Failed to trigger update"
    exit 1
fi
"""
    
    temp_dir = os.path.join(tempfile.gettempdir(), 'webhook-setup')
    script_file_path = os.path.join(temp_dir, 'trigger_update.sh')
    
    with open(script_file_path, 'w') as f:
        f.write(script_content)
    
    # Make executable on Unix-like systems
    if os.name != 'nt':
        os.chmod(script_file_path, 0o755)
    
    print("✅ Created manual trigger script")
    print(f"📁 Location: {script_file_path}")
    print()
    print("📋 To use this script:")
    print("1. Set your GITHUB_TOKEN environment variable")
    print("2. Run ./trigger_update.sh to manually trigger an update")

def print_setup_instructions():
    """Print comprehensive setup instructions"""
    print("🔧 AUTOMATIC LANGUAGE DETECTION SETUP")
    print("=" * 50)
    print()
    print("Your language statistics system is now enhanced with:")
    print("✅ Daily automatic updates (instead of weekly)")
    print("✅ Immediate detection of new repositories")
    print("✅ Cross-repository trigger support")
    print("✅ Enhanced logging and feedback")
    print()
    print("🎯 FOR IMMEDIATE UPDATES WHEN CREATING NEW REPOS:")
    print()
    print("Option 1: Automatic (Recommended)")
    print("- The system now runs daily and will detect new repos within 24 hours")
    print("- New repositories are highlighted in the logs")
    print()
    print("Option 2: Manual Trigger")
    print("- Go to your profile repo > Actions > 'Update Language Statistics'")
    print("- Click 'Run workflow' to trigger immediate update")
    print()
    print("Option 3: From Other Repositories (Advanced)")
    print("- Add the generated GitHub Action to your other repositories")
    print("- They will automatically trigger updates when you push code")
    print()
    print("🔗 WEBHOOK SETUP FOR OTHER REPOSITORIES:")
    print("- Copy the action file to other repos: .github/workflows/trigger-language-stats.yml")
    print("- Add PERSONAL_ACCESS_TOKEN secret with repo access")
    print("- Pushes to main/master will trigger immediate language stats updates")
    print()
    print("📊 FEATURES:")
    print("- Detects languages from all public repositories")
    print("- Smart framework detection (React, Flutter, Node.js, etc.)")
    print("- Automatic progress bar updates")
    print("- Excludes forked repositories")
    print("- Color-coded language badges")

def main():
    print("🚀 Setting up automatic language detection...")
    print()
    
    create_webhook_action_file()
    print()
    create_manual_trigger_script()
    print()
    print_setup_instructions()

if __name__ == '__main__':
    main()
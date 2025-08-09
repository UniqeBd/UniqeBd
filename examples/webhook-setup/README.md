# Webhook Setup Examples

This folder contains helper files for setting up automatic language statistics updates when you create new repositories or push code to existing ones.

## 🚀 Quick Setup for Immediate Updates

### For Other Repositories (Cross-Repository Automation)

1. **Copy the Action File**:
   ```bash
   cp trigger-language-stats.yml your-other-repo/.github/workflows/
   ```

2. **Add GitHub Token Secret**:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PERSONAL_ACCESS_TOKEN`
   - Value: Your GitHub personal access token with `repo` scope

3. **That's it!** Now when you push code to that repository, it will automatically trigger a language statistics update on your profile.

### For Manual Triggering

1. **Make the script executable**:
   ```bash
   chmod +x trigger_update.sh
   ```

2. **Set your GitHub token**:
   ```bash
   export GITHUB_TOKEN=your_github_token_here
   ```

3. **Run the trigger**:
   ```bash
   ./trigger_update.sh
   ```

## 📋 How It Works

- **trigger-language-stats.yml**: GitHub Action that triggers language stats updates from other repositories
- **trigger_update.sh**: Manual script to immediately trigger an update

## 🔧 Personal Access Token Setup

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select these scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
4. Copy the token and use it as `PERSONAL_ACCESS_TOKEN` secret

## ⚡ Automatic Detection Features

With these files set up, you get:
- ✅ Immediate language detection when pushing new code
- ✅ Automatic framework detection (React, Flutter, Node.js, etc.)
- ✅ Real-time progress bar updates
- ✅ Smart repository categorization
- ✅ Cross-repository synchronization

## 🎯 Use Cases

- **New Project**: Create repo → Push code → Language stats update automatically
- **Framework Change**: Switch from vanilla JS to React → Stats reflect change immediately  
- **Language Learning**: Try new programming language → Progress bars update to show growth
- **Portfolio Updates**: Add new projects → Profile languages update to match your skillset

## 📊 What Gets Updated

When triggered, the system updates:
- Programming language percentages in README.md
- Progress bars with correct colors and percentages
- Framework and tools badges based on actual usage
- Repository categorization and framework detection

Run `python ../scripts/setup_repo_webhook.py` to regenerate these files with the latest setup instructions.
# Language Statistics Auto-Update

This repository contains an **enhanced automated system** that immediately detects new repositories and updates both the language usage statistics and the "Languages and Tools" section in the README.md file.

## 🆕 Latest Updates & Fixes

- ✅ **Fixed workflow failures**: Resolved path issues that caused daily job failures
- ✅ **Cross-platform compatibility**: Works on Windows, macOS, and Linux
- ✅ **Robust error handling**: Added retry logic and better error messages
- ✅ **Improved badge generation**: Fixed logo slugs and URL encoding for special characters
- ✅ **Configurable React detection**: Set `REACT_JS_ALLOCATION_PERCENT` (default: 0 = disabled)
- ✅ **Enhanced framework detection**: Uses repository topics for better accuracy
- ✅ **HTML marker-based updates**: More reliable README section replacement

## ✨ Immediate Language Detection Features

The system now provides **immediate detection** when you create new repositories and push projects:

- 🚀 **Daily Automatic Updates**: Runs every day for faster detection
- 🆕 **New Repository Detection**: Automatically highlights recently created repositories  
- ⚡ **Cross-Repository Triggers**: Other repositories can trigger immediate updates
- 📊 **Real-time Language Analysis**: Updates progress bars as soon as new languages are detected
- 🎯 **Smart Framework Detection**: Instantly recognizes frameworks and tools in new projects

## How it works

1. **Enhanced GitHub Actions Workflow**: The `.github/workflows/update-language-stats.yml` workflow triggers:
   - **Daily at 00:00 UTC** for immediate detection of new repositories
   - When **any code is pushed** to the main branch
   - Via **repository_dispatch** events from other repositories
   - Manually via workflow dispatch

2. **Enhanced Language Analysis Script**: The `scripts/update_language_stats.py` script:
   - Fetches all public repositories sorted by most recently updated
   - **Detects repositories created within the last 30 days**
   - Analyzes language usage across all repositories (excluding forks)
   - Calculates percentage distribution of languages by bytes
   - Detects frameworks and tools based on repository analysis
   - Updates both the "Most Used Languages" table and "Languages and Tools" section in README.md
   - **Provides detailed logging** showing which new repositories were detected
   - Commits changes if statistics have changed

## 🎯 Quick Setup for New Repositories

### Method 1: Automatic Detection (Recommended)
- The system runs **daily** and will detect new repositories within 24 hours
- New repositories are automatically highlighted in the logs with 🆕 indicators
- No manual intervention required

### Method 2: Manual Trigger (Instant)
1. Go to your profile repository → Actions → "Update Language Statistics"
2. Click "Run workflow" to trigger immediate update
3. New languages and repositories will be detected within minutes

### Method 3: Cross-Repository Automation (Advanced)
Set up other repositories to automatically trigger updates when you push code:

1. Run the setup helper:
   ```bash
   python scripts/setup_repo_webhook.py
   ```

2. Copy the generated action file to your other repositories:
   ```
   .github/workflows/trigger-language-stats.yml
   ```

3. Add a `PERSONAL_ACCESS_TOKEN` secret with repo access

4. Now pushes to any configured repository will trigger immediate language stats updates!

## 🔧 Local Development

For local testing and development:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   export GITHUB_TOKEN=your_github_token
   export GITHUB_USERNAME=UniqeBd
   # Optional: Enable React detection (percentage of JS to convert to React)
   export REACT_JS_ALLOCATION_PERCENT=60
   ```

3. **Run the script**:
   ```bash
   python scripts/update_language_stats.py
   ```

## Configuration Options

- `REACT_JS_ALLOCATION_PERCENT`: Percentage of JavaScript to convert to React in detected React projects (default: 0 = disabled)
- `GITHUB_TOKEN`: Your GitHub personal access token
- `GITHUB_USERNAME`: Your GitHub username
- `GITHUB_WORKSPACE`: Workspace directory (auto-detected in CI)

## Features

- **Automatic Updates**: No manual intervention needed when adding new repositories
- **Dynamic Languages and Tools**: The "Languages and Tools" section now shows images based on actual repository data
- **Rate Limiting**: Built-in delays to respect GitHub API rate limits
- **Language Colors**: Maintains consistent badge colors for popular languages
- **React Detection**: Automatically detects React projects and shows React as a separate language
- **Framework Detection**: Intelligently detects frameworks like Flutter, React, Node.js, Android Studio based on repository names and descriptions
- **Top Languages**: Shows top languages by percentage in the statistics table
- **Smart Tool Detection**: Only shows frameworks and tools that are actually used in repositories
- **Fork Exclusion**: Excludes forked repositories from statistics
- **Error Handling**: Graceful handling of API errors and rate limits

## Sections Updated

### 🛠️ Languages and Tools
- **Programming Languages**: Dynamically generated based on actual language usage from repositories
- **Frameworks & Tools**: Automatically detects and displays only frameworks/tools actually used
- **Ordered by Usage**: Languages appear in order of usage frequency
- **Visual Consistency**: Maintains the same badge style while adding dynamic functionality

### 📊 Most Used Languages
- **Percentage Table**: Shows detailed breakdown with percentages and progress bars
- **Top 10 Display**: Limits to most relevant languages
- **Color-Coded**: Each language has its distinctive color

## Manual Trigger

You can manually trigger the language statistics update by:
1. Going to the Actions tab in your repository
2. Selecting "Update Language Statistics" workflow
3. Click "Run workflow"

## Customization

### Adding New Language Colors

Edit the `language_colors` dictionary in `scripts/update_language_stats.py`:

```python
self.language_colors = {
    'NewLanguage': 'COLOR_HEX',
    'React': '61DAFB',        # React projects
    'JSX': '61DAFB',          # JSX files
    # ... existing colors
}
```

### Adding New Framework Detection

Edit the `detect_frameworks_and_tools()` method to add new framework detection:

```python
# Add new framework detection logic
if 'newframework' in repo_name or 'newframework' in description:
    detected['NewFramework'] = True
```

### Changing Update Frequency

Modify the cron schedule in `.github/workflows/update-language-stats.yml`:

```yaml
schedule:
  - cron: '0 0 * * 0'  # Weekly on Sundays at 00:00 UTC
```

## Requirements

- `GITHUB_TOKEN`: Automatically provided by GitHub Actions
- `requests` Python package: Installed automatically in workflow

The system is fully automated and requires no maintenance once set up.
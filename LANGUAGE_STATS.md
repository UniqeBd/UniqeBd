# Language Statistics Auto-Update

This repository contains an automated system that updates both the language usage statistics and the "Languages and Tools" section in the README.md file.

## How it works

1. **GitHub Actions Workflow**: The `.github/workflows/update-language-stats.yml` workflow triggers:
   - When README.md is pushed to the main branch
   - Weekly on Sundays at 00:00 UTC  
   - Manually via workflow dispatch

2. **Language Analysis Script**: The `scripts/update_language_stats.py` script:
   - Fetches all public repositories for the user via GitHub API
   - Analyzes language usage across all repositories (excluding forks)
   - Calculates percentage distribution of languages by bytes
   - Detects frameworks and tools based on repository analysis
   - Updates both the "Most Used Languages" table and "Languages and Tools" section in README.md
   - Commits changes if statistics have changed

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
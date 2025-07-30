# Language Statistics Auto-Update

This repository contains an automated system that updates the language usage statistics in the README.md file.

## How it works

1. **GitHub Actions Workflow**: The `.github/workflows/update-language-stats.yml` workflow triggers:
   - When README.md is pushed to the main branch
   - Weekly on Sundays at 00:00 UTC  
   - Manually via workflow dispatch

2. **Language Analysis Script**: The `scripts/update_language_stats.py` script:
   - Fetches all public repositories for the user via GitHub API
   - Analyzes language usage across all repositories (excluding forks)
   - Calculates percentage distribution of languages by bytes
   - Updates the "Most Used Languages" table in README.md
   - Commits changes if statistics have changed

## Features

- **Automatic Updates**: No manual intervention needed when adding new repositories
- **Rate Limiting**: Built-in delays to respect GitHub API rate limits
- **Language Colors**: Maintains consistent badge colors for popular languages
- **React Detection**: Automatically detects React projects and shows React as a separate language
- **Top Languages**: Shows top 10 most used languages by percentage
- **Fork Exclusion**: Excludes forked repositories from statistics
- **Error Handling**: Graceful handling of API errors and rate limits

## Manual Trigger

You can manually trigger the language statistics update by:
1. Going to the Actions tab in your repository
2. Selecting "Update Language Statistics" workflow
3. Clicking "Run workflow"

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
# Test Language Statistics Workflow

This directory contains testing utilities for the language statistics update workflow.

## 🧪 Test Workflow

The `test-language-stats.yml` workflow is designed to test the language statistics update functionality without affecting the main workflow.

### Features:
- ✅ Manual trigger only (no automatic runs)
- 🔍 Comprehensive debugging and logging
- 🧪 Dry-run mode option
- 📊 Shows detected changes before committing
- 🏷️ Creates test PRs with clear labeling

### How to Run:

#### Option 1: Using PowerShell (Windows)
```powershell
# Test without creating PR (dry-run)
.\trigger-test.ps1 -DryRun

# Test with PR creation
.\trigger-test.ps1
```

#### Option 2: Using Bash (Linux/Mac)
```bash
# Test without creating PR (dry-run)
./trigger-test.sh dry-run

# Test with PR creation
./trigger-test.sh
```

#### Option 3: Manual GitHub UI
1. Go to [GitHub Actions](https://github.com/UniqeBd/UniqeBd/actions)
2. Click on "Test Language Statistics Update"
3. Click "Run workflow"
4. Choose dry-run mode (true/false)
5. Click "Run workflow"

## 🔍 What the Test Does:

1. **Environment Check**: Validates all environment variables and tokens
2. **Script Execution**: Runs the language statistics Python script
3. **Change Detection**: Checks if README.md was modified
4. **Dry-run Option**: Shows what would happen without making changes
5. **PR Creation**: Creates a labeled test PR (if not in dry-run mode)

## 📋 Test Results:

The workflow will show:
- ✅ Whether the script executed successfully
- 📝 What changes were detected
- 🔧 Any errors or issues encountered
- 📊 Debug information about tokens and environment

## 🗑️ Cleanup:

Test PRs are clearly labeled and can be safely closed after reviewing the results. The test branches can also be deleted after testing.

## 🚨 Troubleshooting:

If the test fails, check:
1. GitHub token permissions
2. Repository access
3. Python script syntax
4. Workflow permissions
5. Network connectivity

The test workflow provides detailed error messages to help identify issues.

# PowerShell script to trigger the test language statistics workflow
# Usage: .\trigger-test.ps1 [-DryRun]

param(
    [switch]$DryRun
)

$REPO = "UniqeBd/UniqeBd"
$WORKFLOW = "test-language-stats.yml"

if ($DryRun) {
    $DRY_RUN_VALUE = "true"
    Write-Host "🧪 Triggering TEST workflow in DRY-RUN mode..." -ForegroundColor Yellow
} else {
    $DRY_RUN_VALUE = "false"
    Write-Host "🧪 Triggering TEST workflow (will create PR if changes detected)..." -ForegroundColor Green
}

# Check if GitHub CLI is available
if (Get-Command gh -ErrorAction SilentlyContinue) {
    # Trigger the workflow using GitHub CLI
    gh workflow run $WORKFLOW --repo $REPO --field dry_run=$DRY_RUN_VALUE
    
    Write-Host "✅ Test workflow triggered successfully!" -ForegroundColor Green
    Write-Host "📋 You can monitor the progress at:"
    Write-Host "   https://github.com/$REPO/actions" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⏰ The workflow will take a few minutes to complete."
    
    if ($DryRun) {
        Write-Host "🔍 Running in dry-run mode - no commits or PRs will be created" -ForegroundColor Yellow
    } else {
        Write-Host "🚀 Running in full mode - will create a test PR if changes are detected" -ForegroundColor Green
    }
} else {
    Write-Host "❌ GitHub CLI (gh) not found. Please install it first:" -ForegroundColor Red
    Write-Host "   https://cli.github.com/"
    Write-Host ""
    Write-Host "🔄 Alternative: Manually trigger the workflow from GitHub:" -ForegroundColor Yellow
    Write-Host "   1. Go to https://github.com/$REPO/actions"
    Write-Host "   2. Click on 'Test Language Statistics Update'"
    Write-Host "   3. Click 'Run workflow'"
    Write-Host "   4. Set dry_run to $DRY_RUN_VALUE"
    Write-Host "   5. Click 'Run workflow'"
}

# PowerShell deployment script for Railway
# Make sure you have Railway CLI installed: npm install -g @railway/cli

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Deploying to Railway" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Railway CLI is installed
$railwayCmd = Get-Command railway -ErrorAction SilentlyContinue
if (-not $railwayCmd) {
    Write-Host "❌ Railway CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install it with:"
    Write-Host "  npm install -g @railway/cli" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "✅ Railway CLI found" -ForegroundColor Green
Write-Host ""

# Login check
Write-Host "Checking Railway login status..."
$loginCheck = railway whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Please login to Railway:" -ForegroundColor Yellow
    railway login
}

Write-Host ""
Write-Host "Initializing Railway project..."
railway init

Write-Host ""
Write-Host "Deploying application..."
railway up

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To open your app:" -ForegroundColor Cyan
Write-Host "  railway open" -ForegroundColor Yellow
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Cyan
Write-Host "  railway logs" -ForegroundColor Yellow
Write-Host ""

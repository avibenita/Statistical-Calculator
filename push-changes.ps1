# ============================================
# Git Push Script for Statistical-Calculator
# PowerShell Version with Enhanced Features
# ============================================

param(
    [string]$Message = "",
    [switch]$Force,
    [switch]$Help
)

# Color definitions
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }

# Help message
if ($Help) {
    Write-Info "`nGit Push Utility - Help"
    Write-Host "Usage: .\push-changes.ps1 [-Message <commit_message>] [-Force] [-Help]"
    Write-Host "`nParameters:"
    Write-Host "  -Message    Commit message (if not provided, will prompt)"
    Write-Host "  -Force      Force push (use with caution!)"
    Write-Host "  -Help       Show this help message"
    Write-Host "`nExamples:"
    Write-Host '  .\push-changes.ps1'
    Write-Host '  .\push-changes.ps1 -Message "Fixed bug in calculator"'
    Write-Host '  .\push-changes.ps1 -Message "Update" -Force'
    exit 0
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Git Push Utility" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Navigate to script directory
Set-Location $PSScriptRoot

# Check if git is installed
try {
    git --version | Out-Null
} catch {
    Write-Error "ERROR: Git is not installed or not in PATH!"
    exit 1
}

# Check current branch
$currentBranch = git rev-parse --abbrev-ref HEAD
Write-Info "Current branch: $currentBranch"

# Show current status
Write-Info "`nChecking repository status..."
git status --short

# Check if there are changes
$changes = git status --porcelain
if (-not $changes) {
    Write-Warning "`nNo changes to commit!"
    $continue = Read-Host "Do you want to force push anyway? (y/n)"
    if ($continue -ne 'y') {
        Write-Info "Exiting..."
        exit 0
    }
}

# Get commit message
if (-not $Message) {
    Write-Host "`n"
    $Message = Read-Host "Enter commit message (or press Enter for default)"
    if (-not $Message) {
        $Message = "Update files - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    }
}

# Add all changes
Write-Info "`nAdding all changes..."
git add -A

# Commit changes
Write-Info "Committing with message: '$Message'"
try {
    git commit -m $Message
    if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne 1) {
        throw "Commit failed"
    }
} catch {
    Write-Warning "No changes to commit or commit failed"
}

# Pull latest changes first (to avoid conflicts)
Write-Info "`nPulling latest changes from remote..."
try {
    git pull origin $currentBranch --rebase
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Pull failed - there might be conflicts. Resolve them and run again."
        exit 1
    }
} catch {
    Write-Warning "Pull operation had issues"
}

# Push to GitHub
Write-Info "`nPushing to GitHub..."
try {
    if ($Force) {
        Write-Warning "Force pushing..."
        git push origin $currentBranch --force
    } else {
        git push origin $currentBranch
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n========================================" -ForegroundColor Green
        Write-Success "SUCCESS: Changes pushed to GitHub!"
        Write-Success "Repository: https://github.com/avibenita/Statistical-Calculator"
        Write-Host "========================================`n" -ForegroundColor Green
    } else {
        throw "Push failed"
    }
} catch {
    Write-Host "`n========================================" -ForegroundColor Red
    Write-Error "ERROR: Push failed! Check the error above."
    Write-Host "========================================`n" -ForegroundColor Red
    exit 1
}

# Show final status
Write-Info "`nFinal repository status:"
git status

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


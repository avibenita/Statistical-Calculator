# Erlang C Server - Quick Start Deployment Script (PowerShell)
param(
    [string]$ProjectId = ""
)

Write-Host "Erlang C Server - Google Cloud Functions Quick Start" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# Check if gcloud is installed
Write-Host "Checking Google Cloud CLI..." -ForegroundColor Yellow
try {
    $null = gcloud version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Google Cloud CLI found" -ForegroundColor Green
    } else {
        Write-Host "✗ Google Cloud CLI not working" -ForegroundColor Red
        Write-Host "Please install from: https://cloud.google.com/sdk" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "✗ Google Cloud CLI not found" -ForegroundColor Red
    Write-Host "Please install from: https://cloud.google.com/sdk" -ForegroundColor Yellow
    exit 1
}

# Authentication check
Write-Host "Checking authentication..." -ForegroundColor Yellow
try {
    $activeAccount = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null
    if ($activeAccount) {
        Write-Host "✓ Already authenticated" -ForegroundColor Green
    } else {
        Write-Host "Starting authentication..." -ForegroundColor Yellow
        gcloud auth login
    }
} catch {
    Write-Host "Starting authentication..." -ForegroundColor Yellow
    gcloud auth login
}

# Project setup
if ($ProjectId -eq "") {
    try {
        $currentProject = gcloud config get-value project 2>$null
    } catch {
        $currentProject = $null
    }

    if (-not $currentProject) {
        Write-Host ""
        Write-Host "No project set. Available projects:" -ForegroundColor Yellow
        gcloud projects list --format="table(projectId,name)"
        Write-Host ""
        $ProjectId = Read-Host "Enter your project ID"
        gcloud config set project $ProjectId
    } else {
        Write-Host "Current project: $currentProject" -ForegroundColor Green
        $continue = Read-Host "Continue with this project? (y/n)"
        if ($continue -ne "y") {
            Write-Host "Available projects:" -ForegroundColor Yellow
            gcloud projects list --format="table(projectId,name)"
            Write-Host ""
            $ProjectId = Read-Host "Enter your project ID"
            gcloud config set project $ProjectId
        }
    }
}

Write-Host ""
Write-Host "Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable cloudfunctions.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ APIs enabled" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to enable APIs" -ForegroundColor Red
    exit 1
}

# Check files
Write-Host ""
Write-Host "Checking deployment files..." -ForegroundColor Yellow
$requiredFiles = @("main.py", "requirements.txt")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file found" -ForegroundColor Green
    } else {
        Write-Host "✗ $file not found" -ForegroundColor Red
        Write-Host "Make sure you're in the correct directory" -ForegroundColor Yellow
        exit 1
    }
}

# Deploy
Write-Host ""
Write-Host "Deploying to Google Cloud Functions..." -ForegroundColor Cyan
Write-Host "This may take a few minutes..." -ForegroundColor Yellow

gcloud functions deploy erlang-c-server --runtime python39 --trigger-http --allow-unauthenticated --memory 512MB --timeout 540s --region us-central1 --entry-point erlang_c_server --source .

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Deployment successful!" -ForegroundColor Green
    
    # Get function URL
    $functionUrl = gcloud functions describe erlang-c-server --region=us-central1 --format="value(httpsTrigger.url)" 2>$null
    
    if ($functionUrl) {
        Write-Host ""
        Write-Host "Your function URL:" -ForegroundColor Cyan
        Write-Host $functionUrl -ForegroundColor White
        Write-Host ""
        
        # Test option
        $testNow = Read-Host "Test the deployment now? (y/n)"
        if ($testNow -eq "y") {
            if (Get-Command python -ErrorAction SilentlyContinue) {
                python test_cloud_function.py $functionUrl
            } else {
                Write-Host "Python not found. Test manually:" -ForegroundColor Yellow
                Write-Host "curl $functionUrl/health" -ForegroundColor White
            }
        }
        
        Write-Host ""
        Write-Host "Next Steps:" -ForegroundColor Cyan
        Write-Host "1. Update your HTML file" -ForegroundColor White
        Write-Host "2. Replace localhost:5000 with: $functionUrl" -ForegroundColor White
        Write-Host "3. Test your application" -ForegroundColor White
    }
} else {
    Write-Host ""
    Write-Host "✗ Deployment failed!" -ForegroundColor Red
    Write-Host "Check error messages above" -ForegroundColor Yellow
} 
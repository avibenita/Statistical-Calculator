Write-Host "Erlang C Server - Cloud Functions Deployment" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

Write-Host "Step 1: Checking Google Cloud CLI..." -ForegroundColor Yellow
gcloud version

Write-Host "`nStep 2: Authentication (if needed)..." -ForegroundColor Yellow
Write-Host "Current auth status:" -ForegroundColor Cyan
gcloud auth list

$needAuth = Read-Host "`nDo you need to authenticate? (y/n)"
if ($needAuth -eq "y") {
    gcloud auth login
}

Write-Host "`nStep 3: Project configuration..." -ForegroundColor Yellow
gcloud config list project

$projectId = Read-Host "`nEnter your project ID (or press Enter to use current)"
if ($projectId -ne "") {
    gcloud config set project $projectId
}

Write-Host "`nStep 4: Enabling APIs..." -ForegroundColor Yellow
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com

Write-Host "`nStep 5: Checking files..." -ForegroundColor Yellow
if (Test-Path "main.py") {
    Write-Host "✓ main.py found" -ForegroundColor Green
} else {
    Write-Host "✗ main.py missing" -ForegroundColor Red
    exit 1
}

if (Test-Path "requirements.txt") {
    Write-Host "✓ requirements.txt found" -ForegroundColor Green
} else {
    Write-Host "✗ requirements.txt missing" -ForegroundColor Red
    exit 1
}

Write-Host "`nStep 6: Deploying to Google Cloud Functions..." -ForegroundColor Yellow
Write-Host "This will take a few minutes..." -ForegroundColor Cyan

gcloud functions deploy erlang-c-server --runtime python39 --trigger-http --allow-unauthenticated --memory 512MB --timeout 540s --region us-central1 --entry-point erlang_c_server --source .

Write-Host "`nStep 7: Getting function URL..." -ForegroundColor Yellow
$url = gcloud functions describe erlang-c-server --region=us-central1 --format="value(httpsTrigger.url)"

Write-Host "`nDeployment Complete!" -ForegroundColor Green
Write-Host "Function URL: $url" -ForegroundColor Cyan
Write-Host "`nNext: Update your HTML file to use this URL instead of localhost:5000" -ForegroundColor Yellow 
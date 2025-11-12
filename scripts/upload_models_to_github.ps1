# PowerShell script to help upload models to GitHub Releases
# Run this after generating models from the notebook

Write-Host "📦 Preparing models for GitHub Release..." -ForegroundColor Cyan

# Check if models directory exists
if (-not (Test-Path "models")) {
    Write-Host "❌ Error: models/ directory not found" -ForegroundColor Red
    Write-Host "Please run the notebook to generate models first" -ForegroundColor Yellow
    exit 1
}

# Check if all model files exist
$RequiredFiles = @("scaler.pkl", "label_encoders.pkl", "kmeans_model.pkl", "feature_info.pkl", "cluster_profiles.pkl")
$MissingFiles = @()

foreach ($file in $RequiredFiles) {
    if (-not (Test-Path "models\$file")) {
        $MissingFiles += $file
    }
}

if ($MissingFiles.Count -ne 0) {
    Write-Host "❌ Missing model files:" -ForegroundColor Red
    foreach ($file in $MissingFiles) {
        Write-Host "   - $file" -ForegroundColor Yellow
    }
    Write-Host "Please run the notebook to generate all models" -ForegroundColor Yellow
    exit 1
}

# Create release directory
$ReleaseDir = "models-release"
if (Test-Path $ReleaseDir) {
    Remove-Item $ReleaseDir -Recurse -Force
}
New-Item -ItemType Directory -Path $ReleaseDir | Out-Null

# Copy models
Write-Host "📋 Copying model files..." -ForegroundColor Cyan
Copy-Item "models\*.pkl" -Destination $ReleaseDir

# Create zip file
Write-Host "📦 Creating zip archive..." -ForegroundColor Cyan
Compress-Archive -Path "$ReleaseDir\*.pkl" -DestinationPath "models-release.zip" -Force

Write-Host ""
Write-Host "✅ Models prepared for release!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to: https://github.com/likhitha281/DiabetesHospitalReadmission/releases/new"
Write-Host "2. Create a new release (e.g., tag: v1.0.0-models)"
Write-Host "3. Upload models-release.zip OR upload individual .pkl files"
Write-Host "4. Publish the release"
Write-Host "5. Update MODEL_BASE_URL in api/predict.py or Vercel environment variables"
Write-Host ""
Write-Host "Release URL format will be:" -ForegroundColor Yellow
Write-Host "https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/{filename}"


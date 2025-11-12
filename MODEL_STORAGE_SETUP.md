# Model Storage Setup Guide

Since Vercel has a 250MB limit for serverless functions, we need to store models externally. Here are several options:

## Option 1: GitHub Releases (Easiest - Recommended)

### Step 1: Create a GitHub Release

1. Go to your GitHub repository: `https://github.com/likhitha281/DiabetesHospitalReadmission`
2. Click **"Releases"** → **"Create a new release"**
3. Create a new tag (e.g., `v1.0.0-models`)
4. Upload all 5 model files:
   - `scaler.pkl`
   - `label_encoders.pkl`
   - `kmeans_model.pkl`
   - `feature_info.pkl`
   - `cluster_profiles.pkl`
5. Publish the release

### Step 2: Update API Code

The `api/predict.py` is already configured to download from GitHub releases. The URL format is:
```
https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/{filename}
```

Update the tag name in `api/predict.py` if needed, or set it via environment variable.

### Step 3: Set Environment Variable (Optional)

In Vercel dashboard:
1. Go to **Settings** → **Environment Variables**
2. Add: `MODEL_BASE_URL` = `https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/`

## Option 2: Google Drive (Free)

### Step 1: Upload Models to Google Drive

1. Upload all 5 `.pkl` files to Google Drive
2. Right-click each file → **Get link** → **Anyone with the link**
3. Copy the file IDs from the URLs

### Step 2: Update API Code

Replace the download URLs in `api/predict.py`:

```python
MODEL_FILES = {
    'scaler.pkl': 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_1',
    'label_encoders.pkl': 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_2',
    'kmeans_model.pkl': 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_3',
    'feature_info.pkl': 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_4',
    'cluster_profiles.pkl': 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID_5',
}
```

## Option 3: AWS S3 (Production)

### Step 1: Create S3 Bucket

1. Go to AWS S3 console
2. Create a new bucket (e.g., `diabetes-models`)
3. Upload all 5 model files
4. Make files publicly readable (or use signed URLs)

### Step 2: Update API Code

```python
MODEL_BASE_URL = 'https://diabetes-models.s3.amazonaws.com/models/'
```

## Option 4: Dropbox (Simple)

### Step 1: Upload to Dropbox

1. Upload models to Dropbox
2. Get shareable links
3. Replace `www.dropbox.com` with `dl.dropboxusercontent.com` in URLs

### Step 2: Update API Code

Use direct Dropbox download URLs in `api/predict.py`

## Option 5: Deploy Python API Separately (Best for Large Models)

If models are very large (>100MB each), deploy the Python API separately:

### Using Railway (Recommended)

1. Create `app.py` (Flask/FastAPI wrapper)
2. Deploy to Railway: https://railway.app
3. Update frontend to call Railway URL

### Using Render

1. Create `app.py`
2. Deploy to Render: https://render.com
3. Update frontend API URL

## Quick Setup Script

Run this to prepare models for GitHub release:

```bash
# Create a zip file with all models
cd models
zip -r ../models-release.zip *.pkl
cd ..

# Or use PowerShell on Windows:
Compress-Archive -Path models\*.pkl -DestinationPath models-release.zip
```

Then upload `models-release.zip` to GitHub release and extract there, or upload individual files.

## Testing Model Downloads

Test if models download correctly:

```python
import urllib.request
url = "YOUR_MODEL_URL"
urllib.request.urlretrieve(url, "test.pkl")
```

## Current Configuration

The `api/predict.py` is configured for **GitHub Releases** by default. To use it:

1. Create a GitHub release with your model files
2. Update the release tag in the code (or use environment variable)
3. Models will download automatically on first API call
4. Models are cached in temp directory for subsequent calls

## Troubleshooting

### Issue: Models won't download

- Check URLs are publicly accessible
- Verify file permissions
- Check Vercel function logs for download errors

### Issue: Download too slow

- Use CDN (CloudFlare, etc.)
- Compress models before uploading
- Consider deploying Python API separately

### Issue: Still hitting size limits

- Models might be cached in deployment
- Use separate Python API service (Railway/Render)
- Compress models more aggressively


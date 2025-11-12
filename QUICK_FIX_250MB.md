# Quick Fix: 250MB Vercel Limit Error

## Problem
Vercel has a 250MB limit for serverless functions. Your model files exceed this limit.

## Solution: Use External Storage

I've updated `api/predict.py` to download models from external storage instead of bundling them.

## Quick Setup (5 minutes)

### Step 1: Upload Models to GitHub Releases

1. **Go to your GitHub repository**: https://github.com/likhitha281/DiabetesHospitalReadmission

2. **Create a new release**:
   - Click **"Releases"** → **"Create a new release"**
   - Tag: `v1.0.0-models` (or any version)
   - Title: "Model Files for Vercel Deployment"
   - Description: "Model files for cluster prediction API"

3. **Upload model files**:
   - Drag and drop all 5 files from your `models/` folder:
     - `scaler.pkl`
     - `label_encoders.pkl`
     - `kmeans_model.pkl`
     - `feature_info.pkl`
     - `cluster_profiles.pkl`
   - Click **"Publish release"**

### Step 2: Update the Release Tag in Code

Open `api/predict.py` and update line 18-20:

```python
MODEL_BASE_URL = os.environ.get(
    'MODEL_BASE_URL',
    'https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/'
)
```

Replace `v1.0.0-models` with your actual release tag.

### Step 3: Remove Models from Git (Important!)

The models are now excluded via `.gitignore`, but if they're already committed:

```bash
# Remove models from Git (but keep local files)
git rm --cached models/*.pkl
git commit -m "Remove model files from Git (use external storage)"
git push
```

### Step 4: Deploy to Vercel

```bash
git add .
git commit -m "Use external model storage"
git push
```

Vercel will automatically redeploy. The function will download models on first request.

## How It Works

1. **First API call**: Downloads models from GitHub releases to temp directory
2. **Subsequent calls**: Uses cached models (faster)
3. **No size limit**: Models aren't bundled with the function

## Alternative: Use Environment Variable

Instead of hardcoding the URL, set it in Vercel:

1. Go to Vercel dashboard → Your project → **Settings** → **Environment Variables**
2. Add:
   - Name: `MODEL_BASE_URL`
   - Value: `https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/`
3. Redeploy

## Testing

After deployment, test the API:

```bash
curl -X POST https://your-app.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": {"time_in_hospital": 3, "num_lab_procedures": 43, ...}}'
```

## Troubleshooting

### Models won't download
- Check GitHub release is public
- Verify file names match exactly
- Check Vercel function logs for download errors

### Still getting size errors
- Make sure `models/` folder is not in the deployment
- Check `.gitignore` includes `models/*.pkl`
- Verify models are removed from Git history

### Download too slow
- First request will be slower (downloading models)
- Subsequent requests use cached models
- Consider using a CDN for faster downloads

## Other Storage Options

If GitHub releases don't work, see `MODEL_STORAGE_SETUP.md` for:
- Google Drive
- AWS S3
- Dropbox
- Separate Python API deployment


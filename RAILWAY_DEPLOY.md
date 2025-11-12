# Deploy Python API to Railway (5 Minutes)

## Why Railway?

Vercel has a 250MB limit. Python ML libraries (pandas, numpy, scikit-learn) exceed this. Railway has no such limit.

## Quick Setup

### Step 1: Push Code to GitHub

Your code is already on GitHub, so skip this if already done.

### Step 2: Deploy to Railway

1. **Go to**: https://railway.app
2. **Sign up** (free with GitHub)
3. **New Project** → **Deploy from GitHub repo**
4. **Select**: `DiabetesHospitalReadmission`
5. Railway will auto-detect Python

### Step 3: Configure Railway

1. **Set Start Command**:
   - Go to Settings → Deploy
   - Start Command: `python app.py`

2. **Add Environment Variable**:
   - Go to Variables
   - Add: `MODEL_BASE_URL` = `https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/`
   - (Update tag if different)

3. **Get Your API URL**:
   - Railway will give you a URL like: `https://your-app.railway.app`
   - Copy this URL

### Step 4: Update Vercel Frontend

1. **Go to Vercel Dashboard** → Your Project → Settings → Environment Variables
2. **Add**: 
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://your-app.railway.app` (your Railway URL)
3. **Redeploy** Vercel

### Step 5: Test

1. Visit your Vercel URL
2. Fill in the form
3. Click "Predict Cluster"
4. Should work! 🎉

## Alternative: Render

If Railway doesn't work, use Render:

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - Build Command: (leave empty)
   - Start Command: `python app.py`
5. Add environment variable: `MODEL_BASE_URL`
6. Deploy

## Cost

- **Railway**: Free tier (500 hours/month), then $5/month
- **Render**: Free tier available
- **Vercel**: Still free for frontend

## Troubleshooting

### API returns 404

- Check Railway deployment is "Live"
- Verify start command is `python app.py`
- Check Railway logs for errors

### Models not downloading

- Verify `MODEL_BASE_URL` environment variable is set
- Check GitHub release exists and is public
- Check Railway logs for download errors

### CORS errors

- `app.py` already has CORS enabled
- If issues persist, check Railway logs

## What's Happening

- **Frontend**: Deployed on Vercel (fast, free)
- **API**: Deployed on Railway (handles ML, no size limit)
- **Models**: Downloaded from GitHub Releases (on first request)

This is the recommended architecture for ML apps!


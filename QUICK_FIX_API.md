# Quick Fix: "Python prediction service not available"

## The Problem

The frontend is trying to call the Python API, but it's not configured yet. We removed Python from Vercel (to fix 250MB error) and need to deploy it separately.

## Solution: Deploy Python API to Railway (5 minutes)

### Step 1: Deploy to Railway

1. **Go to**: https://railway.app
2. **Sign up** with GitHub (free)
3. **Click**: "New Project" → "Deploy from GitHub repo"
4. **Select**: `DiabetesHospitalReadmission`
5. Railway will auto-detect Python

### Step 2: Configure Railway

1. **Set Start Command**:
   - Click on your service
   - Go to **Settings** → **Deploy**
   - Start Command: `python app.py`
   - Click **Save**

2. **Add Environment Variable**:
   - Go to **Variables** tab
   - Click **+ New Variable**
   - Name: `MODEL_BASE_URL`
   - Value: `https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/`
   - (Update the tag if your release has a different tag)
   - Click **Add**

3. **Get Your API URL**:
   - Railway will give you a URL like: `https://your-app-name.railway.app`
   - Copy this URL (you'll need it in Step 3)

### Step 3: Connect Vercel to Railway

1. **Go to Vercel Dashboard**: https://vercel.com
2. **Select your project**: `diabetes-hospital-readmission`
3. **Go to**: Settings → Environment Variables
4. **Add new variable**:
   - Name: `RAILWAY_API_URL`
   - Value: `https://your-app-name.railway.app` (your Railway URL from Step 2)
   - Environment: Production, Preview, Development (select all)
   - Click **Save**

5. **Redeploy**:
   - Go to **Deployments** tab
   - Click **"..."** on latest deployment
   - Click **Redeploy**
   - Make sure **"Use existing Build Cache"** is OFF
   - Click **Redeploy**

### Step 4: Test

1. Wait for Vercel redeploy to complete
2. Visit your Vercel URL
3. Fill in the form
4. Click "Predict Cluster"
5. Should work! 🎉

## Alternative: Use Render Instead of Railway

If Railway doesn't work, use Render:

1. Go to: https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - Build Command: (leave empty)
   - Start Command: `python app.py`
5. Add environment variable: `MODEL_BASE_URL`
6. Deploy
7. Copy Render URL and add to Vercel as `RAILWAY_API_URL`

## Troubleshooting

### Still getting error after setup?

1. **Check Railway is running**:
   - Go to Railway dashboard
   - Check service status is "Active"
   - Check logs for errors

2. **Test Railway API directly**:
   ```bash
   curl -X POST https://your-app.railway.app/predict \
     -H "Content-Type: application/json" \
     -d '{"data": {"time_in_hospital": 3, ...}}'
   ```

3. **Check Vercel environment variable**:
   - Make sure `RAILWAY_API_URL` is set
   - Make sure it's the full URL (with https://)
   - Redeploy after adding variable

4. **Check Railway logs**:
   - Railway dashboard → Your service → Logs
   - Look for errors when API is called

## What's Happening

- **Frontend (Vercel)**: Handles the UI
- **API Route (Vercel)**: `/api/predict` proxies to Railway
- **Python API (Railway)**: Does the actual prediction
- **Models**: Downloaded from GitHub Releases

This architecture separates concerns and avoids Vercel's size limits!


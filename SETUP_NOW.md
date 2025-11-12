# Setup Railway API - Do This Now

## Current Status

✅ Vercel frontend is deployed  
❌ Python API is not deployed yet  
❌ Environment variable not set in Vercel

## Quick Setup (10 minutes)

### Step 1: Deploy to Railway (5 min)

1. **Go to**: https://railway.app
2. **Sign up** with GitHub (it's free)
3. **Click**: "New Project"
4. **Select**: "Deploy from GitHub repo"
5. **Choose**: `DiabetesHospitalReadmission`
6. **Wait**: Railway will auto-detect Python and start deploying

### Step 2: Configure Railway (2 min)

Once Railway detects your repo:

1. **Click on your service** (the one that says "Python" or "Web Service")

2. **Set Start Command**:
   - Click **Settings** tab
   - Scroll to **Deploy**
   - **Start Command**: `python app.py`
   - Click **Save**

3. **Add Environment Variable**:
   - Click **Variables** tab
   - Click **+ New Variable**
   - **Name**: `MODEL_BASE_URL`
   - **Value**: `https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/`
   - Click **Add**

4. **Get Your URL**:
   - Railway will generate a URL like: `https://your-app-name.up.railway.app`
   - Or go to **Settings** → **Domains** to see your URL
   - **COPY THIS URL** - you'll need it next!

### Step 3: Connect Vercel to Railway (3 min)

1. **Go to Vercel**: https://vercel.com
2. **Select your project**: `diabetes-hospital-readmission`
3. **Go to**: **Settings** → **Environment Variables**
4. **Click**: **Add New**
5. **Fill in**:
   - **Name**: `RAILWAY_API_URL`
   - **Value**: Paste your Railway URL (from Step 2)
   - **Environments**: Check all (Production, Preview, Development)
   - Click **Save**

6. **Redeploy**:
   - Go to **Deployments** tab
   - Click the **"..."** menu (three dots) on the latest deployment
   - Click **Redeploy**
   - **IMPORTANT**: Uncheck "Use existing Build Cache"
   - Click **Redeploy**

7. **Wait** for redeploy to complete (1-2 minutes)

### Step 4: Test

1. Visit your Vercel URL
2. Fill in the form
3. Click "Predict Cluster"
4. Should work! 🎉

## Troubleshooting

### Railway deployment fails

- Check Railway logs (click on your service → Logs tab)
- Make sure `app.py` exists in your repo
- Make sure `requirements.txt` exists

### Railway URL not working

- Check Railway service status is "Active"
- Test the URL directly: `https://your-app.railway.app/health`
- Should return: `{"status":"ok"}`

### Still getting error after setup

1. **Verify environment variable**:
   - Vercel Dashboard → Settings → Environment Variables
   - Make sure `RAILWAY_API_URL` exists
   - Make sure value is correct (with https://)

2. **Check Railway is running**:
   - Railway dashboard → Your service
   - Status should be "Active"
   - Check logs for errors

3. **Test Railway API directly**:
   ```bash
   curl https://your-app.railway.app/health
   ```
   Should return: `{"status":"ok"}`

4. **Redeploy Vercel**:
   - Make sure you redeployed AFTER adding the environment variable
   - Environment variables only apply to new deployments

## Alternative: Use Render Instead

If Railway doesn't work:

1. Go to: https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - **Start Command**: `python app.py`
5. Add environment variable: `MODEL_BASE_URL`
6. Deploy
7. Copy Render URL and add to Vercel as `RAILWAY_API_URL`

## Need Help?

If you're stuck:
1. Share a screenshot of Railway dashboard
2. Share Railway logs (if any errors)
3. Share Vercel environment variables (hide the URL if sensitive)


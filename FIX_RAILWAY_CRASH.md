# Fix Railway Container Crash

## Problem

Railway logs show the Flask app starts but the container stops immediately. This is likely due to:
1. Import errors when loading prediction functions
2. Missing dependencies
3. Port configuration issues

## Solution

I've updated `app.py` to:
- Better handle imports
- Add error logging
- Use correct port (8080 for Railway)
- Add debug output

## Steps to Fix

### Step 1: Push Updated Code

The code is already updated. Just make sure it's pushed:

```bash
git add app.py
git commit -m "Fix Railway import errors and add logging"
git push
```

Railway will automatically redeploy.

### Step 2: Check Railway Configuration

1. **Go to Railway Dashboard**
2. **Check Environment Variables**:
   - `MODEL_BASE_URL` should be set
   - `PORT` should be set automatically by Railway (usually 8080)

3. **Check Start Command**:
   - Should be: `python app.py`
   - Not: `flask run` or `gunicorn`

### Step 3: Check Railway Logs Again

After Railway redeploys, check logs for:
- ✅ "Successfully imported prediction functions" or "Successfully loaded prediction functions"
- ✅ "Starting Flask app on port 8080"
- ❌ Any import errors or tracebacks

### Step 4: Test Railway Health Endpoint

Once Railway is running, test:
```
https://your-railway-url.railway.app/health
```

Should return: `{"status":"ok"}`

## Common Issues

### Issue: Import Error

**Symptom**: Logs show "ImportError" or "ModuleNotFoundError"

**Fix**:
1. Check `api/predict.py` exists in your repo
2. Check `api/requirements.txt` has all dependencies
3. Railway should install dependencies automatically

### Issue: Models Not Found

**Symptom**: Logs show "Error loading models" or "Failed to download"

**Fix**:
1. Verify `MODEL_BASE_URL` is set in Railway
2. Check GitHub release exists and is public
3. Test download URL in browser

### Issue: Port Mismatch

**Symptom**: App starts but Railway can't connect

**Fix**:
- Railway sets `PORT` environment variable automatically
- Updated `app.py` to use `PORT` or default to 8080
- Should work now

## Verify It's Working

1. **Check Railway Logs**:
   - Should see "Starting Flask app on port 8080"
   - Should see "Successfully imported prediction functions"
   - No errors

2. **Test Health Endpoint**:
   - Visit: `https://your-railway-url.railway.app/health`
   - Should return: `{"status":"ok"}`

3. **Test from Vercel**:
   - Visit: `https://diabetes-hospital-readmission.vercel.app/api/test-railway`
   - Should show Railway is reachable

4. **Test Prediction**:
   - Use the dashboard
   - Should work now!

## Still Crashing?

If Railway still crashes after redeploy:

1. **Check Full Logs**:
   - Railway dashboard → Your service → Logs
   - Look for the last error before container stops
   - Share the error message

2. **Check Requirements**:
   - Make sure `requirements.txt` in root has Flask
   - Make sure `api/requirements.txt` has ML libraries

3. **Try Manual Start**:
   - Railway dashboard → Your service → Settings
   - Try different start commands:
     - `python app.py`
     - `python3 app.py`
     - `flask run --host=0.0.0.0 --port=$PORT`


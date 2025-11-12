# Diagnose Railway Connection Issue

## Quick Test

1. **Visit this URL in your browser**:
   ```
   https://diabetes-hospital-readmission.vercel.app/api/test-railway
   ```
   
   This will show you:
   - If `RAILWAY_API_URL` is set
   - What the URL value is
   - If Railway API is reachable
   - Any connection errors

## Common Issues & Fixes

### Issue 1: Railway URL Not Set

**Symptom**: Test page shows "RAILWAY_API_URL not set"

**Fix**:
1. Go to Vercel Dashboard → Settings → Environment Variables
2. Check if `RAILWAY_API_URL` exists
3. If not, add it with your Railway URL
4. Redeploy Vercel

### Issue 2: Railway Service Not Running

**Symptom**: Test page shows "Cannot connect to Railway API"

**Fix**:
1. Go to Railway dashboard: https://railway.app
2. Check if your service status is "Active"
3. If it says "Sleeping" or "Stopped":
   - Click on the service
   - Click "Deploy" or "Restart"
4. Wait for it to become "Active"

### Issue 3: Wrong Railway URL

**Symptom**: Test page shows connection error

**Fix**:
1. Go to Railway dashboard
2. Click on your service
3. Go to Settings → Domains
4. Copy the correct URL (should be like `https://xxx.up.railway.app`)
5. Update in Vercel environment variables
6. Redeploy Vercel

### Issue 4: Railway Service Has Errors

**Symptom**: Railway is running but API doesn't work

**Fix**:
1. Go to Railway dashboard
2. Click on your service
3. Go to Logs tab
4. Look for error messages
5. Common issues:
   - Missing `MODEL_BASE_URL` environment variable
   - Models not downloading from GitHub
   - Python import errors

## Step-by-Step Diagnosis

### Step 1: Check Environment Variable

1. Go to Vercel Dashboard
2. Your Project → Settings → Environment Variables
3. Look for `RAILWAY_API_URL`
4. Verify the value is correct (should be a Railway URL)

### Step 2: Check Railway Status

1. Go to Railway dashboard
2. Check if service exists
3. Check if status is "Active"
4. If sleeping, wake it up

### Step 3: Test Railway Directly

1. Copy your Railway URL from Vercel environment variables
2. Open in browser: `https://your-railway-url.railway.app/health`
3. Should return: `{"status":"ok"}`
4. If not, Railway has issues

### Step 4: Check Railway Logs

1. Railway dashboard → Your service → Logs
2. Look for:
   - Startup errors
   - Import errors
   - Model download errors
   - Any Python tracebacks

## Quick Fixes

### Fix 1: Restart Railway Service

1. Railway dashboard → Your service
2. Click "..." menu
3. Click "Restart"
4. Wait for it to become active
5. Test again

### Fix 2: Verify Railway Configuration

Make sure in Railway:
- ✅ Start Command: `python app.py`
- ✅ Environment Variable: `MODEL_BASE_URL` is set
- ✅ Service is Active (not sleeping)

### Fix 3: Re-add Environment Variable in Vercel

1. Delete `RAILWAY_API_URL` from Vercel
2. Add it again with correct Railway URL
3. Make sure to select all environments
4. Redeploy Vercel

## Test Commands

### Test Railway Health Endpoint

```bash
# Replace with your Railway URL
curl https://your-app.railway.app/health
```

Should return: `{"status":"ok"}`

### Test Railway Predict Endpoint

```bash
curl -X POST https://your-app.railway.app/predict \
  -H "Content-Type: application/json" \
  -d '{"data": {"time_in_hospital": 3, "num_lab_procedures": 43, "num_procedures": 0, "num_medications": 16, "number_outpatient": 0, "number_emergency": 0, "number_inpatient": 0, "number_diagnoses": 9, "race": "Caucasian", "gender": "Female", "age": "[50-60)", "admission_type_id": 1, "discharge_disposition_id": 1, "admission_source_id": 7, "max_glu_serum": "None", "A1Cresult": "None", "diabetesMed": "No", "metformin": "No", "repaglinide": "No", "nateglinide": "No", "glimepiride": "No", "glipizide": "No", "glyburide": "No", "pioglitazone": "No", "rosiglitazone": "No", "insulin": "No"}}'
```

## Still Not Working?

Share:
1. Output from `/api/test-railway` endpoint
2. Railway service status (Active/Sleeping/Error)
3. Railway logs (any errors)
4. Railway URL you're using


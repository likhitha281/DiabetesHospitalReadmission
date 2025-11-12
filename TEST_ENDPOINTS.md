# Test Endpoints - Step by Step

## Prerequisites

Before testing, make sure:
- ✅ Vercel deployment is "Ready" (green checkmark)
- ✅ Railway service is "Active"
- ✅ `RAILWAY_API_URL` is set in Vercel environment variables

## Step 1: Find Your Vercel URL

1. Go to: https://vercel.com
2. Click on your project
3. Look at the top - you'll see your URL
4. It should be: `https://diabetes-hospital-readmission.vercel.app` (or similar)

## Step 2: Test Endpoints in Order

### Test 1: Main Dashboard
**URL**: `https://diabetes-hospital-readmission.vercel.app`

**Expected**: Dashboard with input forms

**If error**: Check Vercel deployment status

---

### Test 2: Railway Connection Test
**URL**: `https://diabetes-hospital-readmission.vercel.app/api/test-railway`

**Expected**: JSON showing Railway connection status

**What to look for**:
- `railwayUrlConfigured: true` ✅
- `status: "SUCCESS"` ✅
- `railwayHealth: {"status":"ok"}` ✅

**If error**: 
- Check if `RAILWAY_API_URL` is set in Vercel
- Check Railway service is running

---

### Test 3: Railway Health (Direct)
**URL**: `https://your-railway-url.railway.app/health`

**Expected**: `{"status":"ok"}`

**If error**: Railway service might not be running

---

### Test 4: Full Prediction
**URL**: `https://diabetes-hospital-readmission.vercel.app`

**Action**: Fill form and click "Predict Cluster"

**Expected**: Cluster prediction result

**If error**: Check browser console and network tab

## Troubleshooting

### "This site can't be reached"

**Check**:
1. Are you using the full URL with `https://`?
2. Is the deployment live in Vercel?
3. Did you type the URL correctly?

**Fix**:
1. Go to Vercel dashboard
2. Copy the exact URL from there
3. Make sure it includes `.vercel.app`

### "DNS_PROBE_FINISHED_NXDOMAIN"

**Meaning**: Domain doesn't exist

**Fix**:
1. Verify you're using the correct Vercel URL
2. Check deployment is live
3. Try accessing from Vercel dashboard (click "Visit" button)

### Railway Connection Fails

**Check**:
1. Railway service status (should be "Active")
2. `RAILWAY_API_URL` in Vercel environment variables
3. Railway URL is correct (starts with `https://`)

## Quick Checklist

- [ ] Vercel deployment is "Ready"
- [ ] Railway service is "Active"
- [ ] `RAILWAY_API_URL` is set in Vercel
- [ ] Using correct Vercel URL (with .vercel.app)
- [ ] Railway health endpoint works
- [ ] Vercel test-railway endpoint works


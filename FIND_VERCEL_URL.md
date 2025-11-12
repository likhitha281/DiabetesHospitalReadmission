# How to Find Your Vercel URL

## Step 1: Get Your Vercel Deployment URL

1. **Go to Vercel Dashboard**: https://vercel.com
2. **Sign in** to your account
3. **Click on your project**: `diabetes-hospital-readmission` (or similar name)
4. **Look at the top** of the project page - you'll see your deployment URL

Your URL should look like:
- `https://diabetes-hospital-readmission.vercel.app`
- Or `https://diabetes-hospital-readmission-[your-username].vercel.app`

## Step 2: Test the Correct URLs

### Test 1: Main Dashboard
```
https://diabetes-hospital-readmission.vercel.app
```
Should show the dashboard with input forms.

### Test 2: Railway Connection Test
```
https://diabetes-hospital-readmission.vercel.app/api/test-railway
```
Should show Railway connection status.

### Test 3: Health Check (if Railway is set up)
```
https://your-railway-url.railway.app/health
```
Should return: `{"status":"ok"}`

## Common Issues

### Issue: "This site can't be reached"

**Causes**:
1. Wrong URL (missing .vercel.app)
2. Deployment not live
3. Typo in URL

**Fix**:
1. Go to Vercel dashboard
2. Check if latest deployment shows "Ready" (green checkmark)
3. Click on the deployment
4. Copy the exact URL shown
5. Use that URL

### Issue: DNS_PROBE_FINISHED_NXDOMAIN

This means the domain doesn't exist. Check:
1. Are you using the correct Vercel URL?
2. Is the deployment actually live?
3. Did you type the URL correctly?

## Quick Check

1. **Vercel Dashboard** → Your Project
2. **Deployments** tab
3. Find the latest deployment
4. Status should be "Ready" ✅
5. Click on it to see the URL
6. Copy that exact URL

## Alternative: Check from Vercel CLI

If you have Vercel CLI installed:
```bash
vercel ls
```
This will show all your deployments and their URLs.


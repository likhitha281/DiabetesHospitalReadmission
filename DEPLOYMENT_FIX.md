# Fix Vercel Deployment - Dashboard Not Showing

If you're seeing the old placeholder page instead of the interactive dashboard, follow these steps:

## Quick Fix Steps

### 1. Manual Redeploy on Vercel

1. Go to [vercel.com](https://vercel.com) and log in
2. Find your project: `diabetes-hospital-readmission`
3. Click on the project
4. Go to the **"Deployments"** tab
5. Find the latest deployment
6. Click the **"..."** menu (three dots) next to it
7. Select **"Redeploy"**
8. Check **"Use existing Build Cache"** = OFF (to force a fresh build)
9. Click **"Redeploy"**

### 2. Clear Vercel Cache

If redeploy doesn't work:

1. In Vercel dashboard, go to **Settings** → **General**
2. Scroll to **"Build & Development Settings"**
3. Clear build cache (if option available)
4. Or delete and recreate the project

### 3. Force Push to Trigger Auto-Deploy

```bash
# Make a small change to trigger redeploy
git commit --allow-empty -m "Trigger Vercel redeploy"
git push
```

### 4. Check Build Logs

1. In Vercel dashboard, go to your deployment
2. Click on the deployment to see build logs
3. Look for any errors or warnings
4. Common issues:
   - Missing dependencies
   - Build errors
   - Python runtime issues

### 5. Verify Files Are Correct

Make sure these files exist and have the correct content:

- ✅ `pages/index.js` - Should have "Patient Cluster Predictor" title
- ✅ `api/predict.py` - Python prediction function
- ✅ `vercel.json` - Configuration file
- ✅ `package.json` - Dependencies

### 6. Test Locally First

Before deploying, test locally:

```bash
npm install
npm run dev
```

Visit `http://localhost:3000` - you should see the interactive dashboard.

If it works locally but not on Vercel, it's a deployment issue.

### 7. Check Vercel Function Logs

1. Go to Vercel dashboard
2. Click on your project
3. Go to **"Functions"** tab
4. Check for any errors in `api/predict.py`

### 8. Alternative: Delete and Recreate

If nothing works:

1. Delete the project on Vercel
2. Reconnect to GitHub
3. Deploy fresh

## Common Issues

### Issue: Still seeing old page after redeploy

**Solution**: 
- Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
- Clear browser cache
- Try incognito/private mode

### Issue: Build fails

**Solution**:
- Check `package.json` has all dependencies
- Verify `api/requirements.txt` exists
- Check build logs for specific errors

### Issue: Python function not working

**Solution**:
- Verify `api/predict.py` exists
- Check `vercel.json` has Python build configuration
- Ensure models are in `models/` directory (if not using external storage)

## Verification Checklist

After redeploy, verify:

- [ ] Dashboard shows "🏥 Patient Cluster Predictor" title
- [ ] Three columns of input forms are visible
- [ ] "🔮 Predict Cluster" button is present
- [ ] No console errors in browser
- [ ] API endpoint `/api/predict` is accessible

## Still Not Working?

If none of these work:

1. **Check Vercel Status**: [status.vercel.com](https://status.vercel.com)
2. **Contact Support**: Vercel dashboard → Help → Contact Support
3. **Review Logs**: Check both build logs and function logs

## Quick Test

After redeploy, test the API directly:

```bash
curl -X POST https://diabetes-hospital-readmission.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": {"time_in_hospital": 3, "num_lab_procedures": 43, ...}}'
```

If this works but the frontend doesn't, it's a frontend issue.
If this doesn't work, it's a backend/API issue.


# Vercel Deployment Checklist

Use this checklist to ensure everything is set up correctly:

## Pre-Deployment

- [ ] **Models Generated**: Run notebook and generate all 5 model files
- [ ] **Models Uploaded**: Upload to GitHub Releases (see QUICK_FIX_250MB.md)
- [ ] **Models Excluded**: Models are in `.gitignore` and NOT in Git
- [ ] **GitHub Release**: Release exists with all 5 `.pkl` files

## Files Check

- [ ] `api/predict.py` - Python function exists
- [ ] `api/requirements.txt` - Python dependencies listed
- [ ] `pages/index.js` - Frontend dashboard exists
- [ ] `vercel.json` - Configuration file exists
- [ ] `package.json` - Node.js dependencies listed
- [ ] `.gitignore` - Excludes `models/*.pkl`

## Configuration

- [ ] `vercel.json` has Python build configuration
- [ ] `MODEL_BASE_URL` in `api/predict.py` matches your GitHub release
- [ ] Or `MODEL_BASE_URL` set as Vercel environment variable

## Deployment

- [ ] Code pushed to GitHub
- [ ] Vercel connected to GitHub repo
- [ ] Deployment triggered (automatic or manual)
- [ ] Build completes without errors
- [ ] No 250MB limit errors

## Testing

- [ ] Dashboard loads at Vercel URL
- [ ] Shows "🏥 Patient Cluster Predictor" (not old page)
- [ ] Input forms are visible
- [ ] API endpoint `/api/predict` is accessible
- [ ] Prediction works (may be slow on first call)

## If Still Failing

1. Check build logs in Vercel dashboard
2. Check function logs for runtime errors
3. Verify GitHub release URLs are accessible
4. See TROUBLESHOOTING_VERCEL.md for detailed solutions


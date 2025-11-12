# Troubleshooting Vercel Deployment Issues

## Common Issues and Solutions

### Issue 1: Still Getting 250MB Error

**Symptoms**: Build fails with "exceeded the unzipped maximum size of 250 MB"

**Solutions**:

1. **Check if models are still in the deployment**:
   ```bash
   # Make sure models are in .gitignore
   git check-ignore models/*.pkl
   ```

2. **Remove models from Git history** (if they were committed):
   ```bash
   git rm -r --cached models/
   git commit -m "Remove models from Git"
   git push
   ```

3. **Verify .gitignore**:
   ```
   models/*.pkl
   models-release/
   models-release.zip
   ```

4. **Check Vercel build logs**:
   - Go to Vercel dashboard → Your project → Deployments
   - Click on failed deployment
   - Check build logs for file sizes

### Issue 2: Python Function Not Working

**Symptoms**: API returns 500 errors or function not found

**Solutions**:

1. **Check Python runtime**:
   - Vercel should auto-detect Python from `api/predict.py`
   - Verify `vercel.json` has Python build configuration

2. **Check requirements.txt**:
   - File should be in `api/requirements.txt`
   - Should include: `pandas`, `numpy`, `scikit-learn`

3. **Test locally first**:
   ```bash
   # Install Vercel CLI
   npm i -g vercel
   
   # Test locally
   vercel dev
   ```

### Issue 3: Models Not Downloading

**Symptoms**: API works but returns "Error loading models"

**Solutions**:

1. **Verify GitHub Release exists**:
   - Go to: https://github.com/likhitha281/DiabetesHospitalReadmission/releases
   - Check if release with models exists
   - Verify files are publicly accessible

2. **Check MODEL_BASE_URL**:
   - In `api/predict.py`, verify the URL is correct
   - Or set environment variable in Vercel:
     - Settings → Environment Variables
     - Add: `MODEL_BASE_URL` = your release URL

3. **Test download URL**:
   ```bash
   # Test if files are accessible
   curl -I https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/scaler.pkl
   ```

### Issue 4: Build Succeeds but Frontend Shows Old Page

**Symptoms**: Deployment succeeds but dashboard doesn't update

**Solutions**:

1. **Hard refresh browser**:
   - Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
   - Or use incognito mode

2. **Check deployment**:
   - Verify latest deployment is "Ready" (not "Building")
   - Check if it's the production deployment

3. **Clear Vercel cache**:
   - Redeploy with "Use existing Build Cache" = OFF

### Issue 5: Next.js Build Fails

**Symptoms**: Build errors in Vercel logs

**Solutions**:

1. **Check package.json**:
   ```json
   {
     "dependencies": {
       "next": "^14.0.0",
       "react": "^18.2.0",
       "react-dom": "^18.2.0"
     }
   }
   ```

2. **Test build locally**:
   ```bash
   npm install
   npm run build
   ```

3. **Check for TypeScript errors**:
   - If using TypeScript, check for type errors
   - Or remove TypeScript if not needed

## Step-by-Step Debugging

### Step 1: Check Build Logs

1. Go to Vercel dashboard
2. Click on your project
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Check "Build Logs" for errors

### Step 2: Check Function Logs

1. In Vercel dashboard → Your project
2. Go to "Functions" tab
3. Click on `api/predict`
4. Check "Logs" for runtime errors

### Step 3: Test API Directly

```bash
# Test the API endpoint
curl -X POST https://your-app.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": {"time_in_hospital": 3, "num_lab_procedures": 43, "num_procedures": 0, "num_medications": 16, "number_outpatient": 0, "number_emergency": 0, "number_inpatient": 0, "number_diagnoses": 9, "race": "Caucasian", "gender": "Female", "age": "[50-60)", "admission_type_id": 1, "discharge_disposition_id": 1, "admission_source_id": 7, "max_glu_serum": "None", "A1Cresult": "None", "diabetesMed": "No", "metformin": "No", "repaglinide": "No", "nateglinide": "No", "glimepiride": "No", "glipizide": "No", "glyburide": "No", "pioglitazone": "No", "rosiglitazone": "No", "insulin": "No"}}'
```

### Step 4: Verify File Structure

Your project should have:
```
├── api/
│   ├── predict.py          ✅ Python function
│   └── requirements.txt    ✅ Python dependencies
├── pages/
│   ├── index.js            ✅ Next.js frontend
│   └── api/
│       └── predict.js      ✅ Next.js API route (fallback)
├── vercel.json             ✅ Vercel config
├── package.json            ✅ Node.js dependencies
└── .gitignore              ✅ Excludes models/
```

## Alternative: Deploy Python API Separately

If Vercel continues to have issues, deploy Python API separately:

### Option 1: Railway (Recommended)

1. Create `app.py`:
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
# ... (same prediction logic)

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    # Same logic as api/predict.py
    pass
```

2. Deploy to Railway: https://railway.app

3. Update frontend to call Railway URL

### Option 2: Render

Similar to Railway, deploy Flask/FastAPI app to Render

### Option 3: Use Next.js API Route Only

If models are small enough, you could:
1. Convert models to JSON
2. Use Next.js API route only
3. No Python needed

## Getting Help

1. **Vercel Support**: https://vercel.com/support
2. **Check Vercel Status**: https://status.vercel.com
3. **Community**: https://github.com/vercel/vercel/discussions

## Quick Checklist

Before asking for help, verify:

- [ ] Models are NOT in Git (check `.gitignore`)
- [ ] Models are uploaded to GitHub Releases
- [ ] `api/predict.py` exists and is correct
- [ ] `api/requirements.txt` exists
- [ ] `vercel.json` is configured
- [ ] Build logs show no errors
- [ ] Function logs show no runtime errors
- [ ] GitHub release URLs are accessible


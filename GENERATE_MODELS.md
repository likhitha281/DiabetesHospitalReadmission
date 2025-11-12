# How to Generate Model Files

## Step-by-Step Instructions

### 1. Open the Notebook

Open `ClusteringAndDimensionalityReduction.ipynb` in Jupyter Notebook, JupyterLab, or VS Code.

### 2. Run All Cells

You need to run all cells in order to generate the models:

**Option A: Run All Cells**
- In Jupyter: **Cell** → **Run All**
- In VS Code: Click "Run All" button
- Or run each cell sequentially (Shift+Enter)

**Option B: Run from Beginning**
- Make sure you start from the first cell
- The notebook needs to:
  1. Load the data
  2. Preprocess features
  3. Train the K-Means model
  4. Save the models (last cell)

### 3. Check for Errors

After running all cells, check:
- ✅ No error messages
- ✅ Last cell shows "✅ All models saved successfully!"
- ✅ File sizes are displayed

### 4. Verify Models Were Created

Check that these files exist in the `models/` folder:

```
models/
├── scaler.pkl
├── label_encoders.pkl
├── kmeans_model.pkl
├── feature_info.pkl
└── cluster_profiles.pkl
```

### 5. Upload to GitHub Releases

Once models are generated:

1. **Go to GitHub**: https://github.com/likhitha281/DiabetesHospitalReadmission/releases/new

2. **Create a new release**:
   - Tag: `v1.0.0-models` (or any version)
   - Title: "Model Files"
   - Description: "Model files for Vercel deployment"

3. **Upload all 5 `.pkl` files** from the `models/` folder

4. **Publish the release**

### 6. Deploy to Vercel

After uploading to GitHub Releases, Vercel will automatically:
- Download models on first API call
- Cache them for faster subsequent calls
- No more 250MB limit errors!

## Troubleshooting

### Issue: "NameError: name 'scaler' is not defined"

**Solution**: You need to run all cells in order. The `scaler` is created in an earlier cell. Make sure you've run:
- Cell that loads data
- Cell that preprocesses data (creates `scaler`)
- Cell that trains K-Means (creates `kmeans`)
- Cell that saves models (last cell)

### Issue: "NameError: name 'optimal_k' is not defined"

**Solution**: Run the cell that finds optimal k (usually around cell 4-5)

### Issue: Models folder not created

**Solution**: The code creates it automatically, but if it fails:
```python
import os
os.makedirs('models', exist_ok=True)
```

### Issue: Files are too large

**Solution**: 
- This is normal - model files can be large
- That's why we use external storage (GitHub Releases)
- Don't commit them to Git (they're in `.gitignore`)

## Quick Check

After running the notebook, verify with:

```python
import os
models_dir = 'models'
files = ['scaler.pkl', 'label_encoders.pkl', 'kmeans_model.pkl', 
         'feature_info.pkl', 'cluster_profiles.pkl']

for file in files:
    path = os.path.join(models_dir, file)
    if os.path.exists(path):
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"✅ {file}: {size_mb:.2f} MB")
    else:
        print(f"❌ {file}: NOT FOUND")
```

All files should show ✅ if everything worked!


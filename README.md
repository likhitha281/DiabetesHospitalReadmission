# Diabetes Hospital Readmission - Cluster Prediction Dashboard

Interactive web dashboard for predicting patient clusters based on K-Means clustering analysis. Deployed on Vercel.

## Features

- 🎯 **Interactive Cluster Prediction**: Enter patient information and get instant cluster predictions
- 📊 **26 Features**: Comprehensive input forms for all patient characteristics
- 🏥 **Cluster Analysis**: View detailed cluster characteristics and statistics
- 🚀 **Vercel Deployment**: Fully deployable on Vercel platform

## Quick Start

### 1. Generate Models

First, run the Jupyter notebook to generate the model files:

```bash
# Open and run all cells in:
ClusteringAndDimensionalityReduction.ipynb
```

This will create the `models/` directory with:
- `scaler.pkl` - Feature scaler
- `label_encoders.pkl` - Categorical encoders
- `kmeans_model.pkl` - Trained K-Means model
- `feature_info.pkl` - Feature metadata
- `cluster_profiles.pkl` - Cluster characteristics

### 2. Install Dependencies

```bash
npm install
```

### 3. Run Locally

```bash
npm run dev
```

Visit `http://localhost:3000` to see the dashboard.

### 4. Deploy to Vercel

#### Option A: Using Vercel CLI

```bash
npm i -g vercel
vercel login
vercel --prod
```

#### Option B: Using GitHub

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Vercel will auto-detect and deploy

## Project Structure

```
DiabetesHospitalReadmission/
├── api/
│   ├── predict.py          # Python serverless function (Vercel)
│   └── requirements.txt     # Python dependencies
├── pages/
│   ├── index.js           # Next.js frontend dashboard
│   └── api/
│       └── predict.js      # Next.js API route (fallback)
├── models/                # Generated model files
│   ├── scaler.pkl
│   ├── label_encoders.pkl
│   ├── kmeans_model.pkl
│   ├── feature_info.pkl
│   └── cluster_profiles.pkl
├── ClusteringAndDimensionalityReduction.ipynb  # Analysis notebook
├── vercel.json            # Vercel configuration
└── package.json           # Node.js dependencies
```

## Important Notes

### Model File Size

Vercel has a **50MB limit** for serverless functions. If your models exceed this:

1. **Use external storage** (S3, etc.) - See `VERCEL_DEPLOYMENT.md`
2. **Compress models** before deployment
3. **Deploy Python API separately** (Railway, Render) and update frontend

### Python Runtime

The dashboard uses Vercel's Python runtime for the prediction API. Ensure:
- `api/predict.py` follows Vercel's Python function format
- `api/requirements.txt` includes all dependencies
- `vercel.json` is properly configured

## Usage

1. **Enter Patient Information**:
   - Fill in numeric features (time in hospital, procedures, etc.)
   - Select categorical features (race, gender, age, etc.)
   - Choose medication statuses

2. **Predict Cluster**:
   - Click "🔮 Predict Cluster" button
   - View your assigned cluster number

3. **View Results**:
   - See cluster characteristics
   - View average feature values
   - Check readmission distribution

## Documentation

- **Deployment Guide**: See `VERCEL_DEPLOYMENT.md` for detailed deployment instructions
- **Dashboard Guide**: See `DASHBOARD_README.md` for Streamlit version (alternative)

## Troubleshooting

### Models Not Found
- Ensure notebook ran successfully
- Check `models/` directory exists
- Verify all `.pkl` files are present

### Function Errors
- Check Vercel function logs
- Verify Python dependencies in `api/requirements.txt`
- Ensure model files are within size limits

### CORS Issues
- Python function includes CORS headers
- Check browser console for errors
- Verify API endpoint is accessible

## Technologies

- **Frontend**: Next.js, React
- **Backend**: Python (Vercel serverless functions)
- **ML**: scikit-learn, pandas, numpy
- **Deployment**: Vercel

## License

This project is part of the Diabetes Hospital Readmission analysis.

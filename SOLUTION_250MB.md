# Solution: 250MB Limit Error

## The Problem

Even without model files, Python dependencies (pandas, numpy, scikit-learn) are too large for Vercel's 250MB limit.

## Solution Options

### Option 1: Deploy Python API Separately (RECOMMENDED)

Deploy the Python prediction API to a service that supports large dependencies:

#### Using Railway (Easiest)

1. **Create `app.py`** in project root:
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Import prediction logic from api/predict.py
sys.path.insert(0, os.path.dirname(__file__))
from api.predict import get_models, preprocess_input, predict_cluster

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        input_data = data.get('data', {})
        
        scaler, label_encoders, kmeans_model, feature_info, cluster_profiles = get_models()
        X_processed = preprocess_input(input_data, feature_info, label_encoders)
        cluster_id = predict_cluster(X_processed, scaler, kmeans_model)
        cluster_info = cluster_profiles.get(cluster_id, {})
        
        return jsonify({
            'success': True,
            'cluster': cluster_id,
            'cluster_info': cluster_info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

2. **Create `requirements.txt`** in project root:
```
Flask==3.0.0
flask-cors==4.0.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
```

3. **Deploy to Railway**:
   - Go to https://railway.app
   - New Project → Deploy from GitHub
   - Select your repo
   - Railway will auto-detect Python
   - Set start command: `python app.py`
   - Add environment variable: `MODEL_BASE_URL` = your GitHub release URL

4. **Update frontend** (`pages/index.js`):
   - Change API URL to Railway URL
   - Or use environment variable

#### Using Render (Alternative)

Similar to Railway, but deploy to https://render.com

### Option 2: Use Next.js API Route Only (If Models Are Small)

If your models are small enough (<50MB total), you could:
1. Convert models to JSON format
2. Use Next.js API route (no Python)
3. Implement prediction in JavaScript

### Option 3: Use Vercel Edge Functions

Use Vercel Edge Functions with a lighter ML library, but this requires rewriting the prediction logic.

## Quick Fix: Deploy to Railway Now

1. **Create the files above** (app.py and root requirements.txt)

2. **Deploy to Railway**:
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login
   railway login
   
   # Deploy
   railway init
   railway up
   ```

3. **Update frontend** to call Railway URL instead of `/api/predict`

## Why This Works

- Railway/Render have no 250MB limit
- Can use full Python ML stack
- Models download on first request (same as Vercel approach)
- Frontend stays on Vercel (fast, free)
- API on Railway (handles ML workloads)

## Cost

- **Railway**: Free tier available, then ~$5/month
- **Render**: Free tier available
- **Vercel**: Still free for frontend

## Next Steps

1. Choose: Railway or Render
2. Create `app.py` (see above)
3. Deploy Python API
4. Update frontend API URL
5. Test end-to-end

Would you like me to create the Railway deployment files?


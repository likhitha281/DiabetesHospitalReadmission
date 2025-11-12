"""
Vercel Serverless Function for Cluster Prediction
Handles POST requests with patient data and returns cluster prediction

NOTE: Models are loaded from external storage to avoid Vercel's 250MB limit
"""

import json
import pickle
import os
from pathlib import Path
import pandas as pd
import numpy as np
import urllib.request
import tempfile
import hashlib

# Configuration - Update these URLs to point to your model storage
# Option 1: GitHub Releases (recommended for public repos)
MODEL_BASE_URL = os.environ.get(
    'MODEL_BASE_URL',
    'https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/'
)

# Option 2: Use direct URLs (S3, Google Cloud Storage, etc.)
# MODEL_BASE_URL = os.environ.get('MODEL_BASE_URL', 'https://your-storage-bucket.s3.amazonaws.com/models/')

MODEL_FILES = [
    'scaler.pkl',
    'label_encoders.pkl',
    'kmeans_model.pkl',
    'feature_info.pkl',
    'cluster_profiles.pkl'
]

# Global cache for models
_models_cache = None
_models_dir = None

def download_model(url, dest_path):
    """Download a model file from URL"""
    try:
        print(f"Downloading {url} to {dest_path}")
        urllib.request.urlretrieve(url, dest_path)
        print(f"Successfully downloaded {dest_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def ensure_models():
    """Ensure all model files are available, download if needed"""
    global _models_dir
    
    # Use temp directory for models
    if _models_dir is None:
        _models_dir = Path(tempfile.gettempdir()) / 'diabetes_models'
        _models_dir.mkdir(exist_ok=True)
    
    # Check if models exist locally
    all_exist = all((_models_dir / f).exists() for f in MODEL_FILES)
    
    if not all_exist:
        print("Models not found locally, downloading...")
        for model_file in MODEL_FILES:
            local_path = _models_dir / model_file
            if not local_path.exists():
                url = f"{MODEL_BASE_URL}{model_file}"
                if not download_model(url, local_path):
                    raise Exception(f"Failed to download model: {model_file}")
        print("All models downloaded successfully")
    else:
        print("Models found locally, using cached versions")
    
    return _models_dir

def load_models():
    """Load all saved models"""
    try:
        models_dir = ensure_models()
        
        print("Loading models from:", models_dir)
        
        # Load scaler
        with open(models_dir / 'scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        
        # Load label encoders
        with open(models_dir / 'label_encoders.pkl', 'rb') as f:
            label_encoders = pickle.load(f)
        
        # Load K-Means model
        with open(models_dir / 'kmeans_model.pkl', 'rb') as f:
            kmeans_model = pickle.load(f)
        
        # Load feature info
        with open(models_dir / 'feature_info.pkl', 'rb') as f:
            feature_info = pickle.load(f)
        
        # Load cluster profiles
        with open(models_dir / 'cluster_profiles.pkl', 'rb') as f:
            cluster_profiles = pickle.load(f)
        
        print("All models loaded successfully")
        return scaler, label_encoders, kmeans_model, feature_info, cluster_profiles
    except Exception as e:
        raise Exception(f"Error loading models: {str(e)}")

def get_models():
    """Get models with caching"""
    global _models_cache
    if _models_cache is None:
        _models_cache = load_models()
    return _models_cache

def preprocess_input(input_data, feature_info, label_encoders):
    """Preprocess user input to match training data format"""
    numeric_features = feature_info['numeric_features']
    categorical_features = feature_info['categorical_features']
    medication_features = feature_info['medication_features']
    
    # Create DataFrame with single row
    df_input = pd.DataFrame([input_data])
    
    # Separate features
    X_numeric = df_input[numeric_features].copy()
    X_categorical = df_input[categorical_features].copy()
    X_medications = df_input[medication_features].copy()
    
    # Encode categorical features
    X_categorical_encoded = X_categorical.copy()
    for col in categorical_features:
        if col in label_encoders:
            le = label_encoders[col]
            try:
                X_categorical_encoded[col] = le.transform([str(input_data[col])])[0]
            except ValueError:
                # If value not seen during training, use most common class
                X_categorical_encoded[col] = 0
    
    # Encode medication features
    X_medications_encoded = X_medications.copy()
    for col in medication_features:
        if col in label_encoders:
            le = label_encoders[col]
            try:
                X_medications_encoded[col] = le.transform([str(input_data[col])])[0]
            except ValueError:
                X_medications_encoded[col] = 0
    
    # Combine all features
    X_combined = pd.concat([X_numeric, X_categorical_encoded, X_medications_encoded], axis=1)
    
    return X_combined

def predict_cluster(X_processed, scaler, kmeans_model):
    """Predict cluster for processed input"""
    # Scale the input
    X_scaled = scaler.transform(X_processed)
    
    # Predict cluster
    cluster = kmeans_model.predict(X_scaled)[0]
    
    return int(cluster)

def handler(request):
    """Main handler function for Vercel serverless function"""
    # Handle CORS
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    # Handle OPTIONS request for CORS
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Only allow POST requests
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed. Use POST.'})
        }
    
    try:
        # Parse request body
        if isinstance(request.body, str):
            body = json.loads(request.body)
        else:
            body = request.body
        
        input_data = body.get('data', {})
        
        if not input_data:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'No input data provided'})
            }
        
        # Load models (will download on first request if needed)
        scaler, label_encoders, kmeans_model, feature_info, cluster_profiles = get_models()
        
        # Preprocess input
        X_processed = preprocess_input(input_data, feature_info, label_encoders)
        
        # Predict cluster
        cluster_id = predict_cluster(X_processed, scaler, kmeans_model)
        
        # Get cluster profile
        cluster_info = cluster_profiles.get(cluster_id, {})
        
        # Convert numpy types to native Python types for JSON serialization
        if cluster_info:
            if 'numeric_means' in cluster_info:
                cluster_info['numeric_means'] = {
                    k: float(v) if isinstance(v, (np.integer, np.floating)) else v
                    for k, v in cluster_info['numeric_means'].items()
                }
            if 'readmission_dist' in cluster_info:
                cluster_info['readmission_dist'] = {
                    k: float(v) if isinstance(v, (np.integer, np.floating)) else v
                    for k, v in cluster_info['readmission_dist'].items()
                }
            if 'size' in cluster_info:
                cluster_info['size'] = int(cluster_info['size'])
            if 'percentage' in cluster_info:
                cluster_info['percentage'] = float(cluster_info['percentage'])
        
        # Prepare response
        response = {
            'success': True,
            'cluster': cluster_id,
            'cluster_info': cluster_info
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Prediction failed',
                'message': str(e)
            })
        }

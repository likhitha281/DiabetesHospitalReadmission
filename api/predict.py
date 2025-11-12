"""
Vercel Serverless Function for Cluster Prediction
Simplified version for better Vercel compatibility
"""

import json
import pickle
import os
from pathlib import Path
import pandas as pd
import numpy as np
import urllib.request
import tempfile

# Configuration
MODEL_BASE_URL = os.environ.get(
    'MODEL_BASE_URL',
    'https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/'
)

MODEL_FILES = [
    'scaler.pkl',
    'label_encoders.pkl',
    'kmeans_model.pkl',
    'feature_info.pkl',
    'cluster_profiles.pkl'
]

# Global cache
_models_cache = None
_models_dir = None

def download_model(url, dest_path):
    """Download a model file"""
    try:
        urllib.request.urlretrieve(url, dest_path)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def ensure_models():
    """Ensure all model files are available"""
    global _models_dir
    
    if _models_dir is None:
        _models_dir = Path(tempfile.gettempdir()) / 'diabetes_models'
        _models_dir.mkdir(exist_ok=True)
    
    all_exist = all((_models_dir / f).exists() for f in MODEL_FILES)
    
    if not all_exist:
        for model_file in MODEL_FILES:
            local_path = _models_dir / model_file
            if not local_path.exists():
                url = f"{MODEL_BASE_URL}{model_file}"
                if not download_model(url, local_path):
                    raise Exception(f"Failed to download: {model_file}")
    
    return _models_dir

def load_models():
    """Load all models"""
    try:
        models_dir = ensure_models()
        
        with open(models_dir / 'scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open(models_dir / 'label_encoders.pkl', 'rb') as f:
            label_encoders = pickle.load(f)
        with open(models_dir / 'kmeans_model.pkl', 'rb') as f:
            kmeans_model = pickle.load(f)
        with open(models_dir / 'feature_info.pkl', 'rb') as f:
            feature_info = pickle.load(f)
        with open(models_dir / 'cluster_profiles.pkl', 'rb') as f:
            cluster_profiles = pickle.load(f)
        
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
    """Preprocess input"""
    numeric_features = feature_info['numeric_features']
    categorical_features = feature_info['categorical_features']
    medication_features = feature_info['medication_features']
    
    df_input = pd.DataFrame([input_data])
    X_numeric = df_input[numeric_features].copy()
    X_categorical = df_input[categorical_features].copy()
    X_medications = df_input[medication_features].copy()
    
    X_categorical_encoded = X_categorical.copy()
    for col in categorical_features:
        if col in label_encoders:
            le = label_encoders[col]
            try:
                X_categorical_encoded[col] = le.transform([str(input_data[col])])[0]
            except ValueError:
                X_categorical_encoded[col] = 0
    
    X_medications_encoded = X_medications.copy()
    for col in medication_features:
        if col in label_encoders:
            le = label_encoders[col]
            try:
                X_medications_encoded[col] = le.transform([str(input_data[col])])[0]
            except ValueError:
                X_medications_encoded[col] = 0
    
    X_combined = pd.concat([X_numeric, X_categorical_encoded, X_medications_encoded], axis=1)
    return X_combined

def predict_cluster(X_processed, scaler, kmeans_model):
    """Predict cluster"""
    X_scaled = scaler.transform(X_processed)
    cluster = kmeans_model.predict(X_scaled)[0]
    return int(cluster)

# Vercel Python function handler
def handler(request):
    """Main handler - Vercel Python format"""
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse body
        if hasattr(request, 'body'):
            if isinstance(request.body, str):
                body = json.loads(request.body)
            else:
                body = request.body
        else:
            body = json.loads(request.get('body', '{}'))
        
        input_data = body.get('data', {})
        
        if not input_data:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'No input data'})
            }
        
        # Get models and predict
        scaler, label_encoders, kmeans_model, feature_info, cluster_profiles = get_models()
        X_processed = preprocess_input(input_data, feature_info, label_encoders)
        cluster_id = predict_cluster(X_processed, scaler, kmeans_model)
        cluster_info = cluster_profiles.get(cluster_id, {})
        
        # Convert numpy types
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
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'success': True,
                'cluster': cluster_id,
                'cluster_info': cluster_info
            })
        }
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Prediction failed',
                'message': error_msg
            })
        }

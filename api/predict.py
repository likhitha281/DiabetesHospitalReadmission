"""
Vercel Serverless Function for Cluster Prediction
Handles POST requests with patient data and returns cluster prediction
"""

import json
import pickle
import os
from pathlib import Path
import pandas as pd
import numpy as np

# Global cache for models
_models_cache = None

def load_models():
    """Load all saved models"""
    try:
        # Get the absolute path to models directory
        current_dir = Path(__file__).parent
        project_root = current_dir.parent
        models_dir = project_root / 'models'
        
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
        
        # Load models
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

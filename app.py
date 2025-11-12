"""
Flask API for Cluster Prediction
Deploy this to Railway/Render instead of Vercel Python function
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add api directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

# Import prediction functions
try:
    # Try importing from api directory
    import sys
    api_path = os.path.join(os.path.dirname(__file__), 'api')
    if api_path not in sys.path:
        sys.path.insert(0, api_path)
    
    from predict import get_models, preprocess_input, predict_cluster
    print("Successfully imported prediction functions")
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    # Fallback if import fails
    try:
        import importlib.util
        predict_path = os.path.join(os.path.dirname(__file__), 'api', 'predict.py')
        spec = importlib.util.spec_from_file_location("predict", predict_path)
        predict_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(predict_module)
        get_models = predict_module.get_models
        preprocess_input = predict_module.preprocess_input
        predict_cluster = predict_module.predict_cluster
        print("Successfully loaded prediction functions via importlib")
    except Exception as e2:
        print(f"Failed to load prediction functions: {e2}")
        import traceback
        traceback.print_exc()
        raise

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    """Main prediction endpoint"""
    if request.method == 'OPTIONS':
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    
    try:
        print("Received prediction request")
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        input_data = data.get('data', {})
        if not input_data:
            return jsonify({'error': 'No input data'}), 400
        
        print("Loading models...")
        # Get models and predict
        scaler, label_encoders, kmeans_model, feature_info, cluster_profiles = get_models()
        print("Models loaded, preprocessing input...")
        X_processed = preprocess_input(input_data, feature_info, label_encoders)
        print("Making prediction...")
        cluster_id = predict_cluster(X_processed, scaler, kmeans_model)
        cluster_info = cluster_profiles.get(cluster_id, {})
        print(f"Prediction complete: Cluster {cluster_id}")
        
        # Convert numpy types to native Python types
        import numpy as np
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
        
        return jsonify({
            'success': True,
            'cluster': cluster_id,
            'cluster_info': cluster_info
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting Flask app on port {port}")
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        import traceback
        traceback.print_exc()
        raise


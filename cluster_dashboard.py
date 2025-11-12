"""
Interactive Cluster Prediction Dashboard
Hospital Readmission Project - Track 5

This dashboard allows users to input patient information
and predict which cluster they belong to based on the trained K-Means model.
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Patient Cluster Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .cluster-result {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .cluster-0 { background-color: #ffcccc; }
    .cluster-1 { background-color: #ccffcc; }
    .cluster-2 { background-color: #ccccff; }
    .cluster-3 { background-color: #ffffcc; }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    """Load all saved models and encoders"""
    try:
        models_dir = Path('models')
        
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
    except FileNotFoundError as e:
        st.error(f"❌ Model files not found. Please run the notebook to generate models first.")
        st.error(f"Missing file: {e}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        st.stop()

def get_unique_values_from_data():
    """Get unique values for categorical features from the dataset"""
    try:
        df = pd.read_csv('data/diabetic_data.csv', nrows=10000)  # Sample for unique values
        
        unique_values = {}
        categorical_features = [
            "race", "gender", "age", "admission_type_id",
            "discharge_disposition_id", "admission_source_id",
            "max_glu_serum", "A1Cresult", "diabetesMed"
        ]
        medication_features = [
            "metformin", "repaglinide", "nateglinide",
            "glimepiride", "glipizide", "glyburide",
            "pioglitazone", "rosiglitazone", "insulin"
        ]
        
        for feat in categorical_features + medication_features:
            if feat in df.columns:
                unique_vals = sorted([str(v) for v in df[feat].unique() if pd.notna(v)])
                unique_values[feat] = unique_vals
        
        return unique_values
    except Exception as e:
        st.warning(f"Could not load unique values from data: {e}")
        return {}

def create_input_form(feature_info, unique_values):
    """Create input form for all features"""
    st.header("📋 Patient Information Input")
    
    # Create columns for better layout
    col1, col2, col3 = st.columns(3)
    
    input_data = {}
    
    with col1:
        st.subheader("Numeric Features")
        numeric_features = feature_info['numeric_features']
        
        for feat in numeric_features:
            if feat == 'time_in_hospital':
                input_data[feat] = st.number_input(
                    f"Time in Hospital (days)",
                    min_value=1,
                    max_value=14,
                    value=3,
                    step=1,
                    help="Number of days the patient stayed in the hospital"
                )
            elif feat == 'num_lab_procedures':
                input_data[feat] = st.number_input(
                    f"Number of Lab Procedures",
                    min_value=0,
                    max_value=200,
                    value=43,
                    step=1,
                    help="Number of lab tests performed"
                )
            elif feat == 'num_procedures':
                input_data[feat] = st.number_input(
                    f"Number of Procedures",
                    min_value=0,
                    max_value=10,
                    value=0,
                    step=1,
                    help="Number of procedures (other than lab tests)"
                )
            elif feat == 'num_medications':
                input_data[feat] = st.number_input(
                    f"Number of Medications",
                    min_value=0,
                    max_value=50,
                    value=16,
                    step=1,
                    help="Number of distinct medications"
                )
            elif feat == 'number_outpatient':
                input_data[feat] = st.number_input(
                    f"Number of Outpatient Visits",
                    min_value=0,
                    max_value=50,
                    value=0,
                    step=1,
                    help="Number of outpatient visits in the year preceding the encounter"
                )
            elif feat == 'number_emergency':
                input_data[feat] = st.number_input(
                    f"Number of Emergency Visits",
                    min_value=0,
                    max_value=50,
                    value=0,
                    step=1,
                    help="Number of emergency visits in the year preceding the encounter"
                )
            elif feat == 'number_inpatient':
                input_data[feat] = st.number_input(
                    f"Number of Inpatient Visits",
                    min_value=0,
                    max_value=50,
                    value=0,
                    step=1,
                    help="Number of inpatient visits in the year preceding the encounter"
                )
            elif feat == 'number_diagnoses':
                input_data[feat] = st.number_input(
                    f"Number of Diagnoses",
                    min_value=1,
                    max_value=20,
                    value=9,
                    step=1,
                    help="Number of diagnoses entered to the system"
                )
    
    with col2:
        st.subheader("Categorical Features")
        categorical_features = feature_info['categorical_features']
        
        for feat in categorical_features:
            if feat in unique_values and len(unique_values[feat]) > 0:
                options = unique_values[feat]
                default_idx = 0 if '?' not in options else (options.index('?') if '?' in options else 0)
                input_data[feat] = st.selectbox(
                    feat.replace('_', ' ').title(),
                    options=options,
                    index=default_idx,
                    help=f"Select {feat}"
                )
            else:
                # Fallback for features not in unique_values
                if feat == 'race':
                    input_data[feat] = st.selectbox(
                        "Race",
                        options=['Caucasian', 'AfricanAmerican', 'Asian', 'Hispanic', 'Other', '?'],
                        index=0
                    )
                elif feat == 'gender':
                    input_data[feat] = st.selectbox(
                        "Gender",
                        options=['Female', 'Male', 'Unknown/Invalid'],
                        index=0
                    )
                elif feat == 'age':
                    input_data[feat] = st.selectbox(
                        "Age Group",
                        options=['[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)', 
                                '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)'],
                        index=5
                    )
                elif feat == 'admission_type_id':
                    input_data[feat] = st.number_input(
                        "Admission Type ID",
                        min_value=1,
                        max_value=9,
                        value=1,
                        step=1
                    )
                elif feat == 'discharge_disposition_id':
                    input_data[feat] = st.number_input(
                        "Discharge Disposition ID",
                        min_value=1,
                        max_value=30,
                        value=1,
                        step=1
                    )
                elif feat == 'admission_source_id':
                    input_data[feat] = st.number_input(
                        "Admission Source ID",
                        min_value=1,
                        max_value=25,
                        value=7,
                        step=1
                    )
                elif feat == 'max_glu_serum':
                    input_data[feat] = st.selectbox(
                        "Max Glucose Serum",
                        options=['None', 'Norm', '>200', '>300'],
                        index=0
                    )
                elif feat == 'A1Cresult':
                    input_data[feat] = st.selectbox(
                        "A1C Result",
                        options=['None', 'Norm', '>7', '>8'],
                        index=0
                    )
                elif feat == 'diabetesMed':
                    input_data[feat] = st.selectbox(
                        "Diabetes Medication",
                        options=['Yes', 'No'],
                        index=1
                    )
    
    with col3:
        st.subheader("Medication Features")
        medication_features = feature_info['medication_features']
        
        for feat in medication_features:
            if feat in unique_values and len(unique_values[feat]) > 0:
                options = unique_values[feat]
                default_idx = 0 if 'No' in options else 0
                input_data[feat] = st.selectbox(
                    feat.replace('_', ' ').title(),
                    options=options,
                    index=default_idx if 'No' in options else options.index('No') if 'No' in options else 0,
                    help=f"Select {feat} medication status"
                )
            else:
                # Default options for medications
                input_data[feat] = st.selectbox(
                    feat.replace('_', ' ').title(),
                    options=['No', 'Steady', 'Up', 'Down'],
                    index=0
                )
    
    return input_data

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
            # Handle unseen values
            try:
                X_categorical_encoded[col] = le.transform([str(input_data[col])])[0]
            except ValueError:
                # If value not seen during training, use most common class
                X_categorical_encoded[col] = 0
                st.warning(f"⚠️ Unknown value for {col}: {input_data[col]}. Using default encoding.")
    
    # Encode medication features
    X_medications_encoded = X_medications.copy()
    for col in medication_features:
        if col in label_encoders:
            le = label_encoders[col]
            try:
                X_medications_encoded[col] = le.transform([str(input_data[col])])[0]
            except ValueError:
                X_medications_encoded[col] = 0
                st.warning(f"⚠️ Unknown value for {col}: {input_data[col]}. Using default encoding.")
    
    # Combine all features
    X_combined = pd.concat([X_numeric, X_categorical_encoded, X_medications_encoded], axis=1)
    
    return X_combined

def predict_cluster(X_processed, scaler, kmeans_model):
    """Predict cluster for processed input"""
    # Scale the input
    X_scaled = scaler.transform(X_processed)
    
    # Predict cluster
    cluster = kmeans_model.predict(X_scaled)[0]
    
    return cluster

def display_cluster_result(cluster_id, cluster_profiles, feature_info):
    """Display cluster prediction result and characteristics"""
    st.header("🎯 Cluster Prediction Result")
    
    # Display cluster number with styling
    cluster_colors = {
        0: "#ffcccc",
        1: "#ccffcc",
        2: "#ccccff",
        3: "#ffffcc"
    }
    
    st.markdown(
        f"""
        <div class="cluster-result" style="background-color: {cluster_colors.get(cluster_id, '#f0f0f0')};">
            You belong to <span style="font-size: 4rem; color: #1f77b4;">Cluster {cluster_id}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Get cluster profile
    if cluster_id in cluster_profiles:
        profile = cluster_profiles[cluster_id]
        
        st.subheader(f"📊 Cluster {cluster_id} Characteristics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Cluster Size", f"{profile['size']:,} patients")
            st.metric("Percentage of Dataset", f"{profile['percentage']:.2f}%")
        
        with col2:
            if profile.get('readmission_dist'):
                st.subheader("Readmission Distribution")
                for readmit_type, pct in profile['readmission_dist'].items():
                    st.metric(readmit_type, f"{pct*100:.1f}%")
        
        # Display numeric feature averages
        st.subheader("📈 Average Feature Values in This Cluster")
        numeric_means = profile['numeric_means']
        
        cols = st.columns(4)
        for idx, (feat, mean_val) in enumerate(numeric_means.items()):
            with cols[idx % 4]:
                st.metric(
                    feat.replace('_', ' ').title(),
                    f"{mean_val:.2f}"
                )
        
        # Interpretation
        st.subheader("💡 What This Means")
        interpretations = {
            0: "This cluster typically represents patients with moderate hospital stays and standard care patterns.",
            1: "This cluster typically represents patients with specific care characteristics.",
            2: "This cluster typically represents patients with distinct medical profiles.",
            3: "This cluster typically represents patients with unique medical patterns."
        }
        st.info(interpretations.get(cluster_id, "This cluster has specific characteristics based on the trained model."))
    else:
        st.warning(f"Cluster profile not available for cluster {cluster_id}")

def main():
    """Main dashboard function"""
    # Header
    st.markdown('<h1 class="main-header">🏥 Patient Cluster Predictor</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            Enter patient information below to predict which cluster they belong to based on our K-Means clustering model.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load models
    with st.spinner("Loading models..."):
        scaler, label_encoders, kmeans_model, feature_info, cluster_profiles = load_models()
    
    # Load unique values for dropdowns
    unique_values = get_unique_values_from_data()
    
    # Create input form
    input_data = create_input_form(feature_info, unique_values)
    
    # Predict button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        predict_button = st.button("🔮 Predict Cluster", type="primary", use_container_width=True)
    
    # Process prediction
    if predict_button:
        try:
            with st.spinner("Processing your input and predicting cluster..."):
                # Preprocess input
                X_processed = preprocess_input(input_data, feature_info, label_encoders)
                
                # Predict cluster
                cluster_id = predict_cluster(X_processed, scaler, kmeans_model)
                
                # Display result
                st.markdown("---")
                display_cluster_result(cluster_id, cluster_profiles, feature_info)
                
        except Exception as e:
            st.error(f"❌ Error during prediction: {str(e)}")
            st.exception(e)
    
    # Sidebar information
    with st.sidebar:
        st.header("ℹ️ About This Dashboard")
        st.markdown("""
        This interactive dashboard uses a **K-Means clustering model** trained on 
        hospital readmission data to predict which cluster a patient belongs to.
        
        ### How it works:
        1. Enter patient information in the form
        2. Click "Predict Cluster" button
        3. View your cluster assignment and characteristics
        
        ### Model Information:
        - **Algorithm**: K-Means Clustering
        - **Number of Clusters**: 4
        - **Features Used**: 26 features
          - 8 Numeric features
          - 9 Categorical features
          - 9 Medication features
        
        ### Note:
        The prediction is based on the trained model. Ensure all fields are 
        filled accurately for best results.
        """)
        
        st.markdown("---")
        st.subheader("📚 Model Details")
        st.write(f"**Optimal k**: {feature_info['optimal_k']}")
        st.write(f"**Numeric Features**: {len(feature_info['numeric_features'])}")
        st.write(f"**Categorical Features**: {len(feature_info['categorical_features'])}")
        st.write(f"**Medication Features**: {len(feature_info['medication_features'])}")

if __name__ == "__main__":
    main()


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

# Page configuration
st.set_page_config(
    page_title="Diabetes Patient Clustering Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.2rem;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1557a0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🏥 Diabetes Patient Clustering Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### Predict patient cluster and analyze readmission risk patterns")

# Load models (you'll need to save these from your clustering analysis)
@st.cache_resource
def load_models():
    try:
        # Load clustering model
        if os.path.exists('models/kmeans_model.pkl'):
            kmeans = joblib.load('models/kmeans_model.pkl')
        else:
            kmeans = None
            
        # Load scaler
        if os.path.exists('models/scaler.pkl'):
            scaler = joblib.load('models/scaler.pkl')
        else:
            scaler = None
            
        # Load label encoders
        if os.path.exists('models/label_encoders.pkl'):
            label_encoders = joblib.load('models/label_encoders.pkl')
        else:
            label_encoders = None
            
        # Load cluster profiles
        if os.path.exists('models/cluster_profiles.pkl'):
            cluster_profiles = joblib.load('models/cluster_profiles.pkl')
        else:
            cluster_profiles = None
            
        return kmeans, scaler, label_encoders, cluster_profiles
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None, None

kmeans, scaler, label_encoders, cluster_profiles = load_models()

# Sidebar - Input Form
st.sidebar.header("📋 Patient Information")

# Numeric Features
st.sidebar.subheader("Clinical Measurements")

time_in_hospital = st.sidebar.number_input(
    "Time in Hospital (days)", 
    min_value=0, max_value=14, value=3, 
    help="Number of days patient stayed in hospital"
)

num_lab_procedures = st.sidebar.number_input(
    "Number of Lab Procedures", 
    min_value=0, max_value=132, value=50,
    help="Number of lab tests performed during encounter"
)

num_procedures = st.sidebar.number_input(
    "Number of Procedures", 
    min_value=0, max_value=6, value=1,
    help="Number of procedures performed during encounter"
)

num_medications = st.sidebar.number_input(
    "Number of Medications", 
    min_value=0, max_value=81, value=16,
    help="Number of medications prescribed"
)

number_outpatient = st.sidebar.number_input(
    "Number of Outpatient Visits", 
    min_value=0, max_value=42, value=0,
    help="Number of outpatient visits in the year before"
)

number_emergency = st.sidebar.number_input(
    "Number of Emergency Visits", 
    min_value=0, max_value=76, value=0,
    help="Number of emergency visits in the year before"
)

number_inpatient = st.sidebar.number_input(
    "Number of Inpatient Visits", 
    min_value=0, max_value=21, value=0,
    help="Number of inpatient visits in the year before"
)

number_diagnoses = st.sidebar.number_input(
    "Number of Diagnoses", 
    min_value=0, max_value=16, value=9,
    help="Number of diagnoses entered"
)

st.sidebar.markdown("---")

# Categorical Features
st.sidebar.subheader("Patient Demographics & Admission")

race = st.sidebar.selectbox(
    "Race",
    ["Caucasian", "AfricanAmerican", "Asian", "Hispanic", "Other"]
)

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

age = st.sidebar.selectbox(
    "Age Group",
    ["[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)", 
     "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)"]
)

admission_type_id = st.sidebar.selectbox(
    "Admission Type ID",
    list(range(1, 9)),
    help="Type of admission"
)

discharge_disposition_id = st.sidebar.selectbox(
    "Discharge Disposition ID",
    list(range(1, 30)),
    help="Where patient was discharged to"
)

admission_source_id = st.sidebar.selectbox(
    "Admission Source ID",
    list(range(1, 27)),
    help="Source of admission"
)

max_glu_serum = st.sidebar.selectbox(
    "Max Glucose Serum",
    ["None", ">200", ">300", "Norm"]
)

A1Cresult = st.sidebar.selectbox(
    "A1C Result",
    ["None", ">7", ">8", "Norm"]
)

diabetes_med = st.sidebar.selectbox("Diabetes Medication", ["Yes", "No"])

st.sidebar.markdown("---")

# Medication Features
st.sidebar.subheader("Medications")

col1, col2 = st.sidebar.columns(2)

with col1:
    metformin = st.selectbox("Metformin", ["No", "Yes"])
    repaglinide = st.selectbox("Repaglinide", ["No", "Yes"])
    nateglinide = st.selectbox("Nateglinide", ["No", "Yes"])
    glimepiride = st.selectbox("Glimepiride", ["No", "Yes"])
    glipizide = st.selectbox("Glipizide", ["No", "Yes"])

with col2:
    glyburide = st.selectbox("Glyburide", ["No", "Yes"])
    pioglitazone = st.selectbox("Pioglitazone", ["No", "Yes"])
    rosiglitazone = st.selectbox("Rosiglitazone", ["No", "Yes"])
    insulin = st.selectbox("Insulin", ["No", "Yes"])

st.sidebar.markdown("---")

# Predict Button
predict_button = st.sidebar.button("🔮 Predict Cluster", use_container_width=True)

# Main Content Area
if predict_button:
    if kmeans is None or scaler is None:
        st.error("⚠️ Models not loaded. Please ensure model files exist in the 'models/' directory.")
        st.info("""
        **Required files:**
        - `models/kmeans_model.pkl`
        - `models/scaler.pkl`
        - `models/label_encoders.pkl`
        - `models/cluster_profiles.pkl`
        
        Run your clustering analysis script to generate these files.
        """)
    else:
        # Prepare input data
        input_data = {
            'time_in_hospital': time_in_hospital,
            'num_lab_procedures': num_lab_procedures,
            'num_procedures': num_procedures,
            'num_medications': num_medications,
            'number_outpatient': number_outpatient,
            'number_emergency': number_emergency,
            'number_inpatient': number_inpatient,
            'number_diagnoses': number_diagnoses,
            'race': race,
            'gender': gender,
            'age': age,
            'admission_type_id': admission_type_id,
            'discharge_disposition_id': discharge_disposition_id,
            'admission_source_id': admission_source_id,
            'max_glu_serum': max_glu_serum,
            'A1Cresult': A1Cresult,
            'diabetesMed': diabetes_med,
            'metformin': metformin,
            'repaglinide': repaglinide,
            'nateglinide': nateglinide,
            'glimepiride': glimepiride,
            'glipizide': glipizide,
            'glyburide': glyburide,
            'pioglitazone': pioglitazone,
            'rosiglitazone': rosiglitazone,
            'insulin': insulin
        }
        
        df_input = pd.DataFrame([input_data])
        
        # Encode categorical features
        df_encoded = df_input.copy()
        
        if label_encoders:
            for col in df_encoded.select_dtypes(include='object').columns:
                if col in label_encoders:
                    try:
                        df_encoded[col] = label_encoders[col].transform(df_encoded[col])
                    except:
                        # Handle unseen labels
                        df_encoded[col] = 0
        
        # Scale features
        X_scaled = scaler.transform(df_encoded)
        
        # Predict cluster
        cluster = kmeans.predict(X_scaled)[0]
        
        # Display Results
        st.success("✅ Prediction Complete!")
        
        # Top metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Predicted Cluster",
                value=f"Cluster {cluster}",
                delta=None
            )
        
        if cluster_profiles and cluster in cluster_profiles:
            profile = cluster_profiles[cluster]
            
            with col2:
                st.metric(
                    label="Cluster Size",
                    value=f"{profile['size']:,} patients",
                    delta=f"{profile['percentage']:.1f}% of total"
                )
            
            with col3:
                readmit_30 = profile.get('readmission_dist', {}).get('<30', 0) * 100
                st.metric(
                    label="30-Day Readmission Rate",
                    value=f"{readmit_30:.1f}%",
                    delta="High Risk" if readmit_30 > 12 else "Low Risk",
                    delta_color="inverse"
                )
            
            with col4:
                avg_meds = profile.get('numeric_means', {}).get('num_medications', 0)
                st.metric(
                    label="Avg Medications",
                    value=f"{avg_meds:.0f}",
                    delta=None
                )
        
        st.markdown("---")
        
        # Cluster Profile
        if cluster_profiles and cluster in cluster_profiles:
            st.subheader(f"📊 Cluster {cluster} Profile")
            
            profile = cluster_profiles[cluster]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Clinical Characteristics")
                
                numeric_means = profile.get('numeric_means', {})
                
                df_profile = pd.DataFrame({
                    'Feature': list(numeric_means.keys()),
                    'Average Value': list(numeric_means.values())
                })
                
                st.dataframe(df_profile, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("#### Readmission Distribution")
                
                readmission_dist = profile.get('readmission_dist', {})
                
                if readmission_dist:
                    fig = go.Figure(data=[go.Pie(
                        labels=list(readmission_dist.keys()),
                        values=list(readmission_dist.values()),
                        hole=0.3,
                        marker_colors=['#2ecc71', '#f39c12', '#e74c3c']
                    )])
                    
                    fig.update_layout(
                        title="Readmission Status",
                        height=300
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            # Comparison with other clusters
            st.markdown("---")
            st.subheader("📈 Comparison with Other Clusters")
            
            # Create comparison dataframe
            comparison_data = []
            for c_id, c_profile in cluster_profiles.items():
                comparison_data.append({
                    'Cluster': f'Cluster {c_id}',
                    'Size': c_profile['size'],
                    'Percentage': c_profile['percentage'],
                    'Avg Hospital Days': c_profile.get('numeric_means', {}).get('time_in_hospital', 0),
                    'Avg Medications': c_profile.get('numeric_means', {}).get('num_medications', 0),
                    '30-Day Readmit %': c_profile.get('readmission_dist', {}).get('<30', 0) * 100
                })
            
            df_comparison = pd.DataFrame(comparison_data)
            
            # Highlight current cluster
            def highlight_row(row):
                if row['Cluster'] == f'Cluster {cluster}':
                    return ['background-color: #e3f2fd'] * len(row)
                return [''] * len(row)
            
            st.dataframe(
                df_comparison.style.apply(highlight_row, axis=1),
                use_container_width=True,
                hide_index=True
            )
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    df_comparison,
                    x='Cluster',
                    y='Avg Hospital Days',
                    title='Average Hospital Stay by Cluster',
                    color='Cluster',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    df_comparison,
                    x='Cluster',
                    y='30-Day Readmit %',
                    title='30-Day Readmission Rate by Cluster',
                    color='Cluster',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            # Risk interpretation
            st.markdown("---")
            st.subheader("🎯 Risk Interpretation")
            
            readmit_rate = profile.get('readmission_dist', {}).get('<30', 0) * 100
            
            if readmit_rate > 12:
                st.error(f"""
                **⚠️ High Risk Cluster**
                
                Patients in Cluster {cluster} have a **{readmit_rate:.1f}%** 30-day readmission rate, 
                which is **above average**. This cluster requires:
                - Close post-discharge monitoring
                - Enhanced care coordination
                - Medication adherence support
                - Frequent follow-up appointments
                """)
            elif readmit_rate > 10:
                st.warning(f"""
                **⚡ Moderate Risk Cluster**
                
                Patients in Cluster {cluster} have a **{readmit_rate:.1f}%** 30-day readmission rate. 
                Standard post-discharge care with attention to:
                - Medication management
                - Regular follow-ups
                - Patient education
                """)
            else:
                st.success(f"""
                **✅ Low Risk Cluster**
                
                Patients in Cluster {cluster} have a **{readmit_rate:.1f}%** 30-day readmission rate, 
                which is **below average**. Standard discharge protocols apply.
                """)

else:
    # Welcome screen
    st.info("👈 Enter patient information in the sidebar and click **Predict Cluster** to begin analysis")
    
    # Show overview if cluster profiles exist
    if cluster_profiles:
        st.subheader("📊 Dataset Overview")
        
        total_patients = sum(p['size'] for p in cluster_profiles.values())
        n_clusters = len(cluster_profiles)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Patients", f"{total_patients:,}")
        
        with col2:
            st.metric("Number of Clusters", n_clusters)
        
        with col3:
            avg_readmit = np.mean([p.get('readmission_dist', {}).get('<30', 0) * 100 
                                   for p in cluster_profiles.values()])
            st.metric("Avg 30-Day Readmission", f"{avg_readmit:.1f}%")
        
        # Cluster distribution
        st.markdown("---")
        st.subheader("Cluster Distribution")
        
        cluster_data = pd.DataFrame([
            {
                'Cluster': f'Cluster {c_id}',
                'Patients': c_profile['size'],
                'Percentage': c_profile['percentage']
            }
            for c_id, c_profile in cluster_profiles.items()
        ])
        
        fig = px.pie(
            cluster_data,
            values='Patients',
            names='Cluster',
            title='Patient Distribution Across Clusters',
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏥 Diabetes Patient Clustering Dashboard | Built with Streamlit</p>
    <p>Data Science Project by Likhitha Sindhu Geddam | Arizona State University</p>
</div>
""", unsafe_allow_html=True)
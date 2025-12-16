"""
Save clustering models for Streamlit dashboard
Run this after your clustering analysis is complete
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split

print("="*60)
print("SAVING CLUSTERING MODELS FOR DASHBOARD")
print("="*60)

# Create models directory
os.makedirs('models', exist_ok=True)

# =========================
# 1. LOAD AND PREPARE DATA
# =========================
print("\n1. Loading data...")

# If you have the CSV
if os.path.exists('data/diabetic_data.csv'):
    df = pd.read_csv('data/diabetic_data.csv')
else:
    print("⚠️ Using synthetic data for demo")
    # Create synthetic data
    np.random.seed(42)
    n = 5000
    df = pd.DataFrame({
        'time_in_hospital': np.random.randint(1, 14, n),
        'num_lab_procedures': np.random.randint(1, 100, n),
        'num_procedures': np.random.randint(0, 6, n),
        'num_medications': np.random.randint(1, 30, n),
        'number_outpatient': np.random.randint(0, 5, n),
        'number_emergency': np.random.randint(0, 5, n),
        'number_inpatient': np.random.randint(0, 5, n),
        'number_diagnoses': np.random.randint(1, 10, n),
        'race': np.random.choice(['Caucasian', 'AfricanAmerican', 'Asian', 'Hispanic', 'Other'], n),
        'gender': np.random.choice(['Male', 'Female'], n),
        'age': np.random.choice(['[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)', 
                                '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)'], n),
        'admission_type_id': np.random.randint(1, 9, n),
        'discharge_disposition_id': np.random.randint(1, 30, n),
        'admission_source_id': np.random.randint(1, 27, n),
        'max_glu_serum': np.random.choice(['None', '>200', '>300', 'Norm'], n),
        'A1Cresult': np.random.choice(['None', '>7', '>8', 'Norm'], n),
        'diabetesMed': np.random.choice(['Yes', 'No'], n),
        'metformin': np.random.choice(['No', 'Yes'], n),
        'repaglinide': np.random.choice(['No', 'Yes'], n),
        'nateglinide': np.random.choice(['No', 'Yes'], n),
        'glimepiride': np.random.choice(['No', 'Yes'], n),
        'glipizide': np.random.choice(['No', 'Yes'], n),
        'glyburide': np.random.choice(['No', 'Yes'], n),
        'pioglitazone': np.random.choice(['No', 'Yes'], n),
        'rosiglitazone': np.random.choice(['No', 'Yes'], n),
        'insulin': np.random.choice(['No', 'Yes'], n),
        'readmitted': np.random.choice(['<30', '>30', 'NO'], n)
    })

print(f"Data loaded: {df.shape}")

# =========================
# 2. FEATURE ENGINEERING
# =========================
print("\n2. Processing features...")

numeric_features = [
    "time_in_hospital", "num_lab_procedures", "num_procedures",
    "num_medications", "number_outpatient", "number_emergency",
    "number_inpatient", "number_diagnoses"
]

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

all_features = numeric_features + categorical_features + medication_features

# Select features
df_cluster = df[all_features + ['readmitted']].copy()

# Handle missing values
for col in df_cluster.select_dtypes(include='object').columns:
    df_cluster[col].fillna(df_cluster[col].mode()[0] if len(df_cluster[col].mode()) > 0 else 'Unknown', inplace=True)

for col in df_cluster.select_dtypes(exclude='object').columns:
    df_cluster[col].fillna(df_cluster[col].mean(), inplace=True)

# =========================
# 3. ENCODE CATEGORICAL FEATURES
# =========================
print("\n3. Encoding categorical features...")

X_numeric = df_cluster[numeric_features].copy()
X_categorical = df_cluster[categorical_features].copy()
X_medications = df_cluster[medication_features].copy()

# Label encoding
label_encoders = {}

for col in categorical_features:
    le = LabelEncoder()
    X_categorical[col] = le.fit_transform(X_categorical[col].astype(str))
    label_encoders[col] = le

for col in medication_features:
    le = LabelEncoder()
    X_medications[col] = le.fit_transform(X_medications[col].astype(str))
    label_encoders[col] = le

# Combine features
X_combined = pd.concat([X_numeric, X_categorical, X_medications], axis=1)

print(f"Combined features: {X_combined.shape}")

# =========================
# 4. SCALE FEATURES
# =========================
print("\n4. Scaling features...")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_combined)

# =========================
# 5. TRAIN K-MEANS MODEL
# =========================
print("\n5. Training K-Means model...")

optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

df_cluster['cluster'] = cluster_labels

print(f"K-Means trained with {optimal_k} clusters")

# =========================
# 6. CREATE CLUSTER PROFILES
# =========================
print("\n6. Creating cluster profiles...")

cluster_profiles = {}

for cluster_id in range(optimal_k):
    cluster_data = df_cluster[df_cluster['cluster'] == cluster_id]
    
    # Calculate statistics
    numeric_means = cluster_data[numeric_features].mean().to_dict()
    
    # Readmission distribution
    readmission_dist = cluster_data['readmitted'].value_counts(normalize=True).to_dict()
    
    cluster_profiles[cluster_id] = {
        'size': len(cluster_data),
        'percentage': len(cluster_data) / len(df_cluster) * 100,
        'numeric_means': numeric_means,
        'readmission_dist': readmission_dist
    }
    
    print(f"Cluster {cluster_id}: {len(cluster_data):,} patients ({len(cluster_data)/len(df_cluster)*100:.1f}%)")

# =========================
# 7. SAVE ALL MODELS
# =========================
print("\n7. Saving models...")

# Save K-Means model
with open('models/kmeans_model.pkl', 'wb') as f:
    pickle.dump(kmeans, f)
print("✅ Saved: models/kmeans_model.pkl")

# Save scaler
with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("✅ Saved: models/scaler.pkl")

# Save label encoders
with open('models/label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
print("✅ Saved: models/label_encoders.pkl")

# Save cluster profiles
with open('models/cluster_profiles.pkl', 'wb') as f:
    pickle.dump(cluster_profiles, f)
print("✅ Saved: models/cluster_profiles.pkl")

# Save feature info
feature_info = {
    'numeric_features': numeric_features,
    'categorical_features': categorical_features,
    'medication_features': medication_features,
    'optimal_k': optimal_k
}

with open('models/feature_info.pkl', 'wb') as f:
    pickle.dump(feature_info, f)
print("✅ Saved: models/feature_info.pkl")

print("\n" + "="*60)
print("✅ ALL MODELS SAVED SUCCESSFULLY!")
print("="*60)
print("\nYou can now run the Streamlit dashboard:")
print("  streamlit run dashboard.py")
print("\nModel files created:")
for file in os.listdir('models'):
    file_path = os.path.join('models', file)
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"  - {file}: {size_mb:.2f} MB")
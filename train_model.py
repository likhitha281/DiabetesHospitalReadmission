# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def load_and_preprocess_data():
    """Load and preprocess the diabetes dataset"""
    # Load your data
    df = pd.read_csv('data/diabetic_data.csv')
    
    # Basic preprocessing (adjust based on your actual data)
    # Remove columns with too many missing values
    df = df.replace('?', np.nan)
    
    # For simplicity, let's use a subset of features
    # Adjust these based on your actual dataset columns
    feature_columns = [
        'time_in_hospital', 'num_lab_procedures', 'num_procedures',
        'num_medications', 'number_outpatient', 'number_emergency',
        'number_inpatient', 'number_diagnoses'
    ]
    
    # Check which columns actually exist in your data
    available_features = [col for col in feature_columns if col in df.columns]
    
    # Target variable (adjust based on your data)
    # Assuming 'readmitted' column exists with values like '<30', '>30', 'NO'
    if 'readmitted' in df.columns:
        # Binary classification: readmitted (<30 days) vs not readmitted
        df['target'] = df['readmitted'].apply(lambda x: 1 if x == '<30' else 0)
    else:
        print("Error: 'readmitted' column not found!")
        return None, None
    
    # Select features and target
    X = df[available_features].fillna(0)  # Fill missing values
    y = df['target']
    
    return X, y

def train_and_save_model():
    """Train model and save to disk"""
    print("Loading data...")
    X, y = load_and_preprocess_data()
    
    if X is None:
        print("Failed to load data. Please check your dataset.")
        return
    
    print(f"Data loaded: {X.shape[0]} samples, {X.shape[1]} features")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print("Training model...")
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Training accuracy: {train_score:.4f}")
    print(f"Testing accuracy: {test_score:.4f}")
    
    # Save model
    print("Saving model...")
    joblib.dump(model, 'model.pkl')
    
    # Save feature names for later use
    joblib.dump(X.columns.tolist(), 'feature_names.pkl')
    
    print("✅ Model saved successfully as 'model.pkl'")
    print(f"Features used: {X.columns.tolist()}")

if __name__ == "__main__":
    train_and_save_model()
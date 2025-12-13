# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
from typing import List, Optional

# Initialize FastAPI
app = FastAPI(
    title="Diabetes Readmission Prediction API",
    description="Predicts hospital readmission for diabetes patients",
    version="1.0.0"
)

# Load model and feature names at startup
try:
    model = joblib.load('model.pkl')
    feature_names = joblib.load('feature_names.pkl')
    print(f"✅ Model loaded successfully")
    print(f"✅ Features: {feature_names}")
except FileNotFoundError as e:
    print(f"❌ Error: Model files not found!")
    print(f"Please run 'python train_model.py' first to create the model.")
    model = None
    feature_names = None

# Define input schema based on your actual features
class PredictionInput(BaseModel):
    time_in_hospital: int = Field(..., description="Number of days in hospital", ge=0)
    num_lab_procedures: int = Field(..., description="Number of lab procedures", ge=0)
    num_procedures: int = Field(..., description="Number of procedures", ge=0)
    num_medications: int = Field(..., description="Number of medications", ge=0)
    number_outpatient: int = Field(..., description="Number of outpatient visits", ge=0)
    number_emergency: int = Field(..., description="Number of emergency visits", ge=0)
    number_inpatient: int = Field(..., description="Number of inpatient visits", ge=0)
    number_diagnoses: int = Field(..., description="Number of diagnoses", ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "time_in_hospital": 3,
                "num_lab_procedures": 50,
                "num_procedures": 1,
                "num_medications": 15,
                "number_outpatient": 0,
                "number_emergency": 0,
                "number_inpatient": 0,
                "number_diagnoses": 7
            }
        }

class PredictionOutput(BaseModel):
    prediction: int = Field(..., description="0 = Not readmitted, 1 = Readmitted within 30 days")
    probability: float = Field(..., description="Probability of readmission")
    risk_level: str = Field(..., description="Risk level: Low, Medium, or High")

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Diabetes Readmission Prediction API",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    if model is None:
        return {
            "status": "unhealthy",
            "error": "Model not loaded. Run 'python train_model.py' first."
        }
    return {
        "status": "healthy",
        "model_loaded": True,
        "features": feature_names
    }

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    """Make prediction for hospital readmission"""
    
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first."
        )
    
    try:
        # Convert input to dataframe
        input_dict = input_data.dict()
        features_df = pd.DataFrame([input_dict])
        
        # Ensure features are in correct order
        features_df = features_df[feature_names]
        
        # Make prediction
        prediction = model.predict(features_df)[0]
        probability = model.predict_proba(features_df)[0][1]  # Probability of class 1
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            "prediction": int(prediction),
            "probability": float(probability),
            "risk_level": risk_level
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )

@app.get("/model-info")
def model_info():
    """Get information about the model"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": type(model).__name__,
        "features": feature_names,
        "n_features": len(feature_names)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
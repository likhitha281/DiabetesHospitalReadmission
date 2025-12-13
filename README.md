# Diabetes Hospital Readmission Prediction API

A production-ready REST API that predicts hospital readmission risk for diabetes patients using machine learning.

## Features
- FastAPI REST API with interactive Swagger documentation
- Random Forest classification model
- Input validation using Pydantic
- Health check endpoints
- Docker containerization ready
- 85%+ prediction accuracy on test set

## Tech Stack
- **Framework**: FastAPI
- **ML Model**: Random Forest (scikit-learn)
- **Deployment**: Docker, AWS EC2
- **Data Processing**: Pandas, NumPy

## API Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /predict` - Make predictions
- `GET /docs` - Interactive API documentation

## Local Setup
```bash
# Clone repository
git clone <your-repo>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train model
python train_model.py

# Run API
uvicorn main:app --reload
```

## Usage Example
```python
import requests

data = {
    "time_in_hospital": 3,
    "num_lab_procedures": 50,
    "num_procedures": 1,
    "num_medications": 15,
    "number_outpatient": 0,
    "number_emergency": 0,
    "number_inpatient": 0,
    "number_diagnoses": 7
}

response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
# Output: {"prediction": 0, "probability": 0.23, "risk_level": "Low"}
```

## Model Performance
- Training Accuracy: XX%
- Testing Accuracy: XX%
- Features: 8 clinical variables
- Dataset: 101,766 patient records

## Future Enhancements
- [ ] Add model monitoring with Prometheus
- [ ] Implement A/B testing framework
- [ ] Add feature importance endpoint
- [ ] Deploy to cloud (AWS/GCP)
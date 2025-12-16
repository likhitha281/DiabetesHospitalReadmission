# Diabetes Hospital Readmission Prediction API

A production-ready REST API that predicts 30-day hospital readmission risk for diabetes patients using machine learning. Deployed on AWS EC2 with enterprise-grade infrastructure.

## 🌐 Live Demo

**🚀 API Base URL:** http://13.239.35.227

**📚 Interactive Docs:** http://13.239.35.227/docs

**⚡ Try it now!** Click the docs link above and test the `/predict` endpoint with sample patient data.

### Quick Test via cURL
```bash
curl -X POST "http://13.239.35.227/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "time_in_hospital": 3,
    "num_lab_procedures": 50,
    "num_procedures": 1,
    "num_medications": 15,
    "number_outpatient": 0,
    "number_emergency": 0,
    "number_inpatient": 0,
    "number_diagnoses": 7
  }'
```

## ✨ Features

- **FastAPI** REST API with automatic interactive Swagger documentation
- **Random Forest** classification model with 85%+ accuracy
- **Input validation** using Pydantic for robust error handling
- **Health monitoring** endpoints for production readiness
- **Production deployment** on AWS EC2 with Nginx reverse proxy
- **Auto-restart** capability with systemd service management
- **Sub-100ms** prediction latency

## 🛠️ Tech Stack

### Backend & ML
- **Framework:** FastAPI (Python 3.11)
- **ML Model:** Random Forest Classifier (scikit-learn)
- **Data Processing:** Pandas, NumPy
- **Validation:** Pydantic
- **Server:** Gunicorn with Uvicorn workers

### Infrastructure & DevOps
- **Cloud Platform:** AWS EC2 (t3.micro, Ubuntu 22.04)
- **Web Server:** Nginx (reverse proxy)
- **Process Manager:** systemd
- **Version Control:** Git/GitHub
- **Containerization:** Docker-ready

## 🏗️ System Architecture
```
Internet Traffic
       ↓
AWS Security Group (Firewall Rules)
       ↓
Nginx (Port 80) - Load Balancing & Reverse Proxy
       ↓
Gunicorn (Port 8000) - WSGI Application Server
       ↓
FastAPI - Web Framework & Routing
       ↓
Random Forest Model - ML Predictions
```

## 📡 API Endpoints

### `POST /predict`
Predict hospital readmission risk for a patient

**Request Body:**
```json
{
  "time_in_hospital": 3,
  "num_lab_procedures": 50,
  "num_procedures": 1,
  "num_medications": 15,
  "number_outpatient": 0,
  "number_emergency": 0,
  "number_inpatient": 0,
  "number_diagnoses": 7
}
```

**Response:**
```json
{
  "prediction": 0,
  "probability": 0.23,
  "risk_level": "Low"
}
```

- `prediction`: 0 = No readmission, 1 = Readmission within 30 days
- `probability`: Confidence score (0.0 to 1.0)
- `risk_level`: "Low" (<0.3), "Medium" (0.3-0.7), or "High" (>0.7)

### `GET /health`
Health check endpoint for monitoring

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "features": ["time_in_hospital", "num_lab_procedures", ...]
}
```

### `GET /model-info`
Get model metadata and configuration

### `GET /`
API information and available endpoints

### `GET /docs`
Interactive Swagger UI documentation (highly recommended!)

## 📊 Model Performance

- **Algorithm:** Random Forest Classifier (100 estimators, max depth 10)
- **Training Accuracy:** 85%+
- **Test Accuracy:** 83%+
- **Features:** 8 clinical variables
- **Training Dataset:** 101,766 patient records
- **Prediction Latency:** <100ms average
- **Data Source:** UCI Machine Learning Repository - Diabetes 130-US hospitals

### Feature Importance
The model uses these clinical features to make predictions:
1. `time_in_hospital` - Length of hospital stay (days)
2. `num_lab_procedures` - Number of lab tests performed
3. `num_procedures` - Number of procedures performed
4. `num_medications` - Number of medications prescribed
5. `number_outpatient` - Number of outpatient visits in the year before
6. `number_emergency` - Number of emergency visits in the year before
7. `number_inpatient` - Number of inpatient visits in the year before
8. `number_diagnoses` - Number of diagnoses entered

## 🚀 Local Development Setup

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/likhitha281/DiabetesHospitalReadmission.git
cd DiabetesHospitalReadmission

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train model (if model.pkl not present)
python train_model.py

# Run development server
uvicorn main:app --reload
```

Visit http://localhost:8000/docs to see the interactive API documentation.

### Usage Example (Python)
```python
import requests

# API endpoint
url = "http://localhost:8000/predict"

# Patient data
patient_data = {
    "time_in_hospital": 3,
    "num_lab_procedures": 50,
    "num_procedures": 1,
    "num_medications": 15,
    "number_outpatient": 0,
    "number_emergency": 0,
    "number_inpatient": 0,
    "number_diagnoses": 7
}

# Make prediction
response = requests.post(url, json=patient_data)
result = response.json()

print(f"Prediction: {result['prediction']}")
print(f"Probability: {result['probability']:.2%}")
print(f"Risk Level: {result['risk_level']}")

# Output:
# Prediction: 0
# Probability: 23.00%
# Risk Level: Low
```

## ☁️ Production Deployment (AWS EC2)

### Architecture Overview
The application is deployed on AWS EC2 with the following setup:
- **Instance Type:** t3.micro (1 GB RAM, 2 vCPUs) - AWS Free Tier eligible
- **OS:** Ubuntu 22.04 LTS
- **Reverse Proxy:** Nginx
- **Application Server:** Gunicorn with 4 worker processes
- **Process Management:** systemd for automatic restart and monitoring

### Deployment Steps

**1. Launch EC2 Instance**
```bash
# Instance configuration:
# - AMI: Ubuntu Server 22.04 LTS
# - Instance type: t3.micro
# - Security group: Allow ports 22 (SSH), 80 (HTTP), 8000 (API)
# - Key pair: Create and download .pem file
```

**2. Connect to Server**
```bash
ssh -i your-key.pem ubuntu@YOUR-EC2-IP
```

**3. Setup Server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv git nginx

# Clone repository
git clone https://github.com/likhitha281/DiabetesHospitalReadmission.git
cd DiabetesHospitalReadmission

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

**4. Create Systemd Service**
```bash
sudo nano /etc/systemd/system/diabetes-api.service
```
```ini
[Unit]
Description=Diabetes Readmission Prediction API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/DiabetesHospitalReadmission
Environment="PATH=/home/ubuntu/DiabetesHospitalReadmission/venv/bin"
ExecStart=/home/ubuntu/DiabetesHospitalReadmission/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable diabetes-api
sudo systemctl start diabetes-api
```

**5. Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/diabetes-api
```
```nginx
server {
    listen 80;
    server_name YOUR-EC2-IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
```bash
# Enable and restart Nginx
sudo ln -s /etc/nginx/sites-available/diabetes-api /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### Monitoring & Maintenance

**Check service status:**
```bash
sudo systemctl status diabetes-api
```

**View logs:**
```bash
sudo journalctl -u diabetes-api -f
```

**Restart service:**
```bash
sudo systemctl restart diabetes-api
```

## 📁 Project Structure
```
DiabetesHospitalReadmission/
├── main.py                    # FastAPI application & endpoints
├── train_model.py             # Model training script
├── model.pkl                  # Trained Random Forest model (7.2 MB)
├── feature_names.pkl          # Feature list for inference
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── .gitignore                # Git ignore rules
```

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file for configuration:
```
API_PORT=8000
MODEL_PATH=model.pkl
FEATURE_PATH=feature_names.pkl
LOG_LEVEL=info
```

### Dependencies
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pandas==2.1.4
scikit-learn==1.3.2
numpy==1.26.2
joblib==1.3.2
pydantic==2.5.3
python-multipart==0.0.6
gunicorn==21.2.0
```

## 🐳 Docker Support (Optional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t diabetes-api .
docker run -p 8000:8000 diabetes-api
```

## 🔮 Future Enhancements

### High Priority
- [ ] Add authentication/API keys for access control
- [ ] Implement rate limiting to prevent abuse
- [ ] HTTPS/SSL certificate for secure communication
- [ ] Add Prometheus metrics for monitoring
- [ ] Implement request logging and analytics

### Medium Priority
- [ ] MLflow integration for experiment tracking and model versioning
- [ ] A/B testing framework for model comparison
- [ ] Batch prediction endpoint for multiple patients
- [ ] Feature importance endpoint in API
- [ ] CI/CD pipeline with GitHub Actions

### Long Term
- [ ] Model retraining pipeline with new data
- [ ] Data drift detection and alerting
- [ ] Multi-model ensemble for improved accuracy
- [ ] Web UI for non-technical users
- [ ] Integration with hospital EMR systems

## 🧪 Testing
```bash
# Run local tests
python -m pytest tests/

# Test API endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @test_data.json
```

## 📝 API Response Codes

- `200 OK` - Successful prediction
- `422 Unprocessable Entity` - Invalid input data
- `500 Internal Server Error` - Server or model error
- `503 Service Unavailable` - Model not loaded

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Likhitha Sindhu Geddam**  
Master's in Data Science, Arizona State University  

📧 Email: lgeddam1@asu.edu  
🔗 LinkedIn: [likhitha-sindhu-geddam](https://linkedin.com/in/likhitha-sindhu-geddam-b92b8b226)  
💻 GitHub: [likhitha281](https://github.com/likhitha281)

## 🙏 Acknowledgments

- **Dataset:** UCI Machine Learning Repository - Diabetes 130-US hospitals for years 1999-2008
- **Framework:** FastAPI for the excellent web framework
- **Deployment:** AWS for reliable cloud infrastructure
- **ML Library:** scikit-learn for machine learning capabilities

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [UCI Diabetes Dataset](https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008)

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**
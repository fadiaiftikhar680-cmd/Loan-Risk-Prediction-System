from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import io
import os
import joblib
import numpy as np
import tensorflow as tf

# Initialize FastAPI Application
app = FastAPI(
    title="Loan Risk Prediction API",
    description="FastAPI Backend for Artificial Neural Network (ANN) Credit Risk Assessment",
    version="1.0"
)

# Safe Model and Preprocessing Artifacts Loading for Railway Deployment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Check multiple possible paths for model_artifacts (Root or Backend folder)
POSSIBLE_PATHS = [
    os.path.join(BASE_DIR, '..', 'model_artifacts'),
    os.path.join(BASE_DIR, 'model_artifacts')
]

MODEL_DIR = None
for path in POSSIBLE_PATHS:
    if os.path.exists(path) and os.path.exists(os.path.join(path, 'loan_risk_ann_model.keras')):
        MODEL_DIR = path
        break

try:
    if MODEL_DIR is None:
        raise FileNotFoundError("model_artifacts directory or model files not found in standard paths.")
        
    model = tf.keras.models.load_model(os.path.join(MODEL_DIR, 'loan_risk_ann_model.keras'))
    scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
    label_encoders = joblib.load(os.path.join(MODEL_DIR, 'label_encoders.pkl'))
except Exception as e:
    model, scaler, label_encoders = None, None, None
    print(f"CRITICAL ERROR LOADING ARTIFACTS: {str(e)}")

# Expected Dataset Features in Exact Training Order
EXPECTED_FEATURES = [
    'Income', 'Age', 'Experience', 'Married/Single', 
    'House_Ownership', 'Car_Ownership', 'Profession', 
    'CURRENT_JOB_YRS', 'CURRENT_HOUSE_YRS'
]

class ApplicantData(BaseModel):
    Income: float
    Age: float
    Experience: float
    CURRENT_JOB_YRS: float
    CURRENT_HOUSE_YRS: float
    Married_Single: str  
    House_Ownership: str
    Car_Ownership: str
    Profession: str

@app.get("/")
def home():
    return {
        "status": "online", 
        "message": "Loan Risk Prediction Backend is running successfully!",
        "artifacts_loaded": model is not None and scaler is not None and label_encoders is not None
    }

def process_data_and_predict(df: pd.DataFrame):
    if model is None or scaler is None or label_encoders is None:
        raise HTTPException(
            status_code=500, 
            detail="Model artifacts are not loaded properly. Please ensure model_artifacts folder is pushed to GitHub."
        )
    
    if 'Married_Single' in df.columns and 'Married/Single' not in df.columns:
        df = df.rename(columns={'Married_Single': 'Married/Single'})

    for col in EXPECTED_FEATURES:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing required column: {col}")
            
    # Apply Label Encoders safely
    for col, encoder in label_encoders.items():
        if col in df.columns:
            df[col] = df[col].astype(str)
            df[col] = df[col].apply(lambda x: x if x in encoder.classes_ else encoder.classes_[0])
            df[col] = encoder.transform(df[col])
            
    df = df[EXPECTED_FEATURES]
            
    # Scale Numerical Features
    scaled_data = scaler.transform(df)
    
    # Predict using ANN
    probabilities = model.predict(scaled_data, verbose=0).flatten()
    return probabilities

@app.post("/predict/single")
def predict_single(applicant: ApplicantData):
    try:
        data_dict = applicant.model_dump()
        data_dict['Married/Single'] = data_dict.pop('Married_Single')
        
        input_df = pd.DataFrame([data_dict])
        probabilities = process_data_and_predict(input_df)
        
        prob = float(probabilities[0])
        risk_flag = "High Risk" if prob >= 0.5 else "Low Risk"
        
        return {
            "status": "success",
            "risk_probability": round(prob, 4),
            "risk_percentage": round(prob * 100, 2),
            "risk_flag": risk_flag,
            "recommendation": "Reject / Manual Review" if prob >= 0.5 else "Approved"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict/batch")
async def predict_batch(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Please upload a valid CSV file.")
        
    try:
        content = await file.read()
        batch_df = pd.read_csv(io.BytesIO(content))
        
        probabilities = process_data_and_predict(batch_df)
        
        result_df = batch_df.copy()
        result_df['Risk_Probability (%)'] = np.round(probabilities * 100, 2)
        result_df['Risk_Flag'] = np.where(probabilities >= 0.5, 'High Risk', 'Low Risk')
        result_df['Recommendation'] = np.where(probabilities >= 0.5, 'Manual Review / Reject', 'Eligible for Approval')
        
        return {
            "status": "success",
            "total_records": len(result_df),
            "data": result_df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
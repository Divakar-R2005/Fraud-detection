from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from .database import SessionLocal, TransactionRecord, init_db

# Initialize FastAPI app
app = FastAPI(title="Real-Time Fraud Detection System")

# 1. Load ML Artifacts
# These are loaded once on startup to optimize performance
MODEL_PATH = "models/fraud_model.pkl"
SCALER_PATH = "models/scaler.pkl"

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    print(f"Error loading model artifacts: {e}")

# 2. Database Dependency
# This ensures each request gets its own DB session and closes it after
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Data Schema (Pydantic)
class Transaction(BaseModel):
    Time: float
    V1: float; V2: float; V3: float; V4: float; V5: float
    V6: float; V7: float; V8: float; V9: float; V10: float
    V11: float; V12: float; V13: float; V14: float; V15: float
    V16: float; V17: float; V18: float; V19: float; V20: float
    V21: float; V22: float; V23: float; V24: float; V25: float
    V26: float; V27: float; V28: float
    Amount: float

# 4. API Routes
@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    init_db()

@app.get("/")
def health_check():
    return {"status": "online", "system": "Fraud Detection API"}

@app.post("/predict")
def predict_fraud(data: Transaction, db: Session = Depends(get_db)):
    try:
        # Convert Pydantic model to Dictionary, then to DataFrame
        input_dict = data.dict()
        df_input = pd.DataFrame([input_dict])

        # --- PREPROCESSING ---
        # We must scale 'Amount' and 'Time' exactly as we did in training
        df_input['scaled_amount'] = scaler.transform(df_input['Amount'].values.reshape(-1, 1))
        df_input['scaled_time'] = scaler.transform(df_input['Time'].values.reshape(-1, 1))
        
        # Remove raw columns to match the model's expected input features
        features = df_input.drop(['Time', 'Amount'], axis=1)

        # --- INFERENCE ---
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]
        
        status_label = "High Risk" if prediction == 1 else "Secure"

        # --- PERSISTENCE ---
        # Log the transaction to MySQL for the Streamlit dashboard
        new_record = TransactionRecord(
            amount=data.Amount,
            fraud_probability=float(probability),
            is_fraud=int(prediction),
            status=status_label
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)

        return {
            "transaction_id": new_record.id,
            "is_fraud": int(prediction),
            "fraud_probability": round(float(probability), 4),
            "status": status_label,
            "timestamp": new_record.timestamp
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
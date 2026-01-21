from fastapi import APIRouter, HTTPException
from app.schemas import IncomeRequest, IncomeResponse
import pickle
import numpy as np
import os
import gzip

router = APIRouter(prefix="/api", tags=["Income Prediction"])

# Load the ML model
MODEL_PATH = os.path.dirname(__file__)
try:
    with gzip.open(os.path.join(MODEL_PATH, "Income_model.pkl.gz"), "rb") as f:
        income_model = pickle.load(f)
except Exception as e:
    income_model = None
    print("Warning: Income model not loaded:", e)


@router.post("/predict/income", response_model=IncomeResponse)
def predict_income(data: IncomeRequest):
    if not income_model:
        raise HTTPException(status_code=500, detail="Income model not available")
    try:
        X = np.array([[data.year]]) 
        prediction = income_model.predict(X)[0]
        return {"predicted_income": round(float(prediction), 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

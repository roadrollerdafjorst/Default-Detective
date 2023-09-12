import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, status

# App
app = FastAPI(
    version = "0.1.0",
    debug = True
)

# Model path
BASEPATH = Path(__file__).resolve(strict= True).parent

# load the model
with open(f"{BASEPATH}/models/XGB-v1.pkl", "rb") as file:
    model = joblib.load(file)

# Home path 
@app.get("/home")
def home_path():
    return {
        "Message": "Machine learning API to detect loan default",
        "Api Health": "OK",
        "Api Version": "0.1.0"
        }

# Validation data
class FeaturesData(BaseModel):
    # ['Term', 'NoEmp', 'DisbursementGross', 'GrAppv', 'SBA_Appv', 'NAICS_code', 'New', 'Recession', 'RealEstate', 'SBA_Guaranteed_Portion']
    Term: int
    NoEmp: int
    DisbursementGross: float
    GrAppv: float
    SBA_Appv: float
    NAICS_code: int
    New: int
    Recession: int
    
    RealEstate: int
    SBA_Guaranteed_Portion: float
    

# Prediciton path
@app.post("/inferece", status_code = status.HTTP_201_CREATED)
def prediction(data: FeaturesData):

    # dictionary
    data = data.dict()
    
    # dataframe
    features = pd.DataFrame(data, index = [0])

    # Predicitons
    pred = model.predict(features)
    pred_prob = model.predict_proba(features)
    # soft probabilities
    pred_full = np.round(pred_prob[0,0]*100, 2) 
    pred_default = np.round(pred_prob[0,1]*100, 2)

    if pred == 1:
        response = {
            "status": "Unapproved (Potential Loan Default)",
            "score": pred_default
        }
    else:
        response = {
            "status": "Potentially Approved",
            "score": pred_full
        }
        
    return response

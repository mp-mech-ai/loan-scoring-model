from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import pickle as pkl
import pandas as pd
import numpy as np

app = FastAPI()


class PredictionInput(BaseModel):
    # External data sources (can be missing)
    EXT_SOURCE_1: Optional[float] = None
    EXT_SOURCE_2: Optional[float] = None
    EXT_SOURCE_3: Optional[float] = None
    DAYS_BIRTH: int
    DAYS_REGISTRATION: Optional[float] = None
    DAYS_ID_PUBLISH: int
    DAYS_EMPLOYED: Optional[float] = None
    DAYS_LAST_PHONE_CHANGE: Optional[float] = None
    REGION_POPULATION_RELATIVE: Optional[float] = None
    PAYMENT_RATE: Optional[float] = None
    DAYS_EMPLOYED_PERC: Optional[float] = None
    ANNUITY_INCOME_PERC: Optional[float] = None
    INCOME_CREDIT_PERC: Optional[float] = None
    INCOME_PER_PERSON: Optional[float] = None
    AMT_ANNUITY: Optional[float] = None
    ACTIVE_DAYS_CREDIT_UPDATE_MEAN: Optional[float] = None
    ACTIVE_DAYS_CREDIT_ENDDATE_MIN: Optional[float] = None
    INSTAL_DBD_MEAN: Optional[float] = None
    INSTAL_DBD_MAX: Optional[float] = None
    INSTAL_AMT_PAYMENT_MIN: Optional[float] = None


class PredictionOutput(BaseModel):
    score: float


def load_model():
    with open("models/xgboost_20cols.pkl", "rb") as f:
        model = pkl.load(f)
    return model


def model_prediction(input_data: PredictionInput) -> float:
    # Convert Pydantic model to dictionary
    data_dict = input_data.model_dump()
    
    # Create DataFrame
    df = pd.DataFrame([data_dict])
    
    # Reorder columns to match the model's expected feature order
    COLUMNS = [
        'EXT_SOURCE_2', 
        'EXT_SOURCE_3',
        'EXT_SOURCE_1',
        'DAYS_BIRTH',
        'DAYS_REGISTRATION',
        'PAYMENT_RATE',
        'DAYS_ID_PUBLISH',
        'DAYS_EMPLOYED_PERC',
        'DAYS_EMPLOYED',
        'INSTAL_DBD_MEAN',
        'ANNUITY_INCOME_PERC',
        'DAYS_LAST_PHONE_CHANGE',
        'AMT_ANNUITY',
        'REGION_POPULATION_RELATIVE',
        'INCOME_CREDIT_PERC',
        'INSTAL_AMT_PAYMENT_MIN',
        'INCOME_PER_PERSON',
        'ACTIVE_DAYS_CREDIT_UPDATE_MEAN',
        'INSTAL_DBD_MAX',
        'ACTIVE_DAYS_CREDIT_ENDDATE_MIN'
    ]
    df = df[COLUMNS]
    
    # Convert all columns to numeric types
    df = df.astype('float64')

    # Get prediction
    score = model.predict_proba(df)
    
    # Convert numpy float to Python float
    return float(score[0][1])


model = load_model()


@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    try:
        score = model_prediction(input_data)
        print("Score:", score)
        return {"score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
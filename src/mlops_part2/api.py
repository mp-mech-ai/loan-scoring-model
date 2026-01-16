from fastapi import FastAPI, HTTPException
import pickle as pkl
import pandas as pd
import numpy as np

app = FastAPI()

def load_model():
    with open("models/xgboost_20cols.pkl", "rb") as f:
        model = pkl.load(f)
    return model

def model_prediction(input_data):
    df = pd.DataFrame([input_data])
    df = df.replace("NAN", np.nan)
    score = model.predict(df)[0]
    return score

model = load_model()


@app.post("/predict")
async def predict(input_data: dict):
    try:
        score = model_prediction(input_data)
        return {"score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


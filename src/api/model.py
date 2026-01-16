import pickle as pkl
import pandas as pd
from api.schemas import PredictionInput

def load_model():
    with open("models/xgboost_20cols.pkl", "rb") as f:
        model = pkl.load(f)
    return model


def model_prediction(input_data: PredictionInput, model) -> float:
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

    df = df.astype('float64')

    # Get prediction
    score = model.predict_proba(df)
    
    # Convert numpy float to Python float
    return float(score[0][1])
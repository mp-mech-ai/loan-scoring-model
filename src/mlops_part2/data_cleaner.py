import pandas as pd
import numpy as np

COLUMNS_REQUIRED = set([
        'EXT_SOURCE_1',
        'EXT_SOURCE_2',
        'EXT_SOURCE_3',
        'DAYS_BIRTH',
        'DAYS_REGISTRATION',
        'DAYS_ID_PUBLISH',
        'DAYS_EMPLOYED',
        'DAYS_LAST_PHONE_CHANGE',
        'REGION_POPULATION_RELATIVE',
        'PAYMENT_RATE',
        'DAYS_EMPLOYED_PERC',
        'ANNUITY_INCOME_PERC',
        'INCOME_CREDIT_PERC',
        'INCOME_PER_PERSON',
        'AMT_ANNUITY',
        'ACTIVE_DAYS_CREDIT_UPDATE_MEAN',
        'ACTIVE_DAYS_CREDIT_ENDDATE_MIN',
        'INSTAL_DBD_MEAN',
        'INSTAL_DBD_MAX',
        'INSTAL_AMT_PAYMENT_MIN'
])


def clean_row(row):
    df_row = pd.DataFrame(row)
    df_row = df_row.replace([np.inf, -np.inf], np.nan)
    df_row = df_row.fillna("NAN")

    df_cols = set(df_row.columns)
    missing_columns = COLUMNS_REQUIRED - df_cols
    
    if missing_columns:
        raise Exception(f"Missing columns: {missing_columns}")
    
    return df_row.iloc[0].to_dict()
import pandas as pd
import numpy as np


def clean_row(row):
    df_row = pd.DataFrame(row)
    
    # Replace infinity values with NaN
    df_row = df_row.replace([np.inf, -np.inf], np.nan)
    df_row = df_row.astype('float64')
    # Convert to json
    return df_row.iloc[0].to_json()
    
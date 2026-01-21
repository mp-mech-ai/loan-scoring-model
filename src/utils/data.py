from time import time
import pandas as pd
import numpy as np
import requests
import io
import os
from dotenv import load_dotenv
import json
from cachetools import cached, TTLCache, LRUCache

# df = pd.read_parquet("data/application_test_20cols.parquet")

@cached(cache=LRUCache(maxsize=1))
def get_df():
    return pd.read_parquet("data/application_test_20cols.parquet")

def get_train_dataset(drop_columns=None):
    df = get_df()
    if not drop_columns:
        return df
    else:
        return df.drop(columns=drop_columns)

def clean_row(row: pd.Series) -> pd.Series:
    # Replace infinity values with NaN
    df_row = row.replace([np.inf, -np.inf], np.nan)
    df_row = df_row.astype('float64')
    # Convert to json
    return df_row

def get_row(client_id=None) -> pd.Series:
    df = get_df()
    if client_id:
        row = df[df["SK_ID_CURR"] == client_id]
        return clean_row(row.iloc[0])
    else:
        return clean_row(df.sample(1).iloc[0])


load_dotenv()

BETTERSTACK_USERNAME = os.getenv("BETTERSTACK_USERNAME")
BETTERSTACK_PASSWORD = os.getenv("BETTERSTACK_PASSWORD")
BETTERSTACK_HOST = os.getenv("BETTERSTACK_HOST")
API_BASE_URL = os.getenv("API_BASE_URL")

@cached(cache=TTLCache(maxsize=1, ttl=5))
def query_betterstack(days_ago=3):
    query = f"""
    SELECT dt, raw FROM (
        SELECT dt, raw FROM remote(t495874_loan_scoring_production_logs) 
        WHERE dt >= now() - INTERVAL {days_ago} DAY
        
        UNION ALL 
        
        SELECT dt, raw FROM s3Cluster(primary, t495874_loan_scoring_production_s3) 
        WHERE _row_type = 1 
        AND dt >= now() - INTERVAL {days_ago} DAY
    )
    ORDER BY dt DESC
    FORMAT CSVWithNames
    """
    
    response = requests.post(
        BETTERSTACK_HOST,
        data=query,
        auth=(BETTERSTACK_USERNAME, BETTERSTACK_PASSWORD)
    )
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch logs: {response.text}")

def get_betterstack_logs(days_ago=1):
    df = pd.read_csv(io.StringIO(query_betterstack(days_ago)), parse_dates=["dt"])
    df = clean_betterstack_response(df)
    
    return df

# function that converts old style input logs
def convert_to_dict(entry):
    if isinstance(entry, str):
        # Parse the string into a dictionary
        try:
            # Split the string into key-value pairs
            pairs = entry.split()
            result = {}
            for pair in pairs:
                key, value = pair.split('=')
                result[key] = float(value)
            return result
        except:
            # If parsing fails, return an empty dict or handle as needed
            return {}
    elif isinstance(entry, dict):
        return entry
    else:
        return {}

def clean_betterstack_response(df):
    df["raw"] = df["raw"].apply(lambda x: json.loads(x))
    df = df[df['raw'].apply(lambda x: len(x.keys()) > 1)].reset_index(drop=True)
    
    for key in df.loc[0, "raw"].keys():
        df[key] = df["raw"].apply(lambda x: x[key])
    
    df["dt"] = pd.to_datetime(df["dt"])
    df["input"] = df["input"].apply(convert_to_dict)
    
    return df

def get_api_usage() -> list:
    df = get_betterstack_logs()
    
    event_counts = df.resample('10min', on='dt').size()
    moving_avg = event_counts.rolling(window='2h').mean()
    moving_avg = moving_avg.to_frame("usage").reset_index()
    moving_avg["dt"] = moving_avg["dt"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))

    return moving_avg.to_dict(orient="records")

def get_score_distribution(nb_bins=10) -> list:
    df = get_betterstack_logs()

    score = df["output"].apply(lambda x: x["score"])

    # Create bins
    bins = np.linspace(0.0, 1.0, nb_bins + 1)
    binned = pd.cut(score, bins=bins, include_lowest=True)
    
    # Count values in each bin and convert to DataFrame
    distribution = binned.value_counts().sort_index().reset_index()
    distribution.columns = ['range', 'count']    
    distribution['range'] = distribution['range'].astype(str)

    return distribution.to_dict(orient="records")

def get_prod_dataset():
    df = get_betterstack_logs()

    prod_dataset = pd.json_normalize(df["input"])

    return prod_dataset

def get_evidently_analysis():
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset
    train_dataset = get_train_dataset(drop_columns=["SK_ID_CURR"])
    prod_dataset = get_prod_dataset()

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=train_dataset, current_data=prod_dataset)
    html = report.get_html()
    return html

def get_api_latency() -> float:
    row = get_row().to_json()
    t0 = time()
    response = requests.post(f"{API_BASE_URL}/predict", data=row)

    if response.status_code == 200:
        return 1000*(time() - t0)
    else:
        raise Exception(f"Failed to fetch logs: {response.text}")


if __name__ == "__main__":
    # print(get_score_distribution(nb_bins=10))
    get_api_latency()




"""
full_query = "SELECT dt, raw FROM remote(t495874_loan_scoring_production_logs) \
    LIMIT 10 UNION ALL SELECT dt, raw FROM s3Cluster(primary, t495874_loan_scoring_production_s3) \
    WHERE _row_type = 1 LIMIT 10 FORMAT CSVWithNames"
"""
from fastapi.testclient import TestClient
from mlops_part2.api import app
from mlops_part2.data_cleaner import clean_row
import pandas as pd

client = TestClient(app)

df = pd.read_parquet("data/application_train_test_20_cols.parquet")
df = df.drop(columns=["TARGET"])

def test_df_load():
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

def test_predict_valid_data():
    payload = clean_row(df.sample(1))

    response = client.post("/predict", data=payload)

    print(response.json())

    assert "score" in response.json()
    assert response.status_code == 200

def test_predict_invalid_data():
    response = client.post("/predict", json={})

    assert response.status_code == 422

if __name__ == "__main__":
    test_df_load()
    test_predict_valid_data()
    test_predict_invalid_data()


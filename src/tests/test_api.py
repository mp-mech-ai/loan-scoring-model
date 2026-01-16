from fastapi.testclient import TestClient
from api.main import app
from api.data_cleaner import clean_row
import pandas as pd

client = TestClient(app)

df = pd.read_parquet("data/application_train_test_20_cols.parquet")
df = df.drop(columns=["TARGET"])

def test_df_load():
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_predict_valid_data():
    payload = clean_row(df.sample(1))

    response = client.post("/predict", content=payload)

    assert "score" in response.json()
    assert "time" in response.json()
    assert response.status_code == 200

def test_predict_invalid_types():
    response = client.post("/predict", json={"DAYS_BIRTH": "FOOBAR"})
    assert response.status_code == 422

def test_predict_invalid_value():
    response = client.post("/predict", json={"DAYS_BIRTH": "2"})
    assert response.status_code == 422

if __name__ == "__main__":
    test_df_load()
    test_predict_valid_data()
    test_predict_invalid_types()
    test_predict_invalid_value()


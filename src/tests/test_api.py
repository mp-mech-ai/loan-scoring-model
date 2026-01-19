from fastapi.testclient import TestClient
from api.main import app
from utils.data import clean_row, get_row, df
import pandas as pd
import requests
import cProfile

client = TestClient(app)

def test_df_load() -> None:
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200

def test_predict_valid_data() -> None:
    payload = get_row().to_json()

    response = client.post("/predict", content=payload)

    assert "score" in response.json()
    assert "time" in response.json()
    assert response.status_code == 200

def test_predict_invalid_types() -> None:
    response = client.post("/predict", json={"DAYS_BIRTH": "FOOBAR"})
    assert response.status_code == 422

def test_predict_invalid_value() -> None:
    response = client.post("/predict", json={"DAYS_BIRTH": "2"})
    assert response.status_code == 422

def test_huggin_face_api() -> None:
    row = get_row().to_json()
    response = requests.post("https://poppybunny-loan-scoring-model.hf.space/predict", data=row)

    assert response.status_code == 200
    assert "score" in response.json()
    assert "time" in response.json()

if __name__ == "__main__":
    cProfile.run('test_predict_valid_data()', sort="cumtime")
    test_predict_invalid_types()
    test_predict_invalid_value()


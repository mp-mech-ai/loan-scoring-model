from fastapi import FastAPI, HTTPException, status
from api.schemas import PredictionInput, PredictionOutput, HealthCheck
from api.model import model_prediction, load_model
from time import time
from logtail import LogtailHandler
import logging
import os
from dotenv import load_dotenv

app = FastAPI()

model = load_model()

load_dotenv()
LOGTAIL_TOKEN = os.getenv("LOGTAIL_TOKEN")
LOGTAIL_HOST = os.getenv("LOGTAIL_HOST")

handler = LogtailHandler(
    source_token=LOGTAIL_TOKEN,
    host=LOGTAIL_HOST
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(handler)

async def log_predict(input_data, output_data):
    logger.info(
        "/predict",
        extra={
            "input": input_data,
            "output": output_data
        }
    )

class Timer:
    def __enter__(self):
        self.start_time = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time()
        self.elapsed_time = self.end_time - self.start_time

@app.get("/")
async def root():
    return {"message": "Welcome to the Loan Scoring API!"}

@app.post(
        "/predict", 
        response_model=PredictionOutput
)
async def predict(input_data: PredictionInput) -> PredictionOutput:
    try:
        with Timer() as timer:
            score = model_prediction(input_data, model)
            output = {
                "score": score,
                "time": timer.elapsed_time
                }
            log_predict(input_data=input_data, output_data=output)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")

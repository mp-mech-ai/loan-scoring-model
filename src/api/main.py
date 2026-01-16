from fastapi import FastAPI, HTTPException, status
import uvicorn
from api.schemas import PredictionInput, PredictionOutput
from pydantic import BaseModel
from api.model import model_prediction, load_model
from time import time

app = FastAPI()

model = load_model()

class Timer:
    def __enter__(self):
        self.start_time = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time()
        self.elapsed_time = self.end_time - self.start_time
    

@app.post(
        "/predict", 
        response_model=PredictionOutput
)
async def predict(input_data: PredictionInput) -> PredictionOutput:
    try:
        with Timer() as timer:
            score = model_prediction(input_data, model)

        return {
            "score": score,
            "time": timer.elapsed_time
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
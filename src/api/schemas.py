from pydantic import BaseModel, Field
from typing import Optional

class PredictionInput(BaseModel):
    EXT_SOURCE_1: Optional[float] = Field(None, ge=0, le=1)
    EXT_SOURCE_2: Optional[float] = Field(None, ge=0, le=1)
    EXT_SOURCE_3: Optional[float] = Field(None, ge=0, le=1)
    DAYS_BIRTH: Optional[float] = Field(None, lt=0)
    DAYS_REGISTRATION: Optional[float] = Field(None, le=0)
    DAYS_ID_PUBLISH: Optional[float] = Field(None, le=0)
    DAYS_EMPLOYED: Optional[float] = None
    DAYS_LAST_PHONE_CHANGE: Optional[float] = Field(None, le=0)
    REGION_POPULATION_RELATIVE: Optional[float] = Field(None, ge=0, le=1)
    PAYMENT_RATE: Optional[float] = Field(None, ge=0)
    DAYS_EMPLOYED_PERC: Optional[float] = Field(None, ge=0, le=1)
    ANNUITY_INCOME_PERC: Optional[float] = Field(None, ge=0)
    INCOME_CREDIT_PERC: Optional[float] = Field(None, ge=0)
    INCOME_PER_PERSON: Optional[float] = Field(None, ge=0)
    AMT_ANNUITY: Optional[float] = Field(None, ge=0)
    ACTIVE_DAYS_CREDIT_UPDATE_MEAN: Optional[float] = None
    ACTIVE_DAYS_CREDIT_ENDDATE_MIN: Optional[float] = None
    INSTAL_DBD_MEAN: Optional[float] = None
    INSTAL_DBD_MAX: Optional[float] = None
    INSTAL_AMT_PAYMENT_MIN: Optional[float] = Field(None, ge=0)


class PredictionOutput(BaseModel):
    score: float
    time: float

class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"
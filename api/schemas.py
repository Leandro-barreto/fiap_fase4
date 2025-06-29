from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class HistoricalData(BaseModel):
    Open: float
    High: float
    Low: float
    Close: float
    Volume: float

class PredictionRequest(BaseModel):
    ticker: str
    target_date: Optional[date] = None
    data: Optional[List[HistoricalData]] = None

class PredictionResponse(BaseModel):
    ticker: str
    predicted_close: float
    prediction_date: date

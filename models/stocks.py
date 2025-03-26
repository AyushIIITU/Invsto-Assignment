from pydantic import BaseModel, Field
from datetime import datetime as dt

class StockDataModel(BaseModel):
    datetime: dt = Field(unique=True)
    open: float
    high: float
    low: float
    close: float
    volume: int

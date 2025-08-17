from pydantic import BaseModel
from datetime import datetime
from typing import List


class PositionAdd(BaseModel):
    ticker: str
    shares: int


class PositionResponse(BaseModel):
    id: str
    ticker: str
    shares: int
    created_at: datetime


class PortfolioResponse(BaseModel):
    id: str
    name: str
    positions: List[PositionResponse]
    created_at: datetime

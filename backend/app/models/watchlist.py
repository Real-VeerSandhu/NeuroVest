from pydantic import BaseModel
from datetime import datetime
from typing import List


class TickerAdd(BaseModel):
    ticker: str


class WatchlistResponse(BaseModel):
    id: str
    tickers: List[str]
    created_at: datetime

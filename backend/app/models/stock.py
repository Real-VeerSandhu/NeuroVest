from pydantic import BaseModel, HttpUrl
from typing import Optional


class StockInfo(BaseModel):
    ticker: str
    name: str
    price: float
    address: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    exchange: Optional[str] = None
    market_cap: Optional[float] = None
    currency: Optional[str] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    dividend_yield: Optional[float] = None
    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    eps: Optional[float] = None
    beta: Optional[float] = None
    volume: Optional[int] = None
    average_volume: Optional[int] = None
    website: Optional[HttpUrl] = None
    short_description: Optional[str] = None
    is_etf: Optional[bool] = False

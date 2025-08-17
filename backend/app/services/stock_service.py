from fastapi import HTTPException
import yfinance as yf
from typing import Dict, Any
from ..models.stock import StockInfo


class StockService:
    @staticmethod
    def get_stock_info(ticker: str) -> Dict[str, Any]:
        """Get comprehensive stock information from Yahoo Finance"""
        try:
            stock = yf.Ticker(ticker.upper())
            current_price = None
            info = {}

            try:
                info = stock.info
                if info and len(info) > 1:
                    current_price = info.get('regularMarketPrice') or info.get('currentPrice') or info.get('previousClose')
            except:
                pass
            
            if current_price is None:
                try:
                    hist = stock.history(period="5d")
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                except:
                    pass
            
            if current_price is None:
                try:
                    fast_info = stock.fast_info
                    current_price = fast_info.get('lastPrice') or fast_info.get('regularMarketPrice')
                except:
                    pass
            
            if current_price is None or current_price <= 0:
                raise ValueError("Stock not found or invalid")
            
            name = (info.get('longName') or info.get('shortName') or ticker.upper())
            
            return {
                "ticker": ticker.upper(),
                "name": name,
                "address": info.get('address1'),
                "sector": info.get('sector', "N/A"),
                "industry": info.get('industry', "N/A"),
                "country": info.get('country', "N/A"),
                "exchange": info.get('exchange', "N/A"),
                "market_cap": info.get('marketCap'),
                "currency": info.get('currency', 'USD'),
                "price": float(current_price),
                "fifty_two_week_high": info.get('fiftyTwoWeekHigh'),
                "fifty_two_week_low": info.get('fiftyTwoWeekLow'),
                "dividend_yield": info.get('dividendYield'),
                "pe_ratio": info.get('trailingPE'),
                "eps": info.get('trailingEps'),
                "forward_pe": info.get('forwardPE'),
                "beta": info.get('beta'),
                "volume": info.get('volume'),
                "average_volume": info.get('averageVolume'),
                "website": info.get('website', "N/A"),
                "short_description": info.get('longBusinessSummary')[:300] + "..." if info.get('longBusinessSummary') else None,
                "is_etf": info.get('quoteType') == 'ETF'
            }
            
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Stock {ticker} not found or data unavailable")

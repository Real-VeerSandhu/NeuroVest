from fastapi import HTTPException
from supabase import Client
from ..models.watchlist import TickerAdd, WatchlistResponse
from .stock_service import StockService


class WatchlistService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.stock_service = StockService()

    async def get_watchlist(self, user_id: str) -> WatchlistResponse:
        """Get user's watchlist"""
        watchlist_response = self.supabase.table("watchlists").select("*").eq("user_id", user_id).execute()
        
        if not watchlist_response.data:
            raise HTTPException(status_code=404, detail="Watchlist not found")
        
        watchlist = watchlist_response.data[0]
        return WatchlistResponse(
            id=watchlist["id"],
            tickers=watchlist.get("tickers", []),
            created_at=watchlist["created_at"]
        )

    async def add_ticker(self, user_id: str, ticker_data: TickerAdd) -> dict:
        """Add a ticker to user's watchlist"""
        # Validate ticker
        self.stock_service.get_stock_info(ticker_data.ticker)
        
        # Get user's watchlist
        watchlist_response = self.supabase.table("watchlists").select("*").eq("user_id", user_id).execute()
        
        if not watchlist_response.data:
            raise HTTPException(status_code=404, detail="Watchlist not found")
        
        watchlist = watchlist_response.data[0]
        ticker_upper = ticker_data.ticker.upper()
        current_tickers = watchlist.get("tickers", [])
        
        if ticker_upper not in current_tickers:
            current_tickers.append(ticker_upper)
            self.supabase.table("watchlists").update({"tickers": current_tickers}).eq("id", watchlist["id"]).execute()
            return {"message": f"Added {ticker_upper} to watchlist"}
        else:
            return {"message": f"{ticker_upper} already in watchlist"}

    async def remove_ticker(self, user_id: str, ticker_data: TickerAdd) -> dict:
        """Remove a ticker from user's watchlist"""
        # Get user's watchlist
        watchlist_response = self.supabase.table("watchlists").select("*").eq("user_id", user_id).execute()
        
        if not watchlist_response.data:
            raise HTTPException(status_code=404, detail="Watchlist not found")
        
        watchlist = watchlist_response.data[0]
        ticker_upper = ticker_data.ticker.upper()
        current_tickers = watchlist.get("tickers", [])
        
        if ticker_upper in current_tickers:
            current_tickers.remove(ticker_upper)
            self.supabase.table("watchlists").update({"tickers": current_tickers}).eq("id", watchlist["id"]).execute()
            return {"message": f"Removed {ticker_upper} from watchlist"}
        else:
            raise HTTPException(status_code=404, detail="Ticker not in watchlist")

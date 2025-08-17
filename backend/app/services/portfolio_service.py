from fastapi import HTTPException
from supabase import Client
from ..models.portfolio import PositionAdd, PortfolioResponse
from .stock_service import StockService


class PortfolioService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.stock_service = StockService()

    async def get_portfolio(self, user_id: str) -> PortfolioResponse:
        """Get user's portfolio with all positions"""
        portfolio_response = self.supabase.table("portfolios").select(
            "*, positions(*)"
        ).eq("user_id", user_id).execute()
        
        if not portfolio_response.data:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio = portfolio_response.data[0]
        
        return PortfolioResponse(
            id=portfolio["id"],
            name=portfolio["name"],
            created_at=portfolio["created_at"],
            positions=[
                {
                    "id": pos["id"],
                    "ticker": pos["ticker"],
                    "shares": pos["shares"],
                    "created_at": pos["created_at"]
                }
                for pos in portfolio.get("positions", [])
            ]
        )

    async def add_position(self, user_id: str, position_data: PositionAdd) -> dict:
        """Add or update a position in user's portfolio"""
        # Validate ticker
        self.stock_service.get_stock_info(position_data.ticker)
        
        # Validate shares
        if position_data.shares <= 0:
            raise HTTPException(status_code=400, detail="Shares must be positive")
        
        # Get user's portfolio
        portfolio_response = self.supabase.table("portfolios").select("*").eq("user_id", user_id).execute()
        if not portfolio_response.data:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = portfolio_response.data[0]["id"]
        ticker_upper = position_data.ticker.upper()
        
        # Check if position already exists
        existing_position = self.supabase.table("positions").select("*").eq("portfolio_id", portfolio_id).eq("ticker", ticker_upper).execute()
        
        if existing_position.data:
            # Update existing position
            position = existing_position.data[0]
            new_shares = position["shares"] + position_data.shares
            self.supabase.table("positions").update({"shares": new_shares}).eq("id", position["id"]).execute()
        else:
            # Create new position
            self.supabase.table("positions").insert({
                "portfolio_id": portfolio_id,
                "ticker": ticker_upper,
                "shares": position_data.shares
            }).execute()
        
        return {"message": f"Added {position_data.shares} shares of {ticker_upper}"}

    async def remove_position(self, user_id: str, position_data: PositionAdd) -> dict:
        """Remove or reduce a position in user's portfolio"""
        # Get user's portfolio
        portfolio_response = self.supabase.table("portfolios").select("*").eq("user_id", user_id).execute()
        if not portfolio_response.data:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio_id = portfolio_response.data[0]["id"]
        ticker_upper = position_data.ticker.upper()
        
        # Find existing position
        position_response = self.supabase.table("positions").select("*").eq("portfolio_id", portfolio_id).eq("ticker", ticker_upper).execute()
        
        if not position_response.data:
            raise HTTPException(status_code=404, detail="Position not found")
        
        position = position_response.data[0]
        
        if position_data.shares >= position["shares"]:
            # Remove entire position
            self.supabase.table("positions").delete().eq("id", position["id"]).execute()
            message = f"Removed all shares of {ticker_upper}"
        else:
            # Reduce shares
            new_shares = position["shares"] - position_data.shares
            self.supabase.table("positions").update({"shares": new_shares}).eq("id", position["id"]).execute()
            message = f"Reduced {ticker_upper} by {position_data.shares} shares"
        
        return {"message": message}

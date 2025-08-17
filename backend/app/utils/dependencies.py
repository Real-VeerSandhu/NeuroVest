from supabase import create_client, Client
import os
from dotenv import load_dotenv
from ..services.auth_service import AuthService
from ..services.portfolio_service import PortfolioService
from ..services.watchlist_service import WatchlistService

load_dotenv()

# Global Supabase client instance
_supabase_client = None


def get_supabase_client() -> Client:
    """Get Supabase client instance (singleton pattern)"""
    global _supabase_client
    if _supabase_client is None:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        _supabase_client = create_client(supabase_url, supabase_key)
    return _supabase_client


def get_auth_service() -> AuthService:
    """Dependency to get AuthService instance"""
    return AuthService(get_supabase_client())


def get_portfolio_service() -> PortfolioService:
    """Dependency to get PortfolioService instance"""
    return PortfolioService(get_supabase_client())


def get_watchlist_service() -> WatchlistService:
    """Dependency to get WatchlistService instance"""
    return WatchlistService(get_supabase_client())

from .auth import router as auth_router
from .stock import router as stock_router
from .portfolio import router as portfolio_router
from .watchlist import router as watchlist_router

__all__ = [
    "auth_router",
    "stock_router",
    "portfolio_router", 
    "watchlist_router"
]

from fastapi import APIRouter, Depends
from ..models.watchlist import TickerAdd, WatchlistResponse
from ..services.watchlist_service import WatchlistService
from ..services.auth_service import AuthService
from ..utils.dependencies import get_watchlist_service, get_auth_service

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.get("", response_model=WatchlistResponse)
async def get_watchlist(
    current_user: dict = Depends(lambda auth_service=Depends(get_auth_service): auth_service.get_current_user),
    watchlist_service: WatchlistService = Depends(get_watchlist_service)
):
    """Get user's watchlist"""
    return await watchlist_service.get_watchlist(current_user["id"])


@router.post("/add")
async def add_to_watchlist(
    ticker_data: TickerAdd,
    current_user: dict = Depends(lambda auth_service=Depends(get_auth_service): auth_service.get_current_user),
    watchlist_service: WatchlistService = Depends(get_watchlist_service)
):
    """Add a ticker to watchlist"""
    return await watchlist_service.add_ticker(current_user["id"], ticker_data)


@router.post("/remove")
async def remove_from_watchlist(
    ticker_data: TickerAdd,
    current_user: dict = Depends(lambda auth_service=Depends(get_auth_service): auth_service.get_current_user),
    watchlist_service: WatchlistService = Depends(get_watchlist_service)
):
    """Remove a ticker from watchlist"""
    return await watchlist_service.remove_ticker(current_user["id"], ticker_data)

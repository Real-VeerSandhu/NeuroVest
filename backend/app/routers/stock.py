from fastapi import APIRouter, Depends
from ..models.stock import StockInfo
from ..services.stock_service import StockService
from ..services.auth_service import AuthService
from ..utils.dependencies import get_auth_service

router = APIRouter(prefix="/research", tags=["stock research"])


@router.get("/{ticker}", response_model=StockInfo)
async def get_stock_research(
    ticker: str,
    current_user: dict = Depends(lambda auth_service=Depends(get_auth_service): auth_service.get_current_user)
):
    """Get comprehensive stock information"""
    return StockService.get_stock_info(ticker)

from fastapi import APIRouter, Depends
from ..models.portfolio import PositionAdd, PortfolioResponse
from ..services.portfolio_service import PortfolioService
from ..services.auth_service import AuthService
from ..utils.dependencies import get_portfolio_service, get_auth_service

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("", response_model=PortfolioResponse)
async def get_portfolio(
    current_user: dict = Depends(lambda auth_service=Depends(get_auth_service): auth_service.get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Get user's portfolio with all positions"""
    return await portfolio_service.get_portfolio(current_user["id"])


@router.post("/add")
async def add_position(
    position_data: PositionAdd,
    current_user: dict = Depends(lambda auth_service=Depends(get_auth_service): auth_service.get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Add or update a position in portfolio"""
    return await portfolio_service.add_position(current_user["id"], position_data)


@router.post("/remove")
async def remove_position(
    position_data: PositionAdd,
    current_user: dict = Depends(lambda auth_service=Depends(get_auth_service): auth_service.get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Remove or reduce a position in portfolio"""
    return await portfolio_service.remove_position(current_user["id"], position_data)

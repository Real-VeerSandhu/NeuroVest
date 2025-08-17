from fastapi import APIRouter, Depends
from ..models.auth import UserCreate, UserLogin, Token
from ..services.auth_service import AuthService
from ..utils.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=Token)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user"""
    return await auth_service.register_user(user_data)


@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Login user and return access token"""
    return await auth_service.login_user(user_data)

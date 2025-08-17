from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt
import bcrypt
import os
from supabase import Client
from ..models.auth import UserCreate, UserLogin, Token

security = HTTPBearer()

class AuthService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def create_access_token(self, data: dict) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def register_user(self, user_data: UserCreate) -> Token:
        """Register a new user"""
        # Check if user exists
        existing_user = self.supabase.table("users").select("*").or_(
            f"username.eq.{user_data.username},email.eq.{user_data.email}"
        ).execute()
        
        if existing_user.data:
            raise HTTPException(status_code=400, detail="Username or email already registered")
        
        # Create user
        hashed_pw = self.hash_password(user_data.password)
        user_response = self.supabase.table("users").insert({
            "username": user_data.username,
            "email": user_data.email,
            "hashed_password": hashed_pw
        }).execute()
        
        if not user_response.data:
            raise HTTPException(status_code=400, detail="Failed to create user")
        
        user_id = user_response.data[0]["id"]
        
        # Create default portfolio
        self.supabase.table("portfolios").insert({
            "user_id": user_id,
            "name": "Default Portfolio"
        }).execute()
        
        # Create default watchlist
        self.supabase.table("watchlists").insert({
            "user_id": user_id,
            "tickers": []
        }).execute()
        
        # Create access token
        access_token = self.create_access_token(data={"sub": user_data.username})
        return Token(access_token=access_token, token_type="bearer")

    async def login_user(self, user_data: UserLogin) -> Token:
        """Authenticate and login a user"""
        user_response = self.supabase.table("users").select("*").eq("username", user_data.username).execute()
        
        if not user_response.data:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user = user_response.data[0]
        if not self.verify_password(user_data.password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = self.create_access_token(data={"sub": user["username"]})
        return Token(access_token=access_token, token_type="bearer")

    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
        """Get current authenticated user from JWT token"""
        try:
            token = credentials.credentials
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Query user from Supabase
        response = self.supabase.table("users").select("*").eq("username", username).execute()
        if not response.data:
            raise HTTPException(status_code=401, detail="User not found")
        
        return response.data[0]

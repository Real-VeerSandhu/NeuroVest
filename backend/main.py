from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, UUID4, HttpUrl
from supabase import create_client, Client
from datetime import datetime, timedelta
import jwt
import yfinance as yf
import uuid
from typing import List, Optional, Dict, Any
import bcrypt
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


# JWT Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPI setup
app = FastAPI(title="Finance Portfolio API", version="1.0.0")
security = HTTPBearer()

# Pydantic Models (same as before)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class StockInfo(BaseModel):
    ticker: str
    name: str
    price: float
    address: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    exchange: Optional[str] = None
    market_cap: Optional[float] = None
    currency: Optional[str] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    dividend_yield: Optional[float] = None
    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    eps: Optional[float] = None
    beta: Optional[float] = None
    volume: Optional[int] = None
    average_volume: Optional[int] = None
    website: Optional[HttpUrl] = None
    short_description: Optional[str] = None
    is_etf: Optional[bool] = False

class PositionAdd(BaseModel):
    ticker: str
    shares: int

class PositionResponse(BaseModel):
    id: str
    ticker: str
    shares: int
    created_at: datetime

class PortfolioResponse(BaseModel):
    id: str
    name: str
    positions: List[PositionResponse]
    created_at: datetime

class TickerAdd(BaseModel):
    ticker: str

class WatchlistResponse(BaseModel):
    id: str
    tickers: List[str]
    created_at: datetime

# Database Table Creation Functions
def create_tables():
    """
    Create tables in Supabase PostgreSQL database.
    Run this once to set up your database schema.
    """
    
    # Create users table
    users_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    """
    
    # Create portfolios table
    portfolios_sql = """
    CREATE TABLE IF NOT EXISTS portfolios (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        name TEXT NOT NULL DEFAULT 'Default Portfolio',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_portfolios_user_id ON portfolios(user_id);
    """
    
    # Create positions table
    positions_sql = """
    CREATE TABLE IF NOT EXISTS positions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        portfolio_id UUID NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
        ticker TEXT NOT NULL,
        shares INTEGER NOT NULL CHECK (shares > 0),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_positions_portfolio_id ON positions(portfolio_id);
    CREATE INDEX IF NOT EXISTS idx_positions_ticker ON positions(ticker);
    """
    
    # Create watchlists table
    watchlists_sql = """
    CREATE TABLE IF NOT EXISTS watchlists (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        tickers JSONB DEFAULT '[]'::jsonb,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_watchlists_user_id ON watchlists(user_id);
    """
    
    try:
        # Execute each SQL statement
        supabase.postgrest.rpc('exec_sql', {'sql': users_sql}).execute()
        supabase.postgrest.rpc('exec_sql', {'sql': portfolios_sql}).execute()
        supabase.postgrest.rpc('exec_sql', {'sql': positions_sql}).execute()
        supabase.postgrest.rpc('exec_sql', {'sql': watchlists_sql}).execute()
        
        print("Tables created successfully!")
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        # Alternative method if RPC doesn't work
        print("If the above failed, run these SQL commands directly in your Supabase SQL editor:")
        print("\n" + users_sql)
        print("\n" + portfolios_sql)
        print("\n" + positions_sql)
        print("\n" + watchlists_sql)

# Authentication functions (same as before)
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Query user from Supabase
    response = supabase.table("users").select("*").eq("username", username).execute()
    if not response.data:
        raise HTTPException(status_code=401, detail="User not found")
    
    return response.data[0]

# Stock data functions (same as before but cleaner)
def get_stock_info(ticker: str) -> Dict[str, Any]:
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

# Auth endpoints
@app.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    # Check if user exists
    existing_user = supabase.table("users").select("*").or_(
        f"username.eq.{user_data.username},email.eq.{user_data.email}"
    ).execute()
    
    if existing_user.data:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create user
    hashed_pw = hash_password(user_data.password)
    user_response = supabase.table("users").insert({
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hashed_pw
    }).execute()
    
    if not user_response.data:
        raise HTTPException(status_code=400, detail="Failed to create user")
    
    user_id = user_response.data[0]["id"]
    
    # Create default portfolio
    portfolio_response = supabase.table("portfolios").insert({
        "user_id": user_id,
        "name": "Default Portfolio"
    }).execute()
    
    # Create default watchlist
    watchlist_response = supabase.table("watchlists").insert({
        "user_id": user_id,
        "tickers": []
    }).execute()
    
    # Create access token
    access_token = create_access_token(data={"sub": user_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    user_response = supabase.table("users").select("*").eq("username", user_data.username).execute()
    
    if not user_response.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = user_response.data[0]
    if not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Stock research endpoints
@app.get("/research/{ticker}", response_model=StockInfo)
async def get_stock_research(ticker: str, current_user: dict = Depends(get_current_user)):
    return get_stock_info(ticker)

# Portfolio endpoints
@app.get("/portfolio", response_model=PortfolioResponse)
async def get_portfolio(current_user: dict = Depends(get_current_user)):
    # Get portfolio with positions
    portfolio_response = supabase.table("portfolios").select(
        "*, positions(*)"
    ).eq("user_id", current_user["id"]).execute()
    
    if not portfolio_response.data:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    portfolio = portfolio_response.data[0]
    
    # Format response
    return {
        "id": portfolio["id"],
        "name": portfolio["name"],
        "created_at": portfolio["created_at"],
        "positions": [
            {
                "id": pos["id"],
                "ticker": pos["ticker"],
                "shares": pos["shares"],
                "created_at": pos["created_at"]
            }
            for pos in portfolio.get("positions", [])
        ]
    }

@app.post("/portfolio/add")
async def add_position(
    position_data: PositionAdd, 
    current_user: dict = Depends(get_current_user)
):
    # Validate ticker
    get_stock_info(position_data.ticker)
    
    # Validate shares
    if position_data.shares <= 0:
        raise HTTPException(status_code=400, detail="Shares must be positive")
    
    # Get user's portfolio
    portfolio_response = supabase.table("portfolios").select("*").eq("user_id", current_user["id"]).execute()
    if not portfolio_response.data:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    portfolio_id = portfolio_response.data[0]["id"]
    ticker_upper = position_data.ticker.upper()
    
    # Check if position already exists
    existing_position = supabase.table("positions").select("*").eq("portfolio_id", portfolio_id).eq("ticker", ticker_upper).execute()
    
    if existing_position.data:
        # Update existing position
        position = existing_position.data[0]
        new_shares = position["shares"] + position_data.shares
        supabase.table("positions").update({"shares": new_shares}).eq("id", position["id"]).execute()
    else:
        # Create new position
        supabase.table("positions").insert({
            "portfolio_id": portfolio_id,
            "ticker": ticker_upper,
            "shares": position_data.shares
        }).execute()
    
    return {"message": f"Added {position_data.shares} shares of {ticker_upper}"}

@app.post("/portfolio/remove")
async def remove_position(
    position_data: PositionAdd,
    current_user: dict = Depends(get_current_user)
):
    # Get user's portfolio
    portfolio_response = supabase.table("portfolios").select("*").eq("user_id", current_user["id"]).execute()
    if not portfolio_response.data:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    portfolio_id = portfolio_response.data[0]["id"]
    ticker_upper = position_data.ticker.upper()
    
    # Find existing position
    position_response = supabase.table("positions").select("*").eq("portfolio_id", portfolio_id).eq("ticker", ticker_upper).execute()
    
    if not position_response.data:
        raise HTTPException(status_code=404, detail="Position not found")
    
    position = position_response.data[0]
    
    if position_data.shares >= position["shares"]:
        # Remove entire position
        supabase.table("positions").delete().eq("id", position["id"]).execute()
        message = f"Removed all shares of {ticker_upper}"
    else:
        # Reduce shares
        new_shares = position["shares"] - position_data.shares
        supabase.table("positions").update({"shares": new_shares}).eq("id", position["id"]).execute()
        message = f"Reduced {ticker_upper} by {position_data.shares} shares"
    
    return {"message": message}

# Watchlist endpoints
@app.get("/watchlist", response_model=WatchlistResponse)
async def get_watchlist(current_user: dict = Depends(get_current_user)):
    watchlist_response = supabase.table("watchlists").select("*").eq("user_id", current_user["id"]).execute()
    
    if not watchlist_response.data:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    watchlist = watchlist_response.data[0]
    return {
        "id": watchlist["id"],
        "tickers": watchlist.get("tickers", []),
        "created_at": watchlist["created_at"]
    }

@app.post("/watchlist/add")
async def add_to_watchlist(
    ticker_data: TickerAdd,
    current_user: dict = Depends(get_current_user)
):
    # Validate ticker
    get_stock_info(ticker_data.ticker)
    
    # Get user's watchlist
    watchlist_response = supabase.table("watchlists").select("*").eq("user_id", current_user["id"]).execute()
    
    if not watchlist_response.data:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    watchlist = watchlist_response.data[0]
    ticker_upper = ticker_data.ticker.upper()
    current_tickers = watchlist.get("tickers", [])
    
    if ticker_upper not in current_tickers:
        current_tickers.append(ticker_upper)
        supabase.table("watchlists").update({"tickers": current_tickers}).eq("id", watchlist["id"]).execute()
        return {"message": f"Added {ticker_upper} to watchlist"}
    else:
        return {"message": f"{ticker_upper} already in watchlist"}

@app.post("/watchlist/remove")
async def remove_from_watchlist(
    ticker_data: TickerAdd,
    current_user: dict = Depends(get_current_user)
):
    # Get user's watchlist
    watchlist_response = supabase.table("watchlists").select("*").eq("user_id", current_user["id"]).execute()
    
    if not watchlist_response.data:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    watchlist = watchlist_response.data[0]
    ticker_upper = ticker_data.ticker.upper()
    current_tickers = watchlist.get("tickers", [])
    
    if ticker_upper in current_tickers:
        current_tickers.remove(ticker_upper)
        supabase.table("watchlists").update({"tickers": current_tickers}).eq("id", watchlist["id"]).execute()
        return {"message": f"Removed {ticker_upper} from watchlist"}
    else:
        raise HTTPException(status_code=404, detail="Ticker not in watchlist")

# Health check
@app.get("/")
async def root():
    return {"message": "Finance Portfolio API with Supabase is running!"}

# Database setup function - call this once to create tables
@app.get("/setup-database")
async def setup_database():
    """
    Call this endpoint once to create the database tables
    Remove this endpoint in production
    """
    create_tables()
    return {"message": "Database tables created successfully!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from .routers import auth_router, stock_router, portfolio_router, watchlist_router
from .utils.database import create_tables
from .utils.dependencies import get_supabase_client

# Initialize FastAPI app
app = FastAPI(
    title="Finance Portfolio API",
    description="A comprehensive finance portfolio management API with Supabase backend",
    version="1.0.0"
)

# Include routers
app.include_router(auth_router)
app.include_router(stock_router)
app.include_router(portfolio_router)
app.include_router(watchlist_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Finance Portfolio API with Supabase is running!"}


@app.get("/setup-database")
async def setup_database():
    """
    Call this endpoint once to create the database tables.
    Remove this endpoint in production for security.
    """
    supabase = get_supabase_client()
    create_tables(supabase)
    return {"message": "Database tables created successfully!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

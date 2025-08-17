from supabase import Client


def create_tables(supabase: Client):
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

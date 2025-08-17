# NeuroVest: Finance Portfolio Management System

A comprehensive portfolio management and research platform built with FastAPI backend, React TypeScript frontend, and PostgreSQL database. The system provides real-time stock data, portfolio management, watchlist functionality, and advanced simulation capabilities including Monte Carlo analysis and forecasting.

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLModel / SQLAlchemy
- **Stock Data**: Yahoo Finance API (yfinance)
- **Authentication**: JWT/OAuth2
- **Server**: Uvicorn

### Frontend
- **Framework**: React with TypeScript
- **UI Library**: TBD (Material-UI/Tailwind CSS recommended)
- **State Management**: React Query / SWR
- **Charts**: Chart.js / Recharts for visualization

### Database
- **Platform**: Supabase (PostgreSQL)
- **Connection**: asyncpg
- **Migrations**: Alembic

## Features

### Core Functionality
- Real-time stock price lookup and company information
- Portfolio management with position tracking
- Watchlist management for stock monitoring
- User authentication and authorization

### Advanced Analytics
- Monte Carlo simulation for portfolio risk assessment
- Time series forecasting using statistical models
- Portfolio performance analytics and metrics
- Risk-return optimization analysis

## API Documentation

### Stock Research
```
GET /research/{ticker}
```
Retrieve current stock information including price, market cap, sector, and key metrics.

**Response:**
```json
{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "price": 185.25,
  "market_cap": 2850000000000,
  "sector": "Technology",
  "pe_ratio": 28.5,
  "52_week_high": 198.23,
  "52_week_low": 124.17
}
```

### Portfolio Management
```
GET /portfolio
POST /portfolio/add
POST /portfolio/remove
```

**Add Position Request:**
```json
{
  "ticker": "AAPL",
  "shares": 10
}
```

### Watchlist Management
```
GET /watchlist
POST /watchlist/add
POST /watchlist/remove
```

### Simulation & Analytics
```
POST /portfolio/monte-carlo
POST /portfolio/forecast
GET /portfolio/analytics
```

**Monte Carlo Simulation Request:**
```json
{
  "portfolio_id": "uuid",
  "time_horizon": 252,
  "simulations": 10000,
  "confidence_levels": [0.05, 0.95]
}
```

**Forecast Request:**
```json
{
  "portfolio_id": "uuid",
  "forecast_days": 30,
  "model_type": "ARIMA"
}
```

## Database Schema

### Core Tables

#### portfolios
```sql
CREATE TABLE portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### positions
```sql
CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID REFERENCES portfolios(id) ON DELETE CASCADE,
    ticker VARCHAR(10) NOT NULL,
    shares INTEGER NOT NULL CHECK (shares > 0),
    avg_cost DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### watchlists
```sql
CREATE TABLE watchlists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, ticker)
);
```

#### simulation_results
```sql
CREATE TABLE simulation_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID REFERENCES portfolios(id) ON DELETE CASCADE,
    simulation_type VARCHAR(50) NOT NULL,
    parameters JSONB NOT NULL,
    results JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL (via Supabase account)

### Backend Setup
```bash
# Clone repository
git clone <repository-url>
cd finance-portfolio-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.example .env.local
# Edit with your API endpoint

# Start development server
npm run dev
```

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:port/database
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
JWT_SECRET_KEY=your_jwt_secret
YAHOO_FINANCE_API_KEY=optional_api_key
```

#### Frontend (.env.local)
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_SUPABASE_URL=your_supabase_url
REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Simulation Features

### Monte Carlo Analysis
Performs risk assessment using Monte Carlo simulation to project potential portfolio outcomes:

- **Inputs**: Portfolio positions, time horizon, number of simulations
- **Outputs**: Value-at-Risk (VaR), Conditional VaR, confidence intervals
- **Visualization**: Histogram of simulated returns, percentile analysis

### Forecasting Models
Implements multiple forecasting approaches:

- **ARIMA**: Autoregressive Integrated Moving Average for time series prediction
- **LSTM**: Long Short-Term Memory neural networks for complex pattern recognition
- **Linear Regression**: Simple trend analysis for baseline comparison

### Risk Metrics
- Sharpe Ratio calculation
- Maximum Drawdown analysis
- Beta coefficient relative to market indices
- Portfolio volatility and correlation analysis

## Development

### Project Structure
```
├── backend/
│   ├── app/
│   │   ├── models/          # SQLModel schemas
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── utils/           # Helper functions
│   │   └── main.py          # FastAPI application
│   ├── migrations/          # Alembic migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Route components
│   │   ├── services/       # API calls
│   │   ├── types/          # TypeScript definitions
│   │   └── utils/          # Helper functions
│   └── package.json
└── README.md
```

### Testing
```bash
# Backend tests
pytest

# Frontend tests
npm test

# End-to-end tests
npm run test:e2e
```

### Production Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Rate Limits
- Yahoo Finance: 2000 requests/hour (free tier)
- Consider implementing caching for frequently requested stock data
- Use Redis for session management and data caching

## Contributing
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request with detailed description

## License
MIT License - see LICENSE file for details

## Support
For issues and questions, please create an issue in the GitHub repository or contact the development team.
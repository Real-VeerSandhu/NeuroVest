import requests
import json
import getpass
from typing import Optional

# API base URL
BASE_URL = "http://localhost:8000"

def get_user_input():
    """Get user credentials and choice to login or signup"""
    print("🏦 Welcome to Finance Portfolio API!")
    print("=" * 50)
    
    # Ask for login or signup
    while True:
        choice = input("Do you want to (l)ogin or (s)ignup? (l/s): ").lower().strip()
        if choice in ['l', 'login', 's', 'signup']:
            break
        print("❌ Please enter 'l' for login or 's' for signup")
    
    # Get username
    username = input("Username: ").strip()
    
    # Get password (hidden input)
    password = getpass.getpass("Password: ")
    
    # Get email if signing up
    email = None
    if choice in ['s', 'signup']:
        email = input("Email: ").strip()
    
    return choice, username, password, email

def authenticate_user(choice: str, username: str, password: str, email: Optional[str]) -> Optional[str]:
    """Authenticate user and return access token"""
    
    if choice in ['s', 'signup']:
        print(f"\n📝 Registering user '{username}'...")
        register_data = {
            "username": username,
            "email": email,
            "password": password
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Registration successful!")
            return token_data["access_token"]
        else:
            error_detail = response.json().get("detail", "Unknown error")
            print(f"❌ Registration failed: {error_detail}")
            return None
            
    else:  # login
        print(f"\n🔐 Logging in user '{username}'...")
        login_data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Login successful!")
            return token_data["access_token"]
        else:
            error_detail = response.json().get("detail", "Unknown error")
            print(f"❌ Login failed: {error_detail}")
            return None

def interactive_api_test(access_token: str):
    """Interactive API testing with user input"""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    while True:
        print("\n" + "="*60)
        print("📊 FINANCE PORTFOLIO API - MAIN MENU")
        print("="*60)
        print("1. 🔍 Research a stock")
        print("2. 💼 View portfolio")
        print("3. ➕ Add stock to portfolio")
        print("4. ➖ Remove stock from portfolio")
        print("5. 👀 View watchlist")
        print("6. ➕ Add stock to watchlist")
        print("7. ➖ Remove stock from watchlist")
        print("8. 🧪 Run all tests automatically")
        print("9. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            research_stock(headers)
        elif choice == "2":
            view_portfolio(headers)
        elif choice == "3":
            add_to_portfolio(headers)
        elif choice == "4":
            remove_from_portfolio(headers)
        elif choice == "5":
            view_watchlist(headers)
        elif choice == "6":
            add_to_watchlist(headers)
        elif choice == "7":
            remove_from_watchlist(headers)
        elif choice == "8":
            run_automated_tests(headers)
        elif choice == "9":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-9.")

def research_stock(headers):
    """Research a stock"""
    ticker = input("Enter stock ticker (e.g., AAPL): ").strip().upper()
    if not ticker:
        print("❌ Please enter a valid ticker")
        return
    
    print(f"\n🔍 Researching {ticker}...")
    response = requests.get(f"{BASE_URL}/research/{ticker}", headers=headers)
    
    if response.status_code == 200:
        stock_data = response.json()
        print(f"✅ Stock research successful!")
        # print(f"   📊 Company: {stock_data['name']}")
        # print(f"   💰 Price: ${stock_data['price']:.2f} {stock_data['currency']}")
        # print(f"   🏢 Sector: {stock_data['sector'] or 'N/A'}")
        # if stock_data['market_cap']:
        #     print(f"   📈 Market Cap: ${stock_data['market_cap']:,}")
        
        for key, value in stock_data.items():
            formatted_key = key.replace('_', ' ').title()
            print(f"{formatted_key}: {value}")
        
        print("=" * 40)
    else:
        error_detail = response.json().get("detail", "Unknown error")
        print(f"❌ Stock research failed: {error_detail}")

def view_portfolio(headers):
    """View user's portfolio"""
    print(f"\n💼 Getting your portfolio...")
    response = requests.get(f"{BASE_URL}/portfolio", headers=headers)
    
    if response.status_code == 200:
        portfolio = response.json()
        print(f"✅ Portfolio retrieved successfully!")
        print(f"📁 Portfolio: {portfolio['name']}")
        
        if portfolio['positions']:
            print(f"📊 You have {len(portfolio['positions'])} positions:")
            for pos in portfolio['positions']:
                print(f"   • {pos['ticker']}: {pos['shares']} shares")
        else:
            print("   📭 Your portfolio is empty")
    else:
        error_detail = response.json().get("detail", "Unknown error")
        print(f"❌ Failed to get portfolio: {error_detail}")

def add_to_portfolio(headers):
    """Add stock position to portfolio"""
    ticker = input("Enter stock ticker: ").strip().upper()
    if not ticker:
        print("❌ Please enter a valid ticker")
        return
    
    try:
        shares = int(input("Enter number of shares: ").strip())
        if shares <= 0:
            print("❌ Shares must be a positive number")
            return
    except ValueError:
        print("❌ Please enter a valid number of shares")
        return
    
    print(f"\n➕ Adding {shares} shares of {ticker}...")
    position_data = {"ticker": ticker, "shares": shares}
    response = requests.post(f"{BASE_URL}/portfolio/add", json=position_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        error_detail = response.json().get("detail", "Unknown error")
        print(f"❌ Failed to add position: {error_detail}")

def remove_from_portfolio(headers):
    """Remove stock position from portfolio"""
    ticker = input("Enter stock ticker: ").strip().upper()
    if not ticker:
        print("❌ Please enter a valid ticker")
        return
    
    try:
        shares = int(input("Enter number of shares to remove: ").strip())
        if shares <= 0:
            print("❌ Shares must be a positive number")
            return
    except ValueError:
        print("❌ Please enter a valid number of shares")
        return
    
    print(f"\n➖ Removing {shares} shares of {ticker}...")
    position_data = {"ticker": ticker, "shares": shares}
    response = requests.post(f"{BASE_URL}/portfolio/remove", json=position_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        error_detail = response.json().get("detail", "Unknown error")
        print(f"❌ Failed to remove position: {error_detail}")

def view_watchlist(headers):
    """View user's watchlist"""
    print(f"\n👀 Getting your watchlist...")
    response = requests.get(f"{BASE_URL}/watchlist", headers=headers)
    
    if response.status_code == 200:
        watchlist = response.json()
        print(f"✅ Watchlist retrieved successfully!")
        
        if watchlist['tickers']:
            print(f"📋 Watching {len(watchlist['tickers'])} stocks:")
            print(f"   {', '.join(watchlist['tickers'])}")
        else:
            print("   📭 Your watchlist is empty")
    else:
        error_detail = response.json().get("detail", "Unknown error")
        print(f"❌ Failed to get watchlist: {error_detail}")

def add_to_watchlist(headers):
    """Add ticker to watchlist"""
    ticker = input("Enter stock ticker: ").strip().upper()
    if not ticker:
        print("❌ Please enter a valid ticker")
        return
    
    print(f"\n➕ Adding {ticker} to watchlist...")
    ticker_data = {"ticker": ticker}
    response = requests.post(f"{BASE_URL}/watchlist/add", json=ticker_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        error_detail = response.json().get("detail", "Unknown error")
        print(f"❌ Failed to add to watchlist: {error_detail}")

def remove_from_watchlist(headers):
    """Remove ticker from watchlist"""
    ticker = input("Enter stock ticker: ").strip().upper()
    if not ticker:
        print("❌ Please enter a valid ticker")
        return
    
    print(f"\n➖ Removing {ticker} from watchlist...")
    ticker_data = {"ticker": ticker}
    response = requests.post(f"{BASE_URL}/watchlist/remove", json=ticker_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        error_detail = response.json().get("detail", "Unknown error")
        print(f"❌ Failed to remove from watchlist: {error_detail}")

def run_automated_tests(headers):
    """Run automated tests like the original function"""
    print("\n🧪 Running automated tests...")
    
    # Test 1: Research a stock
    print("\n1. 🔍 Researching AAPL stock...")
    response = requests.get(f"{BASE_URL}/research/AAPL", headers=headers)
    if response.status_code == 200:
        stock_data = response.json()
        print(f"✅ Stock research successful!")
        print(f"   {stock_data['name']}: ${stock_data['price']:.2f}")
    else:
        print(f"❌ Stock research failed: {response.text}")
    
    # Test 2: Add position to portfolio
    print("\n2. ➕ Adding AAPL position to portfolio...")
    position_data = {"ticker": "AAPL", "shares": 5}
    response = requests.post(f"{BASE_URL}/portfolio/add", json=position_data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Failed to add position: {response.text}")
    
    # Test 3: Get portfolio
    print("\n3. 💼 Getting portfolio...")
    response = requests.get(f"{BASE_URL}/portfolio", headers=headers)
    if response.status_code == 200:
        portfolio = response.json()
        print(f"✅ Portfolio retrieved successfully!")
        print(f"   Portfolio has {len(portfolio['positions'])} positions")
        for pos in portfolio['positions']:
            print(f"   • {pos['ticker']}: {pos['shares']} shares")
    else:
        print(f"❌ Failed to get portfolio: {response.text}")
    
    # Test 4: Add to watchlist
    print("\n4. ➕ Adding TSLA to watchlist...")
    ticker_data = {"ticker": "TSLA"}
    response = requests.post(f"{BASE_URL}/watchlist/add", json=ticker_data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Failed to add to watchlist: {response.text}")
    
    # Test 5: Get watchlist
    print("\n5. 👀 Getting watchlist...")
    response = requests.get(f"{BASE_URL}/watchlist", headers=headers)
    if response.status_code == 200:
        watchlist = response.json()
        print(f"✅ Watchlist retrieved successfully!")
        if watchlist['tickers']:
            print(f"   Watchlist contains: {', '.join(watchlist['tickers'])}")
        else:
            print("   Watchlist is empty")
    else:
        print(f"❌ Failed to get watchlist: {response.text}")
    
    print("\n✅ All automated tests completed!")

def main():
    """Main function"""
    try:
        # Check if API is running
        try:
            response = requests.get(f"{BASE_URL}/")
            if response.status_code != 200:
                raise Exception("API not responding correctly")
        except Exception:
            print("❌ Cannot connect to API. Make sure the FastAPI server is running on http://localhost:8000")
            print("💡 Run: python main.py")
            return
        
        # Get user credentials and authenticate
        choice, username, password, email = get_user_input()
        access_token = authenticate_user(choice, username, password, email)
        
        if access_token:
            print(f"🎉 Authentication successful!")
            interactive_api_test(access_token)
        else:
            print("💔 Authentication failed. Please try again.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
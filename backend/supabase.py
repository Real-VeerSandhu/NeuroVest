import requests
import json
import getpass
from typing import Optional
import time

# API base URL
BASE_URL = "http://localhost:8000"

def get_user_input():
    """Get user credentials and choice to login or signup"""
    print("🏦 Welcome to Finance Portfolio API with Supabase!")
    print("=" * 60)
    
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
        if not email or '@' not in email:
            print("❌ Please enter a valid email address")
            return get_user_input()
    
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
        
        try:
            response = requests.post(f"{BASE_URL}/auth/register", json=register_data, timeout=10)
            if response.status_code == 200:
                token_data = response.json()
                print(f"✅ Registration successful!")
                print(f"🎉 Welcome {username}! Your account has been created.")
                return token_data["access_token"]
            else:
                error_detail = response.json().get("detail", "Unknown error")
                print(f"❌ Registration failed: {error_detail}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error during registration: {e}")
            return None
            
    else:  # login
        print(f"\n🔐 Logging in user '{username}'...")
        login_data = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
            if response.status_code == 200:
                token_data = response.json()
                print(f"✅ Login successful!")
                print(f"🎉 Welcome back {username}!")
                return token_data["access_token"]
            else:
                error_detail = response.json().get("detail", "Unknown error")
                print(f"❌ Login failed: {error_detail}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error during login: {e}")
            return None

def interactive_api_test(access_token: str):
    """Interactive API testing with user input"""
    headers = {"Authorization": f"Bearer {access_token}"}
    
    while True:
        print("\n" + "="*60)
        print("📊 FINANCE PORTFOLIO API - MAIN MENU (Supabase Edition)")
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
    ticker = input("Enter stock ticker (e.g., AAPL, TSLA, MSFT): ").strip().upper()
    if not ticker:
        print("❌ Please enter a valid ticker")
        return
    
    print(f"\n🔍 Researching {ticker}...")
    print("⏳ Fetching data from Yahoo Finance...")
    
    try:
        response = requests.get(f"{BASE_URL}/research/{ticker}", headers=headers, timeout=15)
        
        if response.status_code == 200:
            stock_data = response.json()
            print(f"✅ Stock research successful!\n")
            print("=" * 50)
            print(f"📊 {stock_data['name']} ({stock_data['ticker']})")
            print("=" * 50)
            
            # Format and display key information
            if stock_data.get('price'):
                print(f"💰 Current Price: ${stock_data['price']:.2f} {stock_data.get('currency', 'USD')}")
            
            if stock_data.get('market_cap'):
                market_cap_b = stock_data['market_cap'] / 1_000_000_000
                print(f"📈 Market Cap: ${market_cap_b:.2f}B")
            
            if stock_data.get('sector'):
                print(f"🏢 Sector: {stock_data['sector']}")
            
            if stock_data.get('industry'):
                print(f"🏭 Industry: {stock_data['industry']}")
            
            if stock_data.get('pe_ratio'):
                print(f"📊 P/E Ratio: {stock_data['pe_ratio']:.2f}")
            
            if stock_data.get('fifty_two_week_high') and stock_data.get('fifty_two_week_low'):
                print(f"📉📈 52-Week Range: ${stock_data['fifty_two_week_low']:.2f} - ${stock_data['fifty_two_week_high']:.2f}")
            
            if stock_data.get('volume'):
                volume_m = stock_data['volume'] / 1_000_000
                print(f"📊 Volume: {volume_m:.2f}M")
            
            if stock_data.get('dividend_yield'):
                print(f"💎 Dividend Yield: {stock_data['dividend_yield']*100:.2f}%")
            
            if stock_data.get('short_description'):
                print(f"\n📝 Description: {stock_data['short_description']}")
            
            print("=" * 50)
        else:
            error_detail = response.json().get("detail", "Unknown error")
            print(f"❌ Stock research failed: {error_detail}")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The stock data service might be slow.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

def view_portfolio(headers):
    """View user's portfolio"""
    print(f"\n💼 Getting your portfolio...")
    
    try:
        response = requests.get(f"{BASE_URL}/portfolio", headers=headers, timeout=10)
        
        if response.status_code == 200:
            portfolio = response.json()
            print(f"✅ Portfolio retrieved successfully!\n")
            print("=" * 40)
            print(f"📁 Portfolio: {portfolio['name']}")
            print(f"🕐 Created: {portfolio['created_at'][:19].replace('T', ' ')}")
            print("=" * 40)
            
            if portfolio['positions']:
                print(f"📊 You have {len(portfolio['positions'])} position(s):")
                total_positions = 0
                for pos in portfolio['positions']:
                    print(f"   • {pos['ticker']}: {pos['shares']:,} shares")
                    total_positions += pos['shares']
                print(f"\n💯 Total shares across all positions: {total_positions:,}")
            else:
                print("   📭 Your portfolio is empty")
                print("   💡 Try adding some stocks with option 3!")
        else:
            error_detail = response.json().get("detail", "Unknown error")
            print(f"❌ Failed to get portfolio: {error_detail}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

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
    
    print(f"\n➕ Adding {shares:,} shares of {ticker}...")
    print("⏳ Validating ticker and updating portfolio...")
    
    position_data = {"ticker": ticker, "shares": shares}
    
    try:
        response = requests.post(f"{BASE_URL}/portfolio/add", json=position_data, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            print(f"🎉 Your portfolio has been updated!")
        else:
            error_detail = response.json().get("detail", "Unknown error")
            print(f"❌ Failed to add position: {error_detail}")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. This might happen when validating the ticker.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

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
    
    print(f"\n➖ Removing {shares:,} shares of {ticker}...")
    position_data = {"ticker": ticker, "shares": shares}
    
    try:
        response = requests.post(f"{BASE_URL}/portfolio/remove", json=position_data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
        else:
            error_detail = response.json().get("detail", "Unknown error")
            print(f"❌ Failed to remove position: {error_detail}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

def view_watchlist(headers):
    """View user's watchlist"""
    print(f"\n👀 Getting your watchlist...")
    
    try:
        response = requests.get(f"{BASE_URL}/watchlist", headers=headers, timeout=10)
        
        if response.status_code == 200:
            watchlist = response.json()
            print(f"✅ Watchlist retrieved successfully!\n")
            print("=" * 40)
            print(f"📋 Your Watchlist")
            print(f"🕐 Created: {watchlist['created_at'][:19].replace('T', ' ')}")
            print("=" * 40)
            
            if watchlist['tickers']:
                print(f"👀 Watching {len(watchlist['tickers'])} stock(s):")
                for i, ticker in enumerate(watchlist['tickers'], 1):
                    print(f"   {i}. {ticker}")
            else:
                print("   📭 Your watchlist is empty")
                print("   💡 Try adding some stocks to watch with option 6!")
        else:
            error_detail = response.json().get("detail", "Unknown error")
            print(f"❌ Failed to get watchlist: {error_detail}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

def add_to_watchlist(headers):
    """Add ticker to watchlist"""
    ticker = input("Enter stock ticker: ").strip().upper()
    if not ticker:
        print("❌ Please enter a valid ticker")
        return
    
    print(f"\n➕ Adding {ticker} to watchlist...")
    print("⏳ Validating ticker...")
    
    ticker_data = {"ticker": ticker}
    
    try:
        response = requests.post(f"{BASE_URL}/watchlist/add", json=ticker_data, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
        else:
            error_detail = response.json().get("detail", "Unknown error")
            print(f"❌ Failed to add to watchlist: {error_detail}")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. This might happen when validating the ticker.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

def remove_from_watchlist(headers):
    """Remove ticker from watchlist"""
    ticker = input("Enter stock ticker: ").strip().upper()
    if not ticker:
        print("❌ Please enter a valid ticker")
        return
    
    print(f"\n➖ Removing {ticker} from watchlist...")
    ticker_data = {"ticker": ticker}
    
    try:
        response = requests.post(f"{BASE_URL}/watchlist/remove", json=ticker_data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
        else:
            error_detail = response.json().get("detail", "Unknown error")
            print(f"❌ Failed to remove from watchlist: {error_detail}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

def run_automated_tests(headers):
    """Run automated tests like the original function"""
    print("\n🧪 Running automated tests with Supabase backend...")
    print("⏳ This may take a moment due to stock data fetching...")
    
    tests = [
        ("🔍 Researching AAPL stock", lambda: requests.get(f"{BASE_URL}/research/AAPL", headers=headers, timeout=15)),
        ("➕ Adding AAPL position to portfolio", lambda: requests.post(f"{BASE_URL}/portfolio/add", json={"ticker": "AAPL", "shares": 10}, headers=headers, timeout=15)),
        ("💼 Getting portfolio", lambda: requests.get(f"{BASE_URL}/portfolio", headers=headers, timeout=10)),
        ("➕ Adding TSLA to watchlist", lambda: requests.post(f"{BASE_URL}/watchlist/add", json={"ticker": "TSLA"}, headers=headers, timeout=15)),
        ("➕ Adding MSFT to watchlist", lambda: requests.post(f"{BASE_URL}/watchlist/add", json={"ticker": "MSFT"}, headers=headers, timeout=15)),
        ("👀 Getting watchlist", lambda: requests.get(f"{BASE_URL}/watchlist", headers=headers, timeout=10))
    ]
    
    passed = 0
    failed = 0
    
    for i, (description, test_func) in enumerate(tests, 1):
        print(f"\n{i}. {description}...")
        
        try:
            response = test_func()
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success!")
                
                # Show specific results
                if "research" in description.lower():
                    print(f"   📊 {result['name']}: ${result['price']:.2f}")
                elif "portfolio" in description.lower() and "Getting" in description:
                    print(f"   📁 Portfolio has {len(result['positions'])} position(s)")
                elif "watchlist" in description.lower() and "Getting" in description:
                    print(f"   👀 Watchlist has {len(result['tickers'])} ticker(s)")
                elif "message" in result:
                    print(f"   💬 {result['message']}")
                    
                passed += 1
            else:
                error_detail = response.json().get("detail", "Unknown error")
                print(f"   ❌ Failed: {error_detail}")
                failed += 1
        except requests.exceptions.Timeout:
            print(f"   ⏰ Test timed out")
            failed += 1
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Connection error: {e}")
            failed += 1
    
    print(f"\n" + "="*50)
    print(f"🧪 TEST RESULTS")
    print(f"="*50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    print(f"="*50)

def check_api_health():
    """Check if the API is running and healthy"""
    print("🔍 Checking API health...")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API is running: {result.get('message', 'OK')}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the FastAPI server is running.")
        print("💡 Run: python main.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ API is not responding (timeout)")
        return False
    except Exception as e:
        print(f"❌ Unexpected error checking API: {e}")
        return False

def main():
    """Main function"""
    try:
        print("🚀 Starting Finance Portfolio Client...")
        
        # Check if API is running
        if not check_api_health():
            return
        
        # Get user credentials and authenticate
        choice, username, password, email = get_user_input()
        access_token = authenticate_user(choice, username, password, email)
        
        if access_token:
            print(f"🔑 Authentication token received!")
            time.sleep(1)  # Small pause for better UX
            interactive_api_test(access_token)
        else:
            print("💔 Authentication failed. Please try again.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
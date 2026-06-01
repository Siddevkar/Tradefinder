import requests
import json

# Configuration
TRADETRON_WEBHOOK_URL = "https://api.tradetron.tech/api/?auth-token=YOUR_TRADETRON_TOKEN"

def get_market_data():
    # Replace with your data provider endpoint (e.g., Deven Securities, Fyers, Zerodha, or rapidAPI NSE data)
    # This example demonstrates the exact mathematical logic required
    url = "https://api.example.com/nse-market-snapshot" 
    response = requests.get(url).json()
    return response

def process_strategy():
    data = get_market_data()
    
    # 1. Sector Level Ranking
    sectors = data['sectors'] # Expected format: [{"name": "NIFTY IT", "pct_change": 1.5}, ...]
    top_sector = max(sectors, key=lambda x: x['pct_change'])
    print(f"Top Performing Sector: {top_sector['name']} ({top_sector['pct_change']}%)")
    
    # 2. Stock Level Ranking within the top sector
    stocks = data['stocks'][top_sector['name']] # Filtered to top sector constituents
    # Sort stocks by % change descending to find the top performer
    top_stock = max(stocks, key=lambda x: x['pct_change'])
    print(f"Top Performing Stock: {top_stock['symbol']} ({top_stock['pct_change']}%)")
    
    # 3. Check technical trigger (Supertrend breakout confirmation can be done here or left to Tradetron)
    if top_stock['close'] > top_stock['supertrend']:
        payload = {
            "auth-token": "YOUR_TRADETRON_TOKEN",
            "stock": top_stock['symbol'],
            "signal": "BUY"
        }
        
        # Send to Tradetron
        headers = {'Content-Type': 'application/json'}
        response = requests.post(TRADETRON_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        print(f"Webhook sent to Tradetron. Response: {response.status_code}")
    else:
        print("Top stock did not cross Supertrend. No trade executed.")

if __name__ == "__main__":
    process_strategy()

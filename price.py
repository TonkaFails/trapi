import pandas as pd
import yfinance as yf
import requests
import os

DATA_DIR = os.getenv('DATA_PATH', 'data')

def get_ticker_details(isin):
    search_url = f"https://query2.finance.yahoo.com/v1/finance/search?q={isin}"
    try:
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
        symbol = response['quotes'][0]['symbol']
        info = yf.Ticker(symbol).info
        return symbol, info.get('currentPrice') or info.get('regularMarketPrice'), info.get('currency', 'EUR')
    except:
        return None, None, None

def get_rate(base, quote):
    if base == quote: return 1.0
    
    # map for pennies :)
    mapping = {'GBp': 'GBP', 'GBX': 'GBP', 'ILA': 'ILS', 'ZAc': 'ZAR'}
    clean_base = mapping.get(base, base)
    multiplier = 0.01 if base in ['GBp', 'GBX', 'ZAc'] else 1.0

    try:
        return yf.Ticker(f"{clean_base}{quote}=X").fast_info['last_price'] * multiplier
    except:
        try:
            return (1 / yf.Ticker(f"{quote}{clean_base}=X").fast_info['last_price']) * multiplier
        except:
            return None

def update_depot_with_currencies():
    dir = f'{DATA_DIR}/current_depot.csv'
    df = pd.read_csv(dir)

    cache = {}
    p_eur, p_usd = [], []

    for _, row in df.iterrows():
        _, price, currency = get_ticker_details(row['ISIN'])
        
        row_eur, row_usd = None, None
        if price and currency:
            for target in ['EUR', 'USD']:
                key = f"{currency}{target}"
                if key not in cache: cache[key] = get_rate(currency, target)
                
                rate = cache[key]
                if rate:
                    if target == 'EUR': row_eur = price * rate
                    if target == 'USD': row_usd = price * rate
        
        p_eur.append(row_eur)
        p_usd.append(row_usd)

    df['price_eur'], df['price_usd'] = p_eur, p_usd
    df['total_eur'], df['total_usd'] = df['Shares'] * df['price_eur'], df['Shares'] * df['price_usd']
    
    df[['price_eur', 'price_usd', 'total_eur', 'total_usd']] = df[['price_eur', 'price_usd', 'total_eur', 'total_usd']].round(4)
    df.to_csv(dir, index=False)

if __name__ == "__main__":
    update_depot_with_currencies()
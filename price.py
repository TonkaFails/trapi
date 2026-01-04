import pandas as pd
import yfinance as yf
import requests

# get ticker name by isin and currency of ticker
def get_ticker_details(isin):
    search_url = f"https://query2.finance.yahoo.com/v1/finance/search?q={isin}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(search_url, headers=headers).json()
        symbol = response['quotes'][0]['symbol']
        ticker = yf.Ticker(symbol)
        
        info = ticker.info
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        currency = info.get('currency', 'EUR')
        
        return symbol, price, currency
    except Exception:
        return None, None, None

def update_depot_with_currencies():
    df = pd.read_csv('data/current_depot.csv')

    # current eurusd rate
    fx = yf.Ticker("EURUSD=X").fast_info['last_price']
    print(f"1 EUR = {fx:.4f} USD")

    p_eur_list, p_usd_list = [], []

    for _, row in df.iterrows():
        symbol, price, currency = get_ticker_details(row['ISIN'])
        
        p_eur, p_usd = None, None
        
        if price:
            if currency == 'GBp':
                price /= 100
                currency = 'GBP'

            # conversion logic
            if currency == 'EUR':
                p_eur = price
                p_usd = price * fx
            elif currency == 'USD':
                p_usd = price
                p_eur = price / fx
            elif currency == 'GBP':
                gbp_eur = yf.Ticker("GBPEUR=X").fast_info['last_price']
                p_eur = price * gbp_eur
                p_usd = p_eur * fx
            else:
                p_eur = price
                p_usd = price * fx

        p_eur_list.append(p_eur)
        p_usd_list.append(p_usd)

    df['price_eur'] = p_eur_list
    df['price_usd'] = p_usd_list
    df['total_eur'] = df['Shares'] * df['price_eur']
    df['total_usd'] = df['Shares'] * df['price_usd']

    rounding = ['price_eur', 'price_usd', 'total_eur', 'total_usd']
    df[rounding] = df[rounding].round(4)


    df.to_csv('data/current_depot.csv', index=False)

if __name__ == "__main__":
    update_depot_with_currencies()
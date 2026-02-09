import yfinance as yf

def get_price(pair):
    try:
        t = yf.Ticker(pair + "=X")
        price = t.fast_info.get("last_price")
        return float(price) if price else None
    except:
        return None

import yfinance as yf

def get_current_price(pair):
    try:
        symbol = pair + "=X"
        ticker = yf.Ticker(symbol)

        # Metodo veloce (meno rate-limit)
        price = ticker.fast_info.get("last_price")

        if price is None:
            price = ticker.info.get("regularMarketPrice")

        return float(price) if price else None

    except Exception:
        return None

import yfinance as yf

def get_current_price(pair):
    symbol = pair + "=X"
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval="1m")

    if data.empty:
        return None

    return float(data["Close"].iloc[-1])
import yfinance as yf

YF_TICKERS = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "AUDUSD": "AUDUSD=X",
    "NZDUSD": "NZDUSD=X",
    "USDCHF": "USDCHF=X",
    "USDCAD": "USDCAD=X",
}

def get_price(pair):
    try:
        ticker = YF_TICKERS[pair]
        df = yf.download(
            ticker,
            period="1d",
            interval="1d",
            progress=False,
            threads=False
        )

        if df.empty:
            return None

        return round(float(df["Close"].iloc[-1]), 5)

    except Exception:
        return None

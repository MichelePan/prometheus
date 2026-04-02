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
            interval="5m",
            progress=False,
            threads=False
        )

        if df.empty:
            print(f"⚠️ DataFrame vuoto per {pair}")
            return None

        price = float(df["Close"].iloc[-1])
        print(f"{pair} -> {price}")

        return round(price, 5)

    except Exception as e:
        print(f"❌ Errore {pair}: {e}")
        return None

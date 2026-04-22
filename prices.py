import yfinance as yf

YF_TICKERS = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "AUDUSD": "AUDUSD=X",
    "NZDUSD": "NZDUSD=X",
    "USDCHF": "USDCHF=X",
    "USDCAD": "USDCAD=X",
}

# ===============================
# CACHE
# ===============================
_price_cache = {}
_last_valid_cache = {}


# ===============================
# DOWNLOAD BATCH (veloce ma instabile)
# ===============================
def _download_batch():
    try:
        tickers = list(YF_TICKERS.values())

        df = yf.download(
            tickers=" ".join(tickers),
            period="1d",
            interval="5m",
            group_by="ticker",
            progress=False,
            threads=True
        )

        prices = {}

        for pair, ticker in YF_TICKERS.items():
            try:
                if ticker not in df:
                    prices[pair] = None
                    continue

                data = df[ticker]

                if data is None or data.empty or "Close" not in data:
                    prices[pair] = None
                    continue

                price = float(data["Close"].iloc[-1])
                prices[pair] = round(price, 5)

            except Exception:
                prices[pair] = None

        return prices

    except Exception:
        return {pair: None for pair in YF_TICKERS}


# ===============================
# DOWNLOAD SINGOLO (affidabile)
# ===============================
def _download_single(ticker):
    try:
        df = yf.download(
            ticker,
            period="1d",
            interval="5m",
            progress=False
        )

        if df is None or df.empty or "Close" not in df:
            return None

        return round(float(df["Close"].iloc[-1]), 5)

    except Exception:
        return None


# ===============================
# MAIN
# ===============================
def get_price(pair):
    """
    Ritorna (price, source)
    source = "LIVE" o "CACHE"
    """
    global _price_cache, _last_valid_cache

    source = "CACHE"

    # 1️⃣ Se cache vuota → prova batch
    if not _price_cache:
        print("🔄 Batch download...")
        batch_prices = _download_batch()

        # 2️⃣ fallback singolo per i mancanti
        for pair_name, price in batch_prices.items():
            if price is None:
                ticker = YF_TICKERS[pair_name]
                print(f"↻ Fallback singolo: {pair_name}")
                price = _download_single(ticker)
                batch_prices[pair_name] = price

        _price_cache = batch_prices

        if any(v is not None for v in batch_prices.values()):
            source = "LIVE"

            # salva fallback buoni
            for k, v in batch_prices.items():
                if v is not None:
                    _last_valid_cache[k] = v

    price = _price_cache.get(pair)

    # 3️⃣ fallback finale
    if price is None:
        price = _last_valid_cache.get(pair)

        if price is not None:
            print(f"↩️ Uso fallback: {pair}")
            source = "CACHE"
        else:
            print(f"❌ Nessun dato: {pair}")

    return price, source


def clear_price_cache():
    global _price_cache
    _price_cache = {}

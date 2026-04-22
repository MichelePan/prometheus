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
# CACHE INTERNA (evita chiamate duplicate)
# ===============================
_price_cache = {}


def _download_all_prices():
    """
    Scarica tutti i prezzi in una sola chiamata
    """
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
                data = df[ticker]

                if data.empty:
                    print(f"⚠️ Vuoto: {pair}")
                    prices[pair] = None
                    continue

                price = float(data["Close"].iloc[-1])
                prices[pair] = round(price, 5)

            except Exception as e:
                print(f"❌ Errore parsing {pair}: {e}")
                prices[pair] = None

        return prices

    except Exception as e:
        print(f"❌ Errore download batch: {e}")
        return {pair: None for pair in YF_TICKERS}


def get_price(pair):
    return price, "LIVE" or "CACHE"
    """
    Restituisce il prezzo usando cache + batch download
    """
    global _price_cache

    # se cache vuota → scarica tutto
    if not _price_cache:
        print("🔄 Download prezzi (batch)...")
        _price_cache = _download_all_prices()

    price = _price_cache.get(pair)

    if price is None:
        print(f"⚠️ Prezzo non disponibile per {pair}")

    return price


def clear_price_cache():
    """
    Permette di forzare refresh manuale
    """
    global _price_cache
    _price_cache = {}

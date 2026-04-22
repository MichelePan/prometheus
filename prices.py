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
_last_valid_cache = {}  # fallback ultimi valori buoni


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

                # Controlli robusti
                if data is None or data.empty or "Close" not in data:
                    print(f"⚠️ Dato mancante: {pair}")
                    prices[pair] = None
                    continue

                price = float(data["Close"].iloc[-1])
                price = round(price, 5)

                prices[pair] = price

            except Exception as e:
                print(f"❌ Errore parsing {pair}: {e}")
                prices[pair] = None

        return prices

    except Exception as e:
        print(f"❌ Errore download batch: {e}")
        return {pair: None for pair in YF_TICKERS}


def get_price(pair):
    """
    Ritorna (price, source)
    source = "LIVE" o "CACHE"
    """
    global _price_cache, _last_valid_cache

    source = "CACHE"

    # Se cache vuota → prova download
    if not _price_cache:
        print("🔄 Download prezzi (batch)...")
        new_prices = _download_all_prices()

        if any(v is not None for v in new_prices.values()):
            _price_cache = new_prices
            source = "LIVE"

            # aggiorna fallback
            for k, v in new_prices.items():
                if v is not None:
                    _last_valid_cache[k] = v
        else:
            print("⚠️ Download fallito → uso fallback")

    price = _price_cache.get(pair)

    # fallback se None
    if price is None:
        price = _last_valid_cache.get(pair)

        if price is not None:
            print(f"↩️ Fallback usato per {pair}: {price}")
            source = "CACHE"
        else:
            print(f"❌ Nessun dato disponibile per {pair}")

    return price, source


def clear_price_cache():
    """
    Reset cache per forzare refresh LIVE
    """
    global _price_cache
    _price_cache = {}

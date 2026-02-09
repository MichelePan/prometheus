def calc_pips(pair, entry, current):
    if entry is None or current is None:
        return None

    if pair.endswith("JPY"):
        return round((current - entry) * 100, 1)
    else:
        return round((current - entry) * 10000, 1)

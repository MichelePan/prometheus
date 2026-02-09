def calc_pips(pair, entry, current):
    if current is None:
        return None

    if "JPY" in pair:
        return round((current - entry) * 100, 1)

    return round((current - entry) * 10000, 1)

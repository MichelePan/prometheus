def calc_pips(direction, entry, current):
    if entry is None or current is None:
        return None

    if direction == "SELL":
        return round((entry - current) * 10000, 1)

    if direction == "BUY":
        return round((current - entry) * 10000, 1)

    return None

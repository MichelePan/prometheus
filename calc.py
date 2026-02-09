def calc_pips(pair, entry, current):
    if current is None:
        return None
    mult = 100 if "JPY" in pair else 10000
    return round((current - entry) * mult, 1)

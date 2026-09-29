import pandas as pd

def soda_chips_rule(baskets: pd.DataFrame) -> dict:
    n = len(baskets)
    soda = baskets["items"].str.contains("SODA_BRAND")
    chips = baskets["items"].str.contains("CHIPS")
    both = soda & chips
    support = both.sum() / n
    conf = both.sum() / soda.sum() if soda.sum() else 0
    p_chips = chips.sum() / n
    lift = conf / p_chips if p_chips else 0
    return {"rule": "SODA_BRAND -> CHIPS", "support": round(support, 2), "confidence": round(conf, 2), "lift": round(lift, 2)}

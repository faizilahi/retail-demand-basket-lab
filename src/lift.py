import pandas as pd

def promo_lift(df: pd.DataFrame, sku: str) -> dict:
    base = df[(df.sku == sku) & (~df.promo)]["units"].sum()
    promo = df[(df.sku == sku) & (df.promo)]["units"].sum()
    # compare equal number of weeks: use mean*2
    base_w = df[(df.sku == sku) & (~df.promo)]["units"].mean() * 2
    promo_w = df[(df.sku == sku) & (df.promo)]["units"].sum()
    return {"baseline_units": int(base_w), "promo_units": int(promo_w), "lift_units": int(promo_w - base_w)}

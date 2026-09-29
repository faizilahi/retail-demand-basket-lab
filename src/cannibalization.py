import pandas as pd

def cannibalization(df, promo_sku, victim_sku):
    base_v = df[(df.sku == victim_sku) & (~df.promo_week)]["units"].mean() * 2 if False else None
    # mark promo weeks from promo sku
    promo_weeks = set(df.loc[df.sku == promo_sku].loc[df.promo, "week"])
    v = df[df.sku == victim_sku].copy()
    base = v[~v.week.isin(promo_weeks)]["units"].mean() * len(promo_weeks)
    promo = v[v.week.isin(promo_weeks)]["units"].sum()
    decline = base - promo
    return {"victim": victim_sku, "decline_units": int(round(decline)), "base_units": int(round(base)), "promo_period_units": int(promo)}

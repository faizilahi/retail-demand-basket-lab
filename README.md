# Promo That Looked Like Demand

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

A 2-week soda promo lifted units **+38%**, but **61%** of the lift was
cannibalized from adjacent private-label SKUs. Basket rules still showed soda↔chips
affinity — useful for ends, not for demand planning.

## The lift

Promo SKU units baseline **40,000** → promo **55,200** (lift **15,200**).

## The cannibalization

Adjacent SKU decline **9,272** units → net new demand **5,928** (**39%** of lift).

## The basket rule

`SODA_BRAND -> CHIPS` support 0.42, confidence 0.42, lift 1.00 — kept for merchandising,
excluded from replenishment forecasts.

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_basket.py
```

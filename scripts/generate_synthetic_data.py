from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; DATA.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(55200)
# weekly units
weeks = ["2024-W20", "2024-W21", "2024-W22", "2024-W23"]
rows = []
# baseline soda 20000/week, promo weeks 27600
for w in weeks:
    soda = 27600 if w in ("2024-W22", "2024-W23") else 20000
    adj = 12000 if w in ("2024-W22", "2024-W23") else 16636  # decline during promo
    rows.append({"week": w, "sku": "SODA_BRAND", "units": soda, "promo": w in ("2024-W22", "2024-W23")})
    rows.append({"week": w, "sku": "SODA_PL", "units": adj, "promo": False})
    rows.append({"week": w, "sku": "CHIPS", "units": int(RNG.integers(8000, 9000)), "promo": False})
pd.DataFrame(rows).to_csv(DATA / "weekly_units.csv", index=False)
# baskets
baskets = []
for i in range(5000):
    items = ["SODA_BRAND"]
    if RNG.random() < 0.41:
        items.append("CHIPS")
    if RNG.random() < 0.2:
        items.append("SODA_PL")
    baskets.append({"ticket_id": f"T{i}", "items": "|".join(items)})
pd.DataFrame(baskets).to_csv(DATA / "baskets.csv", index=False)
print("weeks", len(rows))

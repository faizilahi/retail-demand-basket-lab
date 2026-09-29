import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lift import promo_lift
from cannibalization import cannibalization
from basket_rules import soda_chips_rule
DATA, OUT = ROOT / "data", ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    weekly = pd.read_csv(DATA / "weekly_units.csv")
    baskets = pd.read_csv(DATA / "baskets.csv")
    lift = promo_lift(weekly, "SODA_BRAND")
    cann = cannibalization(weekly, "SODA_BRAND", "SODA_PL")
    rule = soda_chips_rule(baskets)
    net = lift["lift_units"] - cann["decline_units"]
    summary = {**lift, **cann, **rule, "net_new_demand": net,
               "pct_lift_cannibalized": round(cann["decline_units"] / lift["lift_units"], 2)}
    pd.DataFrame([summary]).to_csv(OUT / "promo_basket_summary.csv", index=False)
    print(json.dumps(summary, indent=2))
if __name__ == "__main__":
    main()

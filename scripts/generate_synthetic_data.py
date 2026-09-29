"""Synthetic POS transactions for demand and basket analysis."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(11)

SKUS = [
    ("SKU01", "Milk 1L", "Dairy", 3.49),
    ("SKU02", "Bread", "Bakery", 2.99),
    ("SKU03", "Eggs 12pk", "Dairy", 4.29),
    ("SKU04", "Coffee", "Beverage", 8.99),
    ("SKU05", "Butter", "Dairy", 5.49),
    ("SKU06", "Bananas", "Produce", 1.99),
    ("SKU07", "Cereal", "Grocery", 4.99),
    ("SKU08", "Orange Juice", "Beverage", 3.79),
    ("SKU09", "Yogurt", "Dairy", 1.29),
    ("SKU10", "Chips", "Snacks", 3.59),
]
BASKET_PATTERNS = [
    ["SKU01", "SKU02", "SKU03"],
    ["SKU04", "SKU05", "SKU07"],
    ["SKU06", "SKU08"],
    ["SKU01", "SKU05", "SKU09"],
]


def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    stores = pd.DataFrame(
        {
            "store_id": [f"ST{i:03d}" for i in range(1, 11)],
            "region": RNG.choice(["North", "South", "East", "West"], 10),
        }
    )
    sku_df = pd.DataFrame(SKUS, columns=["sku_id", "sku_name", "category", "unit_price"])

    rows = []
    txn_id = 1
    dates = pd.date_range("2024-01-01", "2024-09-30", freq="D")
    for d in dates:
        daily_txn = int(RNG.integers(40, 75))
        for _ in range(daily_txn):
            store = RNG.choice(stores["store_id"])
            basket = BASKET_PATTERNS[int(RNG.integers(0, len(BASKET_PATTERNS)))]
            if RNG.random() < 0.3:
                basket = list(basket) + [RNG.choice([s[0] for s in SKUS])]
            for sku in set(basket):
                price_row = sku_df.loc[sku_df["sku_id"] == sku].iloc[0]
                qty = int(RNG.integers(1, 4))
                rows.append(
                    {
                        "transaction_id": f"T{txn_id:07d}",
                        "txn_date": d,
                        "store_id": store,
                        "sku_id": sku,
                        "quantity": qty,
                        "line_revenue": round(qty * price_row["unit_price"], 2),
                    }
                )
            txn_id += 1

    stores.to_csv(out_dir / "dim_store.csv", index=False)
    sku_df.to_csv(out_dir / "dim_sku.csv", index=False)
    pd.DataFrame(rows).to_csv(out_dir / "fact_pos_line.csv", index=False)
    print(f"Retail synthetic POS data written to {out_dir}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    main(p.parse_args().out)

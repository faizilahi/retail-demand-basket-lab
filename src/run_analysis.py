"""Baseline demand forecast and market basket association rules."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from mlxtend.frequent_patterns import apriori, association_rules
    from mlxtend.preprocessing import TransactionEncoder

    HAS_MLXTEND = True
except ImportError:
    HAS_MLXTEND = False


def baseline_forecast(daily: pd.Series, horizon: int = 14) -> pd.DataFrame:
    """Simple moving average baseline for teaching."""
    window = 28
    last_ma = daily.tail(window).mean()
    last_date = daily.index.max()
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon)
    forecast = pd.DataFrame({"date": future_dates, "forecast_units": last_ma})
    return forecast


def basket_rules(transactions: pd.DataFrame) -> pd.DataFrame:
    baskets = transactions.groupby("transaction_id")["sku_id"].apply(list).tolist()
    if HAS_MLXTEND:
        te = TransactionEncoder()
        arr = te.fit(baskets).transform(baskets)
        df_ohe = pd.DataFrame(arr, columns=te.columns_)
        freq = apriori(df_ohe, min_support=0.02, use_colnames=True)
        if freq.empty:
            return pd.DataFrame(columns=["antecedents", "consequents", "lift"])
        rules = association_rules(freq, metric="lift", min_threshold=1.0)
        return rules.sort_values("lift", ascending=False).head(15)
    # Pure pandas fallback: pair co-occurrence lift approximation
    sku_sets = [set(b) for b in baskets]
    all_skus = sorted({s for b in sku_sets for s in b})
    n = len(sku_sets)
    counts = {s: sum(s in b for b in sku_sets) for s in all_skus}
    pair_rows = []
    for i, a in enumerate(all_skus):
        for b in all_skus[i + 1 :]:
            both = sum((a in s and b in s) for s in sku_sets)
            if both < 20:
                continue
            support_ab = both / n
            lift = support_ab / ((counts[a] / n) * (counts[b] / n))
            pair_rows.append({"antecedents": a, "consequents": b, "lift": lift, "support": support_ab})
    return pd.DataFrame(pair_rows).sort_values("lift", ascending=False).head(15)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data = root / "data"
    img = root / "docs" / "images"
    img.mkdir(parents=True, exist_ok=True)

    lines = pd.read_csv(data / "fact_pos_line.csv", parse_dates=["txn_date"])
    skus = pd.read_csv(data / "dim_sku.csv")

    daily = lines.groupby("txn_date")["quantity"].sum().sort_index()
    daily.to_csv(data / "daily_units_series.csv")
    forecast = baseline_forecast(daily)
    forecast.to_csv(data / "demand_forecast_baseline.csv", index=False)

    plt.figure(figsize=(10, 5))
    plt.plot(daily.index, daily.values, label="Actual daily units", color="#3366CC", alpha=0.7)
    plt.plot(forecast["date"], forecast["forecast_units"], label="28-day MA baseline", color="#DC3912", linestyle="--")
    plt.title("Demand Forecast Baseline (Synthetic POS)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(img / "demand_forecast.png", dpi=120)
    plt.close()

    by_cat = lines.merge(skus, on="sku_id").groupby("category")["line_revenue"].sum().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    plt.bar(by_cat.index, by_cat.values, color="#FF9900")
    plt.title("Revenue by Category (Synthetic)")
    plt.ylabel("USD")
    plt.tight_layout()
    plt.savefig(img / "revenue_by_category.png", dpi=120)
    plt.close()

    rules = basket_rules(lines[["transaction_id", "sku_id"]])
    rules.to_csv(data / "association_rules_top.csv", index=False)

    if not rules.empty and "lift" in rules.columns:
        plot_df = rules.head(8).copy()
        labels = plot_df.apply(
            lambda r: f"{r.get('antecedents', '')} -> {r.get('consequents', '')}", axis=1
        )
        plt.figure(figsize=(9, 5))
        plt.barh(range(len(plot_df)), plot_df["lift"], color="#109618")
        plt.yticks(range(len(plot_df)), labels)
        plt.gca().invert_yaxis()
        plt.xlabel("Lift")
        plt.title("Top Association Rules (Synthetic)")
        plt.tight_layout()
        plt.savefig(img / "basket_association_rules.png", dpi=120)
        plt.close()

    print(f"mlxtend={'yes' if HAS_MLXTEND else 'no (pandas fallback)'}")
    print("Retail analysis complete.")


if __name__ == "__main__":
    main()

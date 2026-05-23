"""CSV append + price-history analytics.

The store is a single CSV. Each scrape appends one row per product, never
overwrites. That preserves a true time series so we can compute trends,
detect drops, and chart history without a database.

For 12 products scraped daily, a 10-year history is roughly 44,000 rows -
well within what pandas handles instantly on any laptop.
"""

from __future__ import annotations

import csv
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

from .scraper import Product

CSV_COLUMNS = ["timestamp", "target", "name", "price", "url", "in_stock", "source_url"]


def append(csv_path: str | Path, products: list[Product]) -> int:
    if not products:
        return 0
    path = Path(csv_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        if write_header:
            writer.writeheader()
        for product in products:
            row = asdict(product)
            writer.writerow({k: row.get(k) for k in CSV_COLUMNS})
    return len(products)


def load_history(csv_path: str | Path) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        return pd.DataFrame(columns=CSV_COLUMNS)
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    return df


def detect_price_drops(
    csv_path: str | Path,
    new_products: list[Product],
    drop_threshold: float = 0.9,
    lookback_days: int = 14,
) -> list[dict]:
    """Compare each new price to the product's max over the lookback window.

    Returns alert dicts for products where the new price is at or below
    `drop_threshold * recent_max`. A threshold of 0.9 alerts on 10%+ drops.
    """
    if not new_products:
        return []
    df = load_history(csv_path)
    if df.empty:
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    recent = df[df["timestamp"] >= cutoff]
    alerts: list[dict] = []
    for product in new_products:
        if product.price is None:
            continue
        prior = recent[
            (recent["target"] == product.target)
            & (recent["name"] == product.name)
            & (recent["timestamp"] < pd.Timestamp(product.timestamp))
        ]
        if prior.empty:
            continue
        prior_max = float(prior["price"].max())
        if pd.isna(prior_max) or prior_max <= 0:
            continue
        if product.price <= drop_threshold * prior_max:
            drop_pct = (1 - (product.price / prior_max)) * 100
            alerts.append(
                {
                    "name": product.name,
                    "target": product.target,
                    "url": product.url,
                    "old_price": prior_max,
                    "new_price": product.price,
                    "drop_pct": round(drop_pct, 1),
                }
            )
    return alerts

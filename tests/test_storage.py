"""Smoke tests for storage layer: dedupe, append, and price-drop detection.

These do not hit the network and run in well under a second.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.scraper import Product
from src.storage import append, detect_price_drops, load_history


def _product(name: str, price: float, when: datetime, target: str = "test") -> Product:
    return Product(
        timestamp=when.isoformat(timespec="seconds"),
        target=target,
        name=name,
        price=price,
        url=f"https://example.com/p/{name.lower().replace(' ', '-')}",
        in_stock=True,
        source_url="https://example.com/category",
    )


def test_append_creates_csv_with_header(tmp_path: Path) -> None:
    csv_path = tmp_path / "prices.csv"
    written = append(csv_path, [_product("Pack A", 1990, datetime.now(timezone.utc))])
    assert written == 1
    text = csv_path.read_text(encoding="utf-8")
    assert "timestamp,target,name,price" in text.splitlines()[0]
    assert "Pack A" in text


def test_append_is_additive(tmp_path: Path) -> None:
    csv_path = tmp_path / "prices.csv"
    now = datetime.now(timezone.utc)
    append(csv_path, [_product("Pack A", 1990, now)])
    append(csv_path, [_product("Pack A", 1850, now + timedelta(days=1))])
    df = load_history(csv_path)
    assert len(df) == 2


def test_detect_price_drops_flags_significant_drop(tmp_path: Path) -> None:
    csv_path = tmp_path / "prices.csv"
    now = datetime.now(timezone.utc)
    # Seed history with a higher price 3 days ago
    append(csv_path, [_product("Pack A", 2500, now - timedelta(days=3))])
    # New scrape shows a 20% drop
    new = [_product("Pack A", 2000, now)]
    alerts = detect_price_drops(csv_path, new, drop_threshold=0.9, lookback_days=14)
    assert len(alerts) == 1
    assert alerts[0]["drop_pct"] == 20.0
    assert alerts[0]["old_price"] == 2500
    assert alerts[0]["new_price"] == 2000


def test_detect_price_drops_ignores_small_drop(tmp_path: Path) -> None:
    csv_path = tmp_path / "prices.csv"
    now = datetime.now(timezone.utc)
    append(csv_path, [_product("Pack B", 1000, now - timedelta(days=2))])
    new = [_product("Pack B", 970, now)]  # 3% drop, below threshold
    alerts = detect_price_drops(csv_path, new, drop_threshold=0.9)
    assert alerts == []


def test_detect_price_drops_ignores_new_products(tmp_path: Path) -> None:
    csv_path = tmp_path / "prices.csv"
    new = [_product("Brand new pack", 500, datetime.now(timezone.utc))]
    alerts = detect_price_drops(csv_path, new)
    assert alerts == []  # no prior data, cannot compare


def test_detect_price_drops_respects_lookback_window(tmp_path: Path) -> None:
    csv_path = tmp_path / "prices.csv"
    now = datetime.now(timezone.utc)
    # Old high price outside lookback window
    append(csv_path, [_product("Pack C", 3000, now - timedelta(days=30))])
    # Recent low baseline inside the window
    append(csv_path, [_product("Pack C", 1500, now - timedelta(days=2))])
    new = [_product("Pack C", 1400, now)]  # only 7% below recent
    alerts = detect_price_drops(csv_path, new, drop_threshold=0.9, lookback_days=14)
    assert alerts == []  # within lookback the new price is not a 10%+ drop

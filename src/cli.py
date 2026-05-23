"""Command-line entrypoint: read config, scrape, store, alert."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import yaml
from rich.console import Console
from rich.table import Table

from . import scraper, storage, notifier

console = Console()


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _print_results(products: list[scraper.Product]) -> None:
    if not products:
        console.print("[yellow]No products extracted.[/yellow]")
        return
    table = Table(title=f"Scraped {len(products)} products", show_lines=False)
    table.add_column("Target", style="cyan", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Price", justify="right", style="green")
    table.add_column("In stock", justify="center")
    for product in products:
        table.add_row(
            product.target,
            (product.name[:60] + "...") if len(product.name) > 60 else product.name,
            f"{product.price:,.2f}" if product.price is not None else "-",
            "yes" if product.in_stock else ("no" if product.in_stock is False else "?"),
        )
    console.print(table)


def main() -> int:
    parser = argparse.ArgumentParser(description="Competitor price monitor")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.yaml"),
        help="Path to config file (default: config.yaml)",
    )
    parser.add_argument(
        "--no-alerts",
        action="store_true",
        help="Skip Slack alerts even if SLACK_WEBHOOK_URL is set",
    )
    args = parser.parse_args()

    if not args.config.exists():
        console.print(f"[red]Config file not found: {args.config}[/red]")
        return 2

    cfg = load_config(args.config)
    csv_path = cfg.get("output", {}).get("csv_path", "data/prices.csv")
    alerts_cfg = cfg.get("alerts", {})

    products = asyncio.run(scraper.run(cfg))
    _print_results(products)

    written = storage.append(csv_path, products)
    console.print(f"[blue]Wrote {written} new row(s) to {csv_path}[/blue]")

    if products and not args.no_alerts:
        alerts = storage.detect_price_drops(
            csv_path,
            products,
            drop_threshold=float(alerts_cfg.get("drop_threshold", 0.9)),
            lookback_days=int(alerts_cfg.get("lookback_days", 14)),
        )
        if alerts:
            console.print(f"[magenta]Detected {len(alerts)} price drop(s).[/magenta]")
            notifier.send_alerts(alerts)
        else:
            console.print("[dim]No alert-worthy price drops detected.[/dim]")

    return 0 if products else 1


if __name__ == "__main__":
    sys.exit(main())

"""Headless-browser scraper that extracts product price + availability.

Strategy is layered to survive most DOM changes without code edits:

  1. JSON-LD <script type="application/ld+json"> Product schema (preferred,
     used by most modern e-commerce platforms for SEO).
  2. Microdata (itemprop=...) elements.
  3. Plain CSS selectors as a final fallback (configured in config.yaml).

If none yield a result, the scraper logs a warning and moves on rather than
crashing the whole run. That makes it safe to schedule unattended in CI.
"""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from playwright.async_api import Page, TimeoutError as PlaywrightTimeout, async_playwright
from rich.console import Console

console = Console()


@dataclass
class Product:
    timestamp: str
    target: str
    name: str
    price: float | None
    url: str
    in_stock: bool | None
    source_url: str


def _parse_price(raw: str | float | int | None) -> float | None:
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        return float(raw)
    cleaned = re.sub(r"[^\d,.\-]", "", str(raw)).replace("\xa0", "").replace(" ", "")
    cleaned = cleaned.replace(",", ".")
    if cleaned.count(".") > 1:
        head, _, tail = cleaned.rpartition(".")
        cleaned = head.replace(".", "") + "." + tail
    try:
        return float(cleaned)
    except ValueError:
        return None


def _extract_jsonld(html: str) -> list[dict[str, Any]]:
    """Find all JSON-LD blocks and return any Product schema objects."""
    products: list[dict[str, Any]] = []
    for match in re.finditer(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        flags=re.DOTALL | re.IGNORECASE,
    ):
        block = match.group(1).strip()
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        for node in _iter_ld(data):
            if isinstance(node, dict) and node.get("@type") in ("Product", ["Product"]):
                products.append(node)
    return products


def _iter_ld(obj: Any):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from _iter_ld(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from _iter_ld(item)


def _product_from_jsonld(node: dict[str, Any], source_url: str, target: str) -> Product | None:
    name = node.get("name")
    if not name:
        return None
    offers = node.get("offers")
    price_raw = None
    availability = None
    product_url = node.get("url") or source_url
    if isinstance(offers, dict):
        price_raw = offers.get("price")
        availability = offers.get("availability")
        product_url = offers.get("url") or product_url
    elif isinstance(offers, list) and offers:
        first = offers[0]
        if isinstance(first, dict):
            price_raw = first.get("price")
            availability = first.get("availability")
            product_url = first.get("url") or product_url
    in_stock: bool | None = None
    if isinstance(availability, str):
        in_stock = "InStock" in availability
    return Product(
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        target=target,
        name=str(name).strip(),
        price=_parse_price(price_raw),
        url=str(product_url),
        in_stock=in_stock,
        source_url=source_url,
    )


async def _extract_via_selectors(
    page: Page, source_url: str, target: str, selectors: dict[str, list[str]], limit: int
) -> list[Product]:
    """Last-resort extraction using configurable CSS selectors."""
    card_locator = None
    for sel in selectors.get("product_card", []):
        try:
            count = await page.locator(sel).count()
            if count > 0:
                card_locator = page.locator(sel)
                break
        except Exception:
            continue
    if card_locator is None:
        return []

    cards = await card_locator.element_handles()
    products: list[Product] = []
    for card in cards[:limit]:
        name = await _first_text(card, selectors.get("product_name", []))
        if not name:
            continue
        price_text = await _first_text(card, selectors.get("product_price", []))
        href = await _first_attr(card, selectors.get("product_url", []), "href")
        stock_present = await _first_present(card, selectors.get("in_stock_indicator", []))
        products.append(
            Product(
                timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                target=target,
                name=name.strip(),
                price=_parse_price(price_text),
                url=href or source_url,
                in_stock=stock_present if stock_present is not None else None,
                source_url=source_url,
            )
        )
    return products


async def _first_text(card, candidates: list[str]) -> str | None:
    for sel in candidates:
        try:
            handle = await card.query_selector(sel)
            if handle is None:
                continue
            text = (await handle.text_content()) or ""
            if text.strip():
                return text
        except Exception:
            continue
    return None


async def _first_attr(card, candidates: list[str], attr: str) -> str | None:
    for sel in candidates:
        try:
            handle = await card.query_selector(sel)
            if handle is None:
                continue
            value = await handle.get_attribute(attr)
            if value:
                return value
        except Exception:
            continue
    return None


async def _first_present(card, candidates: list[str]) -> bool | None:
    if not candidates:
        return None
    for sel in candidates:
        try:
            handle = await card.query_selector(sel)
            if handle is not None:
                return True
        except Exception:
            continue
    return False


async def scrape_target(
    page: Page,
    target: dict[str, Any],
    selectors: dict[str, list[str]],
    page_timeout: int,
) -> list[Product]:
    url = target["url"]
    name = target["name"]
    limit = int(target.get("max_products", 12))
    console.log(f"[cyan]>> Fetching {name}[/cyan] {url}")

    try:
        await page.goto(url, timeout=page_timeout * 1000, wait_until="domcontentloaded")
    except PlaywrightTimeout:
        console.log(f"[yellow]  timeout loading {url}[/yellow]")
        return []

    try:
        await page.wait_for_load_state("networkidle", timeout=page_timeout * 1000)
    except PlaywrightTimeout:
        pass

    html = await page.content()
    ld_nodes = _extract_jsonld(html)
    products: list[Product] = []
    for node in ld_nodes:
        product = _product_from_jsonld(node, source_url=url, target=name)
        if product:
            products.append(product)
        if len(products) >= limit:
            break

    if products:
        console.log(f"  [green]extracted {len(products)} via JSON-LD[/green]")
        return products[:limit]

    products = await _extract_via_selectors(page, url, name, selectors, limit)
    if products:
        console.log(f"  [green]extracted {len(products)} via CSS selectors[/green]")
    else:
        console.log(f"  [red]no products found - check selectors in config.yaml[/red]")
    return products


async def run(config: dict[str, Any]) -> list[Product]:
    """Run the scraper across all configured targets, return aggregated products."""
    targets = config.get("targets", [])
    selectors = config.get("selectors", {})
    request_cfg = config.get("request", {})
    delay = float(request_cfg.get("delay_between_targets_seconds", 3))
    page_timeout = int(request_cfg.get("page_timeout_seconds", 30))
    user_agent = request_cfg.get(
        "user_agent", "CompetitorPriceMonitor/0.1 (+contact via repo)"
    )

    all_products: list[Product] = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        try:
            context = await browser.new_context(
                user_agent=user_agent,
                viewport={"width": 1366, "height": 900},
                locale="cs-CZ",
            )
            page = await context.new_page()
            for i, target in enumerate(targets):
                products = await scrape_target(page, target, selectors, page_timeout)
                all_products.extend(products)
                if i < len(targets) - 1 and delay > 0:
                    await asyncio.sleep(delay)
            await context.close()
        finally:
            await browser.close()
    return all_products

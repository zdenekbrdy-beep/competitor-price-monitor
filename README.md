# Competitor Price Monitor

Headless-browser price tracker for e-commerce category pages. Runs daily on
GitHub Actions, appends each price to a CSV time series, and posts a Slack
alert when a tracked product drops more than 10% versus its rolling 14-day
maximum.

Built as a portable template. The default config points at
[books.toscrape.com](https://books.toscrape.com), a sandbox built specifically
for scraping practice, so the repo runs out of the box without depending on
any real merchant's terms of service. Swap in real e-commerce category URLs
in `config.yaml` to monitor live competitors.

---

## What's interesting about it

**Resilient extraction strategy.** The scraper tries JSON-LD Product schema
first, then microdata, then configurable CSS selectors. Most modern stores
(Shopify, BigCommerce, WooCommerce, Magento, Shoptet) publish JSON-LD for
SEO, so the JSON-LD path covers them automatically. The CSS fallbacks live
in [`config.yaml`](config.yaml) so a site redesign rarely needs a code change.
See [`src/scraper.py`](src/scraper.py).

**Selectors live in config, not code.** Add a new target or fix a broken
selector by editing [`config.yaml`](config.yaml). No Python edits required.

**True time series, no database.** Each scrape appends rows to one CSV. After
a year of daily scrapes that is roughly 4,400 rows; pandas reads it in
milliseconds. Trivial to back up, audit, or chart in Sheets.

**Tested before it ships.** [`tests/test_storage.py`](tests/test_storage.py)
exercises append, history, and price-drop detection against an in-memory CSV.
The full suite runs in under two seconds and gates the GitHub Actions job.

**Polite by default.** Configurable per-target delay, single browser context,
identifying User-Agent. Designed to be a good citizen, not a scrape bot.

---

## How it works

```
   +--------------------+
   | config.yaml        |  targets, selectors, thresholds
   +---------+----------+
             |
             v
   +--------------------+
   | scraper.py         |  Playwright + JSON-LD + CSS fallbacks
   +---------+----------+
             | list[Product]
             v
   +--------------------+
   | storage.append     |  -> data/prices.csv
   +---------+----------+
             | history + new prices
             v
   +--------------------+
   | storage.detect...  |  flag drops vs 14-day max
   +---------+----------+
             | alerts
             v
   +--------------------+
   | notifier.py        |  Slack incoming webhook
   +--------------------+
```

Each scrape produces rows of:

| timestamp                  | target          | name                       | price | url             | in_stock | source_url      |
| -------------------------- | --------------- | -------------------------- | ----: | --------------- | :------: | --------------- |
| 2026-05-23T06:30:12+00:00  | books_travel    | The Great Railway Bazaar   | 30.54 | https://...     |    1     | https://...     |

`price` is whatever currency the source uses. Mixing currencies across
targets is fine: each row keeps its source URL, so downstream code (or a
Sheets pivot) can group by target and treat each as its own series.

---

## Quick start

```bash
# 1. Clone and install
git clone https://github.com/zdenekbrdy-beep/competitor-price-monitor.git
cd competitor-price-monitor
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python -m playwright install chromium

# 2. (Optional) wire up Slack
cp .env.example .env
# Paste your Incoming Webhook URL into .env

# 3. Run once
python -m src.cli --config config.yaml

# 4. Run tests
pytest -q
```

The first run writes `data/prices.csv`. Each subsequent run appends.

---

## Configuration

Everything lives in [`config.yaml`](config.yaml):

```yaml
targets:
  - name: "books_travel"
    label: "books.toscrape.com - Travel"
    url: "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    max_products: 12

alerts:
  drop_threshold: 0.90    # alert when price <= 90% of recent max
  lookback_days: 14
```

To monitor a real competitor:

1. Find the category or listing page URL you want to watch.
2. Add an entry under `targets:` with a short `name`, human `label`, the URL,
   and how many products to capture.
3. Run once locally to verify. If extraction returns nothing, inspect the page
   source and add or override CSS selectors under `selectors:`. The scraper
   uses the first selector that returns results.
4. Commit. The next scheduled run picks it up automatically.

Most stores expose JSON-LD Product schema; on those, no selector tuning is
needed at all.

---

## Slack alerts

Create an Incoming Webhook in your workspace
([Slack docs](https://api.slack.com/messaging/webhooks)) and store it as:

* Local: `SLACK_WEBHOOK_URL` in `.env`
* GitHub Actions: repository secret named `SLACK_WEBHOOK_URL`

When the scraper detects a drop, it sends a single combined message like:

> :rotating_light: *Competitor price drops*
> - <https://...|The Great Railway Bazaar>  ·  35.40 -> **28.50**  ·  -19.5%  ·  _books_travel_

If the secret is not set, the scraper just skips the alert step. The CSV
still updates either way.

---

## Automated daily run

[`.github/workflows/daily-scrape.yml`](.github/workflows/daily-scrape.yml)
runs the scraper every morning at 06:30 UTC (07:30 CET / 08:30 CEST), commits
any price changes back to `data/prices.csv`, and posts Slack alerts if the
secret is configured.

Trigger it manually any time from the **Actions** tab -> *Daily price scrape*
-> *Run workflow*.

The committed CSV is the public history. Open the file in the repo to see
the actual recorded prices over time.

---

## Ethics and rate limiting

* Only scrapes **public** category and product pages. No login, no user data.
* Single Chromium context, configurable delay between targets.
* User-Agent identifies the bot and links back to this repo.
* If a target site's `robots.txt` or terms of service disallow scraping,
  remove it from `config.yaml`.

This tool is built for competitive intelligence on your **own** market: as a
shop owner watching public competitor pricing, or as a buyer tracking when a
product goes on sale. It is not built for content theft or for resale of the
scraped data.

---

## Extending it

A few directions the structure makes easy:

* Swap CSV for **Google Sheets** by replacing `storage.append` with a Sheets
  API call. Same `Product` dataclass, no other code changes.
* Add **Telegram or email** notifications by writing a sibling to
  `notifier.send_alerts`.
* Forecast price trends with a small **Prophet** or **statsmodels** module
  that reads `data/prices.csv` and writes a weekly chart.
* Add **per-product targets** (specific product URLs, not category pages)
  by introducing a second list of targets and a simpler extractor.

---

## License

MIT. See [`LICENSE`](LICENSE).

---

*Built by [Zdeněk Bradáč](https://www.upwork.com/freelancers/~0152451c5a66cd6d48)
as a portfolio piece. Hire me on Upwork for similar work: AI integrations,
workflow automation, data pipelines, scrapers.*

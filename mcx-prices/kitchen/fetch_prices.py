"""
🍳 fetch_prices.py = THE KITCHEN (the cook)

Its job, in plain English:
  1. Phone the supplier (TradingView) and ask for today's MCX prices.
  2. Check each price makes sense (the quality inspector).
  3. Pack everything into a fresh lunchbox: data/commodities.json.

The page (index.html + app.js) never changes. It just reads the newest lunchbox.
A robot on GitHub (see .github/workflows/update-mcx-prices.yml) runs this
cook every 30 minutes while MCX is open.

Note: the TradingView "scanner" address below is an unofficial, free source.
It's fine for learning, but it isn't a guaranteed service and can change.
"""

import json
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

# The supplier's address (the "API" the cook phones).
SUPPLIER_URL = "https://scanner.tradingview.com/futures/scan"

# The shopping list: what we want, and how to describe each one.
# "1!" means "the nearest-expiry contract" (the one most people trade).
SHOPPING_LIST = [
    {"name": "Gold",        "symbol": "GOLD",       "ticker": "MCX:GOLD1!",       "unit": "per 10 grams"},
    {"name": "Silver",      "symbol": "SILVER",     "ticker": "MCX:SILVER1!",     "unit": "per kg"},
    {"name": "Crude Oil",   "symbol": "CRUDEOIL",   "ticker": "MCX:CRUDEOIL1!",   "unit": "per barrel"},
    {"name": "Natural Gas", "symbol": "NATURALGAS", "ticker": "MCX:NATURALGAS1!", "unit": "per mmBtu"},
    {"name": "Copper",      "symbol": "COPPER",     "ticker": "MCX:COPPER1!",     "unit": "per kg"},
    {"name": "Zinc",        "symbol": "ZINC",       "ticker": "MCX:ZINC1!",       "unit": "per kg"},
]

# Where to put the finished lunchbox.
LUNCHBOX = Path(__file__).resolve().parent.parent / "data" / "commodities.json"


def phone_the_supplier():
    """Send our order (as JSON) and get the supplier's answer (also JSON)."""
    order = {
        "symbols": {"tickers": [item["ticker"] for item in SHOPPING_LIST]},
        "columns": ["close", "change", "change_abs", "high", "low"],
    }
    request = urllib.request.Request(
        SUPPLIER_URL,
        data=json.dumps(order).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "mcx-price-board"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        answer = json.loads(response.read().decode("utf-8"))

    # The answer looks like: {"data": [{"s": "MCX:GOLD1!", "d": [close, change, ...]}, ...]}
    return {row["s"]: row["d"] for row in answer.get("data", [])}


def quality_inspector(name, price, high, low):
    """Return True if the numbers make sense together, False if something's off."""
    if price is None or high is None or low is None:
        print(f"  ✗ {name}: missing numbers, skipping")
        return False
    if price <= 0:
        print(f"  ✗ {name}: price is zero or negative, skipping")
        return False
    if not (low <= price <= high):
        print(f"  ✗ {name}: price {price} is outside today's range {low}–{high}, skipping")
        return False
    return True


def cook():
    print("📞 Phoning the supplier…")
    prices = phone_the_supplier()

    fresh_items = []
    for item in SHOPPING_LIST:
        numbers = prices.get(item["ticker"])
        if not numbers:
            print(f"  ✗ {item['name']}: supplier had nothing, skipping")
            continue
        close, change_pct, change_abs, high, low = numbers
        if not quality_inspector(item["name"], close, high, low):
            continue
        fresh_items.append({
            "name": item["name"],
            "symbol": item["symbol"],
            "unit": item["unit"],
            "price": round(close, 2),
            "change": round(change_abs or 0, 2),
            "changePercent": round(change_pct or 0, 2),
            "high": round(high, 2),
            "low": round(low, 2),
        })
        print(f"  ✓ {item['name']}: ₹{close}")

    # If the supplier failed completely, keep yesterday's lunchbox instead of serving an empty one.
    if not fresh_items:
        raise SystemExit("Nothing fresh came back. Keeping the old lunchbox.")

    india_time = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    lunchbox = {
        "exchange": "MCX",
        "updated": india_time.strftime("%d %b %Y, %I:%M %p IST"),
        "source": "TradingView (MCX near-month futures), fetched automatically",
        "commodities": fresh_items,
    }
    LUNCHBOX.write_text(json.dumps(lunchbox, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"📦 Packed {len(fresh_items)} items into {LUNCHBOX.name}")


if __name__ == "__main__":
    cook()

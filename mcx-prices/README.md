# MCX Price Board – a learning project

A tiny web page that shows MCX commodity prices (Gold, Silver, Crude Oil, …).
It's built to show how the pieces of a software product fit together.

## The restaurant map

| File | Restaurant role | What it does |
|---|---|---|
| `data/commodities.json` | 🥫 Pantry / lunchbox | Holds the prices, each one labelled |
| `index.html` | 🏠 Dining room | The skeleton of the page: heading, search box, empty table |
| `app.js` | 🧑‍🍳 Waiter | Fetches the JSON and turns it into cards on the page |
| `style.css` | 🎨 Decorator | Colours, sizes, layout |
| `kitchen/fetch_prices.py` | 🍳 Kitchen (the cook) | Phones the supplier for live prices, checks them, refills the JSON |
| `../.github/workflows/update-mcx-prices.yml` | ⏰ Robot's alarm clock | Tells GitHub to run the cook every 30 min while MCX is open |

```
You open the page (index.html)
   → it calls the waiter (app.js)
      → the waiter fetches the lunchbox (commodities.json)
         → the waiter lays out one card per commodity
            → the decorator (style.css) makes it look nice
```

## Try changing something

Open `data/commodities.json`, change Gold's `"price"` to `999999`, and reload
the page. The card changes, and you didn't touch any code. That's the point of
keeping **data** separate from **code**.

## Running it

Browsers won't let a page read a file straight off your disk, so it needs a
tiny local web server. From this folder:

```
python3 -m http.server 8000
```

Then open http://localhost:8000

## How live prices work

```
⏰ Every 30 min (Mon–Fri, 9 AM – 11:30 PM IST) GitHub wakes a robot
   → the robot runs the cook (kitchen/fetch_prices.py)
      → the cook phones the supplier (TradingView) and gets JSON back
         → the quality inspector throws out numbers that don't make sense
            → the cook writes a fresh data/commodities.json and saves it
               → next time you open the page, the waiter serves the new prices
```

To cook on demand: GitHub → **Actions** tab → **Update MCX prices** → **Run workflow**.

The supplier address is an unofficial free TradingView endpoint: fine for
learning, but not guaranteed. The timer only runs once this is on the `main` branch.

## Next steps

1. Put the page online with **GitHub Pages**.
2. Add Elliott Wave labels to each commodity.

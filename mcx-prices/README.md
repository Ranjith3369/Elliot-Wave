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

## Next steps

1. Replace the hand-copied JSON with a **live data API** (a real kitchen).
2. Add a small **backend** that updates the prices automatically.
3. Add Elliott Wave labels to each commodity.

// 🧑‍🍳 app.js = THE WAITER
// Its job: go to the pantry (commodities.json), pick up the lunchbox,
// and lay each item out on the table (the page) so you can see it.

// Step 1 – Find the empty table and the search box on the page.
const board = document.getElementById("board");
const search = document.getElementById("search");
const updated = document.getElementById("updated");

let allCommodities = []; // the waiter's notepad: remembers what came from the pantry

// Step 2 – Walk to the pantry and fetch the lunchbox (the JSON file).
// The kitchen (kitchen/fetch_prices.py) refills this lunchbox automatically.
fetch("data/commodities.json", { cache: "no-store" }) // no-store = always get the freshest lunchbox
  .then((response) => response.json()) // open the lunchbox
  .then((data) => {
    allCommodities = data.commodities;
    updated.textContent = `${data.exchange} · prices as of ${data.updated}`;
    showCards(allCommodities); // Step 3 – serve it
  })
  .catch(() => {
    updated.textContent = "Could not reach the pantry (data file).";
  });

// Step 3 – Turn each item in the lunchbox into a card on the page.
function showCards(list) {
  board.innerHTML = ""; // clear the table first

  list.forEach((item) => {
    const isUp = item.change >= 0;
    const card = document.createElement("div");
    card.className = "card " + (isUp ? "up" : "down");
    card.innerHTML = `
      <h2>${item.name}</h2>
      <p class="price">₹${item.price.toLocaleString("en-IN")}</p>
      <p class="unit">${item.unit}</p>
      <p class="change">${isUp ? "▲" : "▼"} ${item.change.toLocaleString("en-IN")}
         (${item.changePercent}%)</p>
      <p class="range">Day range: ₹${item.low.toLocaleString("en-IN")} – ₹${item.high.toLocaleString("en-IN")}</p>
    `;
    board.appendChild(card);
  });

  if (list.length === 0) {
    board.innerHTML = "<p>No commodity matches that name.</p>";
  }
}

// Step 4 – Whenever you type in the search box, show only matching cards.
search.addEventListener("input", () => {
  const word = search.value.toLowerCase();
  const matches = allCommodities.filter((item) =>
    item.name.toLowerCase().includes(word)
  );
  showCards(matches);
});

import requests
import matplotlib.pyplot as plt
from datetime import datetime
import statistics

# === Step 1: Fetch 1-Year Bitcoin Price Data (Daily) ===
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    "vs_currency": "usd",
    "days": "365",  # Last 12 months
    "interval": "daily"
}

response = requests.get(url, params=params)
data = response.json()

# Check if 'prices' is in the response
if 'prices' not in data:
    raise KeyError("API response missing 'prices' field")

# === Step 2: Extract and Format Data ===
timestamps = [datetime.fromtimestamp(price[0] / 1000) for price in data["prices"]]
prices = [price[1] for price in data["prices"]]

# === Step 3: Insight 1 — Full 12-Month Price Trend ===
plt.figure(figsize=(10, 4))
plt.plot(timestamps, prices, color='navy', linewidth=2)
plt.title("Bitcoin Price - Last 12 Months")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.grid(True)
plt.tight_layout()
plt.savefig("insight_1_full_trend.png")
plt.clf()

# === Step 4: Insight 2 — Last 60 Days (Recent Trend) ===
plt.plot(timestamps[-60:], prices[-60:], color='darkred', linewidth=2)
plt.title("Bitcoin Price - Last 60 Days")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.grid(True)
plt.tight_layout()
plt.savefig("insight_2_recent_trend.png")
plt.clf()

# === Step 5: Insight 3 — Monthly Average Prices (Bar Chart) ===
from collections import defaultdict
monthly_prices = defaultdict(list)

for date, price in zip(timestamps, prices):
    key = date.strftime("%Y-%m")
    monthly_prices[key].append(price)

months = list(monthly_prices.keys())
monthly_avg = [sum(vals) / len(vals) for vals in monthly_prices.values()]

plt.bar(months, monthly_avg, color='seagreen')
plt.xticks(rotation=45, ha='right')
plt.title("Monthly Avg BTC Price (Last 12 Months)")
plt.ylabel("Avg Price (USD)")
plt.tight_layout()
plt.savefig("insight_3_monthly_avg.png")
plt.clf()

# === Step 6: Insight 4 — Highlight Dips Below 12-Month Average ===
average_price = statistics.mean(prices)
dip_dates = [t for t, p in zip(timestamps, prices) if p < average_price]
dip_prices = [p for p in prices if p < average_price]

plt.scatter(dip_dates, dip_prices, color='purple', label="Below Avg")
plt.axhline(average_price, color='gray', linestyle='--', label=f"12-Month Avg: ${average_price:.2f}")
plt.title("Dips Below Average Price")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("insight_4_price_dips.png")

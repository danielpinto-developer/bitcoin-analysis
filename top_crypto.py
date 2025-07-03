import requests
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Get data from CoinGecko API
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "sparkline": False
}
response = requests.get(url, params=params)
data = response.json()

# Step 2: Create DataFrame
df = pd.DataFrame(data)
df = df[["name", "current_price", "market_cap", "price_change_percentage_24h"]]

# Step 3: Sort top gainers
top_gainers = df.sort_values(by="price_change_percentage_24h", ascending=False).head(10)

# Step 4: Plot chart
plt.figure(figsize=(10, 6))
plt.barh(top_gainers['name'], top_gainers['price_change_percentage_24h'], color='green')
plt.xlabel("24h Price Change (%)")
plt.title("Top 10 Gaining Cryptos (24h)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("top_10_crypto_gainers.png")
plt.show()

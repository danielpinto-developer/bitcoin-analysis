import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ========== Config ==========
NUM_COINS = 3
DAYS = 90
DATE_TAG = datetime.now().strftime('%Y-%m-%d')
OUTPUT_DIR = f"charts_top_crypto{DATE_TAG}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== Helpers ==========
def get_top_coins(limit=10):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False
    }
    res = requests.get(url, params=params)
    return res.json()

def get_historical_data(coin_id, days=90):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    res = requests.get(url, params=params)

    if 'prices' not in res.json():
        print(f"⚠️ Skipping {coin_id} — no price data returned.")
        return pd.DataFrame()

    prices = res.json()['prices']
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('date', inplace=True)
    df.drop('timestamp', axis=1, inplace=True)
    return df

def plot_price_with_moving_avg(df, coin_id):
    df['MA7'] = df['price'].rolling(window=7).mean()
    df['MA30'] = df['price'].rolling(window=30).mean()
    plt.figure(figsize=(10, 5))
    plt.plot(df['price'], label='Price')
    plt.plot(df['MA7'], label='7D MA')
    plt.plot(df['MA30'], label='30D MA')
    plt.title(f"{coin_id.capitalize()} Price with 7D & 30D MA")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{coin_id}_price_ma.png")
    plt.close()

def plot_daily_returns(df, coin_id):
    df['returns'] = df['price'].pct_change()
    plt.figure(figsize=(10, 5))
    df['returns'].hist(bins=30, edgecolor='black')
    plt.title(f"{coin_id.capitalize()} Daily Return Distribution")
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{coin_id}_return_hist.png")
    plt.close()

def plot_cumulative_returns(df, coin_id):
    df['returns'] = df['price'].pct_change()
    df['cumulative'] = (1 + df['returns']).cumprod()
    plt.figure(figsize=(10, 5))
    plt.plot(df['cumulative'], label='Cumulative Return')
    plt.title(f"{coin_id.capitalize()} Cumulative Return (Last {DAYS} Days)")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{coin_id}_cumulative_return.png")
    plt.close()

def generate_insights(df, coin_id):
    ma7 = df['price'].rolling(window=7).mean().iloc[-1]
    ma30 = df['price'].rolling(window=30).mean().iloc[-1]
    price_now = df['price'].iloc[-1]
    returns = df['price'].pct_change().tail(30)
    volatility = returns.std() * 100
    trend = "uptrend" if ma7 > ma30 else "downtrend"
    return [
        f"{coin_id.capitalize()} is in a {trend} (7D MA: ${ma7:.2f}, 30D MA: ${ma30:.2f}).",
        f"Current price: ${price_now:.2f}. Volatility: {volatility:.2f}%.",
        f"30-day return: {((price_now / df['price'].iloc[-30]) - 1) * 100:.2f}%."
    ]

# ========== Main ==========
if __name__ == "__main__":
    top_coins = get_top_coins(limit=10)[:NUM_COINS]

    for coin in top_coins:
        coin_id = coin['id']
        coin_name = coin['name']
        print(f"\n🔍 Analyzing {coin_name}...")

        df = get_historical_data(coin_id, days=DAYS)
        if df.empty:
            continue

        plot_price_with_moving_avg(df.copy(), coin_id)
        plot_daily_returns(df.copy(), coin_id)
        plot_cumulative_returns(df.copy(), coin_id)

        insights = generate_insights(df.copy(), coin_id)
        for insight in insights:
            print("•", insight)

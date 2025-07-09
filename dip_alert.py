import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf
from tqdm import tqdm

CRYPTO_TICKERS = [
    "BTC-USD", "ETH-USD", "XRP-USD", "DOGE-USD", "SOL-USD",
    "ADA-USD", "DOT-USD", "AVAX-USD", "MATIC-USD", "LTC-USD",
    "TRX-USD", "UNI1-USD", "BCH-USD", "XLM-USD", "LINK-USD",
    "ATOM-USD", "ETC-USD", "FIL-USD", "HBAR-USD", "AAVE-USD",
    "SAND-USD", "EGLD-USD", "MKR-USD", "AR-USD", "NEAR-USD",
    "QNT-USD", "IMX-USD", "RUNE-USD", "ZEC-USD", "ICX-USD"
]
DAYS = 180
OUTPUT_DIR = "charts_dip_alert"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_data(ticker, days):
    try:
        df = yf.download(ticker, period=f"{days}d", interval="1d", progress=False)
        df = df[['Close']].dropna()
        return df
    except:
        return None

def calculate_dip_probabilities(df):
    df['Return'] = df['Close'].pct_change()
    df['Rolling_STD'] = df['Return'].rolling(window=7).std()
    dips = df['Return'] < -df['Rolling_STD']
    total = len(df)

    prob_30 = dips[-30:].mean() * 100 if total >= 30 else 0
    prob_90 = dips[-90:].mean() * 100 if total >= 90 else 0
    prob_180 = dips.mean() * 100

    return round(prob_30, 2), round(prob_90, 2), round(prob_180, 2)

def classify_signal(avg_prob):
    if avg_prob >= 23.5:
        return "🔴 LIKELY DIP"
    elif avg_prob >= 15:
        return "✅ POSSIBLE DIP"
    else:
        return "🟢 STABLE"

# Main
def run_dip_alert():
    results = []

    print("📊 Scanning dip signals across 30 coins...")

    for ticker in tqdm(CRYPTO_TICKERS[:30]):
        df = get_data(ticker, DAYS)
        if df is None or len(df) < 30:
            continue

        prob_30, prob_90, prob_180 = calculate_dip_probabilities(df)
        avg = round((prob_30 + prob_90 + prob_180) / 3, 2)
        signal = classify_signal(avg)

        results.append({
            "name": ticker.replace("-USD", ""),
            "ticker": ticker,
            "prob_30": prob_30,
            "prob_90": prob_90,
            "prob_180": prob_180,
            "avg": avg,
            "signal": signal
        })

    df_result = pd.DataFrame(results)
    df_result.sort_values(by="avg", ascending=False, inplace=True)
    df_result.to_csv(f"{OUTPUT_DIR}/dip_signals.csv", index=False)

    print("\n🔔 TOP 5 DIP SIGNALS TO WATCH:")
    for _, row in df_result.head(5).iterrows():
        print(f"- {row['name'].upper():15} | Dip: {row['avg']}% | Signal: {row['signal']}")

    top5 = df_result.head(5)
    plt.figure(figsize=(10, 6))
    for ticker in top5['ticker']:
        df = get_data(ticker, DAYS)
        df['Return'] = df['Close'].pct_change()
        df['Cumulative'] = (1 + df['Return']).cumprod()
        plt.plot(df['Cumulative'], label=ticker.replace("-USD", ''))

    plt.title("Top 5 Crypto Cumulative Returns (Last 180 Days)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/top5_cumulative_returns.png")
    plt.close()

if __name__ == "__main__":
    run_dip_alert()

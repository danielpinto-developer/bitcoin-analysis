import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# Output directory for charts
output_dir = "charts_bitcoin"
os.makedirs(output_dir, exist_ok=True)

# Download BTC data
btc = yf.download('BTC-USD', period='1y', auto_adjust=True)
btc = btc[['Close']].copy()
btc.reset_index(inplace=True)

# Add Moving Average and drop NA rows
btc['MA50'] = btc['Close'].rolling(window=50).mean()
btc.dropna(inplace=True)
btc.reset_index(drop=True, inplace=True)

# Ensure shape compatibility using .to_numpy().ravel()
close_series = pd.Series(btc['Close'].to_numpy().ravel(), index=btc.index)
ma_series = pd.Series(btc['MA50'].to_numpy().ravel(), index=btc.index)

# Dip logic
btc['Below_MA'] = close_series < ma_series
btc['Price_Change'] = close_series.pct_change().fillna(0) * 100
btc['Recent_Dip'] = btc['Below_MA'] & (btc['Price_Change'] < -1)

# Chart 1: Price + MA + Dips
plt.figure(figsize=(12, 6))
plt.plot(btc['Date'], btc['Close'], label='Bitcoin Price', linewidth=2)
plt.plot(btc['Date'], btc['MA50'], label='50-Day MA', linestyle='--')
plt.scatter(btc.loc[btc['Recent_Dip'], 'Date'],
            btc.loc[btc['Recent_Dip'], 'Close'],
            color='red', label='Dip Detected', zorder=5)
plt.title('Bitcoin Price + 50-Day MA + Dip Zones')
plt.xlabel('Date')
plt.ylabel('USD')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/bitcoin_price_ma_dips.png", dpi=300)
plt.close()

# Chart 2: Daily % Price Change
plt.figure(figsize=(12, 4))
plt.plot(btc['Date'], btc['Price_Change'], color='purple', label='Daily % Change')
plt.axhline(-1, color='red', linestyle='--', label='Dip Threshold')
plt.title('Bitcoin Daily % Price Change')
plt.xlabel('Date')
plt.ylabel('% Change')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/bitcoin_daily_change.png", dpi=300)
plt.close()

# Chart 3: Histogram
plt.figure(figsize=(8, 4))
btc['Price_Change'].hist(bins=50, color='skyblue', edgecolor='black')
plt.axvline(-1, color='red', linestyle='--', label='Dip Threshold')
plt.title('Distribution of Daily % Change')
plt.xlabel('% Change')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/bitcoin_change_histogram.png", dpi=300)
plt.close()

print("\n✅ Bitcoin analysis complete.")
print(f"📉 Dip days detected: {btc['Recent_Dip'].sum()}")
print(f"📁 Charts saved to: {os.path.abspath(output_dir)}")

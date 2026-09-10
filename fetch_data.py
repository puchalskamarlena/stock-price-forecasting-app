import yfinance as yf
import pandas as pd
import os

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "SPY"]
PERIOD = "2y"

os.makedirs("data", exist_ok=True)

all_data = []

for ticker in TICKERS:
    print(f"Fetching data for {ticker}...")
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=PERIOD)
        hist = hist.reset_index()
        hist["Ticker"] = ticker
        all_data.append(hist)
        print(f"  -> retrieved {len(hist)} rows")
    except Exception as e:
        print(f"  Error fetching {ticker}: {e}")

combined = pd.concat(all_data, ignore_index=True)
combined = combined[["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]]

output_path = "data/stock_data.csv"
combined.to_csv(output_path, index=False)

print(f"\nDone! Saved {len(combined)} rows to {output_path}")
print(f"Date range: {combined['Date'].min()} to {combined['Date'].max()}")
print(f"Tickers: {combined['Ticker'].unique().tolist()}")
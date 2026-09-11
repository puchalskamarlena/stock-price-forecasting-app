# Stock Price Analytics & Forecasting

An interactive web app for exploring historical stock price trends and generating short-term price forecasts, built with Streamlit and Facebook Prophet.

**Live app:** https://stock-price-forecasting-marlena.streamlit.app

## Overview

This project analyzes 2 years of historical price data for five major stocks/ETFs (AAPL, MSFT, GOOGL, AMZN, SPY) and builds a time-series forecasting model to project short-term price trends. Beyond building a working model, the project places strong emphasis on **honestly evaluating and communicating the model's limitations** rather than presenting forecasts as precise predictions.

## Features

- Automated data ingestion from the Yahoo Finance API (`yfinance`)
- Exploratory data analysis: price trends, normalized performance comparison, volatility analysis
- Time-series forecasting with Facebook Prophet, including confidence intervals
- Interactive Streamlit app: select any ticker and forecast horizon (7-90 days)
- Transparent reporting of model limitations directly in the app

## Key findings (EDA)

Over the 2-year period analyzed (Sep 2024 - Sep 2026):

| Ticker | Total return | Daily volatility (std) |
|--------|-------------|------------------------|
| GOOGL  | +124.0%     | 2.00%                   |
| AAPL   | +44.5%      | 1.82%                   |
| SPY    | +42.2%      | 1.04%                   |
| AMZN   | +40.6%      | 2.14%                   |
| MSFT   | +20.6%      | 1.82%                   |

SPY (the S&P 500 ETF), as expected, showed the lowest volatility of the group, reflecting the diversification benefit of tracking a broad market index rather than a single stock.

## Model performance and limitations

A Prophet model (weekly seasonality enabled, yearly seasonality disabled due to limited history) was trained on each ticker and evaluated on a 30-day held-out test period.

| Ticker | MAE    | MAPE  | Actual values within 95% confidence interval |
|--------|--------|-------|-----------------------------------------------|
| AAPL   | $20.99 | 6.72% | 1 / 30 (3.3%)                                  |
| GOOGL  | $30.95 | 9.05% | 7 / 30 (23.3%)                                 |

**Key limitation:** while the point forecast (MAPE ~7-9%) looks reasonably accurate at first glance, a deeper evaluation reveals the model's confidence intervals are too narrow and systematically biased — in both tickers tested, the vast majority of actual prices fell *below* the predicted range, indicating the model over-extrapolates recent upward trends and understates the likelihood of a slowdown or reversal. This finding held consistently across two different stocks, suggesting it's a structural limitation of trend-following forecasting rather than a one-off issue.

This is reflected honestly in the app itself: forecasts are explicitly framed as an indication of possible direction, not a precise price prediction.

## Tech stack

Python, pandas, yfinance, Prophet, Streamlit, matplotlib

## Project structure

- app.py                    # Streamlit app
- fetch_data.py              # Data ingestion script (yfinance)
- data/stock_data.csv        # Cached historical price data
- notebooks/
  - 01_eda.ipynb              # Exploratory data analysis
  - 02_forecasting.ipynb      # Model development and evaluation
- requirements.txt

## Running locally

```
git clone https://github.com/puchalskamarlena/stock-price-forecasting-app.git
cd stock-price-forecasting-app
pip install -r requirements.txt
streamlit run app.py
```

## Author

Marlena Puchalska-Zagula
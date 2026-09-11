import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Price Analytics & Forecasting", layout="wide")

st.title("Stock Price Analytics & Forecasting")

@st.cache_data
def load_data():
    df = pd.read_csv("data/stock_data.csv", parse_dates=["Date"])
    df["Date"] = pd.to_datetime(df["Date"], utc=True).dt.tz_localize(None)
    df =df.dropna().reset_index(drop=True)
    return df


df = load_data()

# Sidebar: ticker selector
st.sidebar.header("Settings")
tickers = sorted(df["Ticker"].unique())
selected_ticker = st.sidebar.selectbox("Select a stock ticker", tickers)

# Filter data for the selected ticker
ticker_df = df[df["Ticker"] == selected_ticker].sort_values("Date").reset_index(drop=True)

# Historical price chart
st.subheader(f"{selected_ticker} - Historical Closing Price")
st.line_chart(ticker_df.set_index("Date")["Close"])

# Key stats
current_price = ticker_df["Close"].iloc[-1]
start_price = ticker_df["Close"].iloc[0]
period_return = (current_price / start_price -1) * 100
volatility = ticker_df["Close"].pct_change().std() * 100

col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${current_price:.2f}")
col2.metric("Period Return", f"{period_return:.1f}%")
col3.metric("Daily Volatility", f"{volatility:.2f}%")

# Sidebar: forecast horizon
st.sidebar.header("Forecast Settings")
forecast_days = st.sidebar.slider("Forecast horizon (days)", min_value=7, max_value=90, value=30)

st.subheader(f"{selected_ticker} - Price Forecast ({forecast_days} days)")

@st.cache_data
def generate_forecast(ticker, horizon):
    prophet_df = df[df["Ticker"] == ticker][["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})
    model = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=False)
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=horizon)
    forecast = model.predict(future)
    return forecast

with st.spinner("Generating forecast..."):
    forecast = generate_forecast(selected_ticker, forecast_days)

future_only = forecast[forecast["ds"] > ticker_df["Date"].max()]

fig,  ax = plt.subplots(figsize=(10,5))
ax.plot(ticker_df["Date"], ticker_df["Close"], label="Historical", color="steelblue")
ax.plot(future_only["ds"], future_only["yhat"], label="Forecast", color="orange")
ax.fill_between(
    future_only["ds"],
    future_only["yhat_lower"],
    future_only["yhat_upper"],
    color="orange",
    alpha=0.2,
    label="Confidence interval",
)
ax.set_xlabel("Date")
ax.set_ylabel("Price ($)")
ax.legend()
st.pyplot(fig)

st.warning(
    "Important limitation: backtesting (see the project's forecasting notebook) showed this model's point "
    "forecast tends to extrapolate the recent trend and its confidence interval can understate real price "
    "swings. Treat this forecast as an indication of possible direction, not a precise price prediction."
)


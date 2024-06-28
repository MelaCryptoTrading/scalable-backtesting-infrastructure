# scripts/index_fund.py
import yfinance as yf
import pandas as pd

def get_top_10_crypto():
    # Placeholder function to get the top 10 cryptocurrencies by market cap (excluding stablecoins)
    top_10 = ["BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "SOL-USD", "XRP-USD", "DOT-USD", "DOGE-USD", "LTC-USD", "LINK-USD"]
    return top_10

def fetch_data(tickers, start, end):
    data = yf.download(tickers, start=start, end=end)
    return data['Adj Close']

def rebalance_index(data):
    market_caps = data.iloc[-1] * data.pct_change().mean()  # Placeholder for actual market cap calculation
    weights = market_caps / market_caps.sum()
    return weights

def create_index_fund(start_date, end_date):
    tickers = get_top_10_crypto()
    data = fetch_data(tickers, start=start_date, end=end_date)
    weights = rebalance_index(data)
    index_fund = (data * weights).sum(axis=1)
    return index_fund, weights

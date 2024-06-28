# scripts/backtest.py
import pandas as pd
import numpy as np

def calculate_macd(data, short_window=12, long_window=26, signal=9):
    data['EMA12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['Signal_Line'] = data['MACD'].ewm(span=signal, adjust=False).mean()
    return data

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

def macd_strategy(data):
    data = calculate_macd(data)
    data['Signal'] = 0
    data.loc[data['MACD'] > data['Signal_Line'], 'Signal'] = 1
    data['Position'] = data['Signal'].diff()
    return data

def rsi_strategy(data, overbought=70, oversold=30):
    data = calculate_rsi(data)
    data['Signal'] = 0
    data.loc[data['RSI'] > overbought, 'Signal'] = -1
    data.loc[data['RSI'] < oversold, 'Signal'] = 1
    data['Position'] = data['Signal'].diff()
    return data

def calculate_metrics(data, initial_cash=10000):
    data['Portfolio'] = initial_cash + (data['Close'].pct_change() * data['Position'].shift(1)).cumsum()
    total_return = data['Portfolio'].iloc[-1] / initial_cash - 1
    sharpe_ratio = (data['Portfolio'].pct_change().mean() / data['Portfolio'].pct_change().std()) * np.sqrt(252)
    max_drawdown = ((data['Portfolio'] / data['Portfolio'].cummax()) - 1).min()
    num_trades = data['Position'].abs().sum()
    return {
        'total_return': total_return,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'num_trades': num_trades
    }

def select_best_strategy(data):
    strategies = [
        {'name': 'MACD', 'function': macd_strategy},
        {'name': 'RSI', 'function': rsi_strategy}
    ]
    results = []
    for strat in strategies:
        strategy_data = strat['function'](data.copy())
        metrics = calculate_metrics(strategy_data)
        metrics['strategy'] = strat['name']
        results.append(metrics)
    best_strategy = max(results, key=lambda x: (x['sharpe_ratio'], x['total_return'], -x['max_drawdown']))
    return best_strategy

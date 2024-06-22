# src/backtesting_module.py

import pandas as pd
import backtrader as bt
import matplotlib.pyplot as plt

class RSIStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('rsi_upper', 70),
        ('rsi_lower', 30),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)

    def next(self):
        if self.rsi < self.params.rsi_lower:
            self.buy()
        elif self.rsi > self.params.rsi_upper:
            self.sell()

    def notify_trade(self, trade):
        if trade.isclosed:
            dt = self.data.datetime.date()
            print(f'Trade Closed - Date: {dt}, PnL: {trade.pnl}')

class MACDStrategy(bt.Strategy):
    params = (
        ('macd1', 12),
        ('macd2', 26),
        ('signal', 9),
    )

    def __init__(self):
        self.macd = bt.indicators.MACD(
            self.data.close,
            period_me1=self.params.macd1,
            period_me2=self.params.macd2,
            period_signal=self.params.signal
        )

    def next(self):
        if self.macd > 0:
            self.buy()
        elif self.macd < 0:
            self.sell()

def run_backtest(data, strategy_class, strategy_params):
    cerebro = bt.Cerebro()

    # Add data feed
    data_feed = bt.feeds.PandasData(dataname=data, datetime='Date')
    cerebro.adddata(data_feed)

    # Add strategy
    cerebro.addstrategy(strategy_class, **strategy_params)

    # Set initial cash and commission
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.001)

    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')

    # Run the strategy
    strategies = cerebro.run()

    # Capture metrics
    final_value = cerebro.broker.getvalue()
    sharpe_ratio = strategies[0].analyzers.sharpe.get_analysis()['sharperatio']

    # Plotting equity curve and drawdown
    cerebro.plot(style='candlestick', iplot=False)
    plt.savefig(f'equity_curve_{strategy_class.__name__}.png')
    plt.close()

    cerebro.plot(style='line', iplot=False)
    plt.savefig(f'drawdown_{strategy_class.__name__}.png')
    plt.close()

    trades = []
    for strat in strategies:
        for trade in strat.trades:
            trades.append({
                'open_date': trade.data.datetime.date(),
                'open_price': trade.price,
                'close_date': trade.data.datetime.date(1),
                'close_price': trade.price,
                'pnl': trade.pnl,
                'status': 'Closed' if trade.isclosed else 'Open'
            })

    num_trades = len(trades)
    winning_trades = sum(1 for trade in trades if trade['pnl'] > 0)
    losing_trades = sum(1 for trade in trades if trade['pnl'] < 0)

    return {
        'Final Portfolio Value': final_value,
        'Number of Trades': num_trades,
        'Winning Trades': winning_trades,
        'Losing Trades': losing_trades,
        'Sharpe Ratio': sharpe_ratio,
        'Trades': trades
    }

def load_data(filepath):
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

import json
import pandas as pd
import backtrader as bt
import matplotlib.pyplot as plt
import sys

class RSIStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('rsi_upper', 70),
        ('rsi_lower', 30),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.trade_list = []

    def next(self):
        if not self.position:
            if self.rsi < self.params.rsi_lower:
                self.buy()
                self.trade_list.append({
                    'open_date': self.data.datetime.date(0),
                    'open_price': self.data.close[0],
                    'action': 'buy'
                })
            elif self.rsi > self.params.rsi_upper:
                self.sell()
                self.trade_list.append({
                    'open_date': self.data.datetime.date(0),
                    'open_price': self.data.close[0],
                    'action': 'sell'
                })

    def notify_trade(self, trade):
        if trade.isclosed:
            self.trade_list[-1].update({
                'close_date': self.data.datetime.date(0),
                'close_price': self.data.close[0],
                'pnl': trade.pnl,
                'status': 'Closed'
            })

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
        self.trade_list = []

    def next(self):
        if not self.position:
            if self.macd.macd > self.macd.signal:
                self.buy()
                self.trade_list.append({
                    'open_date': self.data.datetime.date(0),
                    'open_price': self.data.close[0],
                    'action': 'buy'
                })
            elif self.macd.macd < self.macd.signal:
                self.sell()
                self.trade_list.append({
                    'open_date': self.data.datetime.date(0),
                    'open_price': self.data.close[0],
                    'action': 'sell'
                })

    def notify_trade(self, trade):
        if trade.isclosed:
            self.trade_list[-1].update({
                'close_date': self.data.datetime.date(0),
                'close_price': self.data.close[0],
                'pnl': trade.pnl,
                'status': 'Closed'
            })

def run_backtest(data, strategy_class, strategy_params, strategy_name, plot=False):
    cerebro = bt.Cerebro()

    # Add data feed
    data_feed = bt.feeds.PandasData(dataname=data, datetime='Date')
    cerebro.adddata(data_feed)

    # If any parameter is a list, create multiple strategies for each combination
    param_combinations = []
    for param_tuple in zip(*strategy_params.values()):
        param_combinations.append(dict(zip(strategy_params.keys(), param_tuple)))

    # Add strategies for each parameter combination
    for params in param_combinations:
        cerebro.addstrategy(strategy_class, **params)

    # Set initial cash and commission
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.001)

    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')

    # Run the strategy
    strategies = cerebro.run()

    # Capture metrics for each strategy
    results = []
    for i, strat in enumerate(strategies):
        final_value = cerebro.broker.getvalue()
        sharpe_ratio = strat.analyzers.sharpe.get_analysis().get('sharperatio', None)

        trades = strat.trade_list

        num_trades = len(trades)
        winning_trades = sum(1 for trade in trades if trade.get('pnl', 0) > 0)
        losing_trades = sum(1 for trade in trades if trade.get('pnl', 0) < 0)

        results.append({
            'Final Portfolio Value': final_value,
            'Number of Trades': num_trades,
            'Winning Trades': winning_trades,
            'Losing Trades': losing_trades,
            'Sharpe Ratio': sharpe_ratio,
            'Trades': trades
        })

    if plot:
        # Plotting equity curve
        cerebro.plot(style='candlestick')

    return results

def load_data(filepath):
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def main():
    # Load configuration from JSON file
    config = load_config('configs/backtest_config.json')

    # Load data
    data = load_data('data/BTC-USD.csv')

    # Perform backtests based on configurations
    results = []
    for backtest_config in config['backtests']:
        indicator = backtest_config['indicator']
        params = backtest_config['params']
        start_date = backtest_config['date_range']['start_date']
        end_date = backtest_config['date_range']['end_date']

        # Filter data based on date range
        filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

        # Run backtest based on indicator and params
        if indicator == 'RSI':
            strategy_class = RSIStrategy
        elif indicator == 'MACD':
            strategy_class = MACDStrategy
        else:
            raise ValueError(f"Unsupported indicator: {indicator}")

        # Run backtest and store result
        result = run_backtest(filtered_data, strategy_class, params, RSIStrategy, plot=True)
        results.append(result)

        # Print results
        for i, res in enumerate(result):
            print(f"{backtest_config['name']} Backtest Results - Strategy {i + 1} ({indicator}):")
            print(f"Final Portfolio Value: {res['Final Portfolio Value']}")
            print(f"Number of Trades: {res['Number of Trades']}")
            print(f"Winning Trades: {res['Winning Trades']}")
            print(f"Losing Trades: {res['Losing Trades']}")
            print(f"Sharpe Ratio: {res['Sharpe Ratio']}")
            print("")

if __name__ == "__main__":
    main()

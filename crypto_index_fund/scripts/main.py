# scripts/main.py
import pandas as pd
import matplotlib.pyplot as plt
from backtest import select_best_strategy
from index_fund import create_index_fund
from portfolio import optimize_portfolio
import matplotlib.pyplot as plt


``


def plot_index_fund(index_fund):
    plt.figure(figsize=(10, 6))
    index_fund.plot(title='Index Fund Performance')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()

def plot_portfolio_performance(portfolio_weights, mean_returns, cov_matrix):
    num_portfolios = 10000
    results = np.zeros((4, num_portfolios))
    weights_record = []

    for i in range(num_portfolios):
        weights = np.random.random(len(mean_returns))
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return, sharpe_ratio = calculate_portfolio_performance(weights, mean_returns, cov_matrix)
        results[0,i] = portfolio_std_dev
        results[1,i] = portfolio_return
        results[2,i] = sharpe_ratio
        results[3,i] = np.sum(weights)

    plt.figure(figsize=(10, 6))
    plt.scatter(results[0,:], results[1,:], c=results[2,:], cmap='YlGnBu', marker='o')
    plt.title('Simulated Portfolio Optimization based on Efficient Frontier')
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.show()

    return results, weights_record

def main():
    # Load BTC-USD data
    data = pd.read_csv('../data/BTC-USD.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    
    # Backtesting
    best_strategy = select_best_strategy(data)
    print("Best Strategy:", best_strategy)

    # Create Index Fund
    start_date = '2022-01-01'
    end_date = '2023-01-01'
    index_fund, weights = create_index_fund(start_date, end_date)
    print("Index Fund Weights:", weights)
    
    # Plot Index Fund Performance
    plot_index_fund(index_fund)
    
    # Portfolio Optimization
    data = pd.DataFrame(index_fund, columns=['Index_Fund'])
    min_variance, max_sharpe = optimize_portfolio(data)
    mean_returns = data.pct_change().mean()
    cov_matrix = data.pct_change().cov()
    
    # Plot Portfolio Performance
    plot_portfolio_performance(min_variance.x, mean_returns, cov_matrix)
    plot_portfolio_performance(max_sharpe.x, mean_returns, cov_matrix)

    print("Minimum Variance Portfolio Weights:", min_variance.x)
    print("Maximum Sharpe Ratio Portfolio Weights:", max_sharpe.x)

if __name__ == "__main__":
    main()

def main():
    # Load BTC-USD data
    data = pd.read_csv('../data/BTC-USD.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    
    # Backtesting
    best_strategy = select_best_strategy(data)
    print("Best Strategy:", best_strategy)

    # Create Index Fund
    start_date = '2022-01-01'
    end_date = '2023-01-01'
    index_fund, weights = create_index_fund(start_date, end_date)
    print("Index Fund Weights:", weights)
    
    # Portfolio Optimization
    data = pd.DataFrame(index_fund, columns=['Index_Fund'])
    min_variance, max_sharpe = optimize_portfolio(data)
    print("Minimum Variance Portfolio Weights:", min_variance.x)
    print("Maximum Sharpe Ratio Portfolio Weights:", max_sharpe.x)

if __name__ == "__main__":
    main()

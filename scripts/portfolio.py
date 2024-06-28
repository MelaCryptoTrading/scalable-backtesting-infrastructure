# scripts/portfolio.py
import numpy as np
import pandas as pd
from scipy.optimize import minimize

def calculate_portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    sharpe_ratio = returns / std
    return std, returns, sharpe_ratio

def optimize_portfolio(data):
    mean_returns = data.pct_change().mean()
    cov_matrix = data.pct_change().cov()
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)

    def min_variance(weights, mean_returns, cov_matrix):
        return calculate_portfolio_performance(weights, mean_returns, cov_matrix)[0]

    def neg_sharpe_ratio(weights, mean_returns, cov_matrix):
        return -calculate_portfolio_performance(weights, mean_returns, cov_matrix)[2]

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    
    # Optimize for minimum variance
    result_min_variance = minimize(min_variance, num_assets*[1./num_assets,], args=args,
                                   method='SLSQP', bounds=bounds, constraints=constraints)
    
    # Optimize for maximum Sharpe ratio
    result_max_sharpe = minimize(neg_sharpe_ratio, num_assets*[1./num_assets,], args=args,
                                 method='SLSQP', bounds=bounds, constraints=constraints)

    return result_min_variance, result_max_sharpe

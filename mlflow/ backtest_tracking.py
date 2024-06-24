import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import numpy as np

def run_backtest(params):
    # Simulate generating a dataset
    X, y = make_regression(n_samples=1000, n_features=params["n_features"], noise=params["noise"])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train a model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Calculate performance metrics
    score = model.score(X_test, y_test)
    
    return model, score

def log_backtest(params, score):
    # Log parameters and metrics to MLflow
    with mlflow.start_run():
        mlflow.log_params(params)
        mlflow.log_metric("score", score)
        # Log the model
        mlflow.sklearn.log_model(model, "model")
        print(f"Logged backtest run with params: {params} and score: {score}")

# Define the list of parameter sets for multiple backtests
backtest_params_list = [
    {"n_features": 10, "noise": 0.1},
    {"n_features": 20, "noise": 0.2},
    {"n_features": 30, "noise": 0.3},
]

# Run and log multiple backtest runs
for params in backtest_params_list:
    model, score = run_backtest(params)
    log_backtest(params, score)

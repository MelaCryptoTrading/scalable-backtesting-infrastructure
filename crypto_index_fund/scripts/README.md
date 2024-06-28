# Crypto Index Fund

## Setup

1. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

2. Ensure the BTC-USD data file is in the `data/` directory.

## Running the Project

1. Navigate to the `scripts` directory:
    ```bash
    cd scripts
    ```

2. Run the main script:
    ```bash
    python main.py
    ```

## Project Structure

- `data/`: Contains the BTC-USD data file.
- `scripts/`: Contains the Python scripts for backtesting, index fund creation, and portfolio optimization.
- `requirements.txt`: Lists the required Python libraries.

## Components

1. **Backtesting Algorithm:**
   - Selects the best strategy based on metrics like total return, Sharpe ratio, and max drawdown.

2. **Index Fund Creation:**
   - Creates an index of the 10 biggest cryptocurrencies by market capitalization.
   - Rebalances the index fund monthly based on updated market caps.

3. **Portfolio Optimization:**
   - Uses Modern Portfolio Theory to find the optimal composition for the lowest risk and highest Sharpe ratio.

from flask import Flask, request, jsonify
from config import Config
from extensions import db
from models import Userss, BTCData
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import numpy as np
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
#CORS(app)  # Enable CORS for the entire application
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Create the database connection string
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if Userss.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409

    new_user = Userss(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = Userss.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

def calculate_indicators(df):
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    return df

def generate_signals(df):
    df['SMA_Signal'] = 0
    df.loc[df['close'] > df['SMA_20'], 'SMA_Signal'] = 1
    df.loc[df['close'] < df['SMA_20'], 'SMA_Signal'] = -1
    df['MACD_Signal'] = 0
    df.loc[df['MACD'] > df['Signal_Line'], 'MACD_Signal'] = 1
    df.loc[df['MACD'] < df['Signal_Line'], 'MACD_Signal'] = -1
    df['Signal'] = df['SMA_Signal'] + df['MACD_Signal']
    return df

def backtest(start_date_str, end_date_str, initial_capital):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    #df = pd.read_sql_query(f"SELECT * FROM btc_data WHERE date BETWEEN '{start_date}' AND '{end_date}'", engine)
    #df['Date'] = pd.to_datetime(df['date'])
    # Construct the SQL query with parameters
    sql_query = f"SELECT * FROM btc_data WHERE date BETWEEN '{start_date}' AND '{end_date}'"
    
    # Execute the query using SQLAlchemy's engine
    result = engine.execute(sql_query)
    
    # Fetch all rows from the result set into a list of dictionaries
    rows = result.fetchall()
    
    # Close the result set (optional)
    result.close()
    
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(rows, columns=result.keys())
    
    # Convert 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])
        
    df = calculate_indicators(df)
    df = generate_signals(df)
    
    capital = initial_capital
    positions = 0
    df['Position'] = 0.0
    for i in range(len(df)):
        if df['Signal'].iloc[i] == 2 and positions == 0:  # Buy signal
            positions = capital / df['close'].iloc[i]
            capital = 0
        elif df['Signal'].iloc[i] == -2 and positions > 0:  # Sell signal
            capital = positions * df['close'].iloc[i]
            positions = 0
        #df.at[i, 'Position'] = positions if positions > 0 else capital
        # Explicitly cast to compatible dtype (float)
        df.loc[i, 'Position'] = float(positions) if positions > 0 else float(capital)

    final_portfolio_value = capital + positions * df['close'].iloc[-1]

    final_return = (final_portfolio_value - initial_capital) / initial_capital
    num_trades = sum(df['Position'] != 0)
    winning_trades = sum((df['Position'] > 0) & (df['close'] > df['open']))
    losing_trades = sum((df['Position'] < 0) & (df['close'] < df['open']))
    max_drawdown = df['close'].cummax().min() - df['close'].cummin().max()
    sharpe_ratio = (final_portfolio_value - initial_capital) / np.std(df['close']) * np.sqrt(252)

    return {
        'final_portfolio_value': final_portfolio_value,
        'final_return': final_return,
        'num_trades': num_trades,
        'winning_trades': winning_trades,
        'losing_trades': losing_trades,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio
    }

@app.route('/backtest', methods=['POST'])
def perform_backtest():
    data = request.json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    initial_capital = float(data.get('initial_capital'))
    
    results = backtest(start_date, end_date, initial_capital)
    return jsonify(results)

#index fund
def fetch_market_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
        'sparkline': 'false'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def exclude_stable_coins(data):
    stable_coins = ['tether', 'usd-coin', 'binance-usd', 'dai']
    filtered_data = [coin for coin in data if coin['id'] not in stable_coins]
    return filtered_data

def create_index(data):
    top_10 = data[:10]
    total_market_cap = sum(coin['market_cap'] for coin in top_10)
    index = [
        {
            'id': coin['id'],
            'name': coin['name'],
            'symbol': coin['symbol'],
            'market_cap': coin['market_cap'],
            'price': coin['current_price'],
            'weight': coin['market_cap'] / total_market_cap
        }
        for coin in top_10
    ]
    return index

@app.route('/index-fund', methods=['GET'])
def get_index_fund():
    market_data = fetch_market_data()
    filtered_data = exclude_stable_coins(market_data)
    index = create_index(filtered_data)
    return jsonify(index)

@app.route('/index-fund/recapitalize', methods=['POST'])
def recapitalize_index_fund():
    market_data = fetch_market_data()
    filtered_data = exclude_stable_coins(market_data)
    index = create_index(filtered_data)
    return jsonify(index)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

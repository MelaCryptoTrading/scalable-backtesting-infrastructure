from flask import Flask, request, jsonify
from config import Config
from extensions import db
from models import Userss, BTCData
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
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
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    return df

def generate_signals(df):
    df['SMA_Signal'] = 0
    df.loc[df['Close'] > df['SMA_20'], 'SMA_Signal'] = 1
    df.loc[df['Close'] < df['SMA_20'], 'SMA_Signal'] = -1
    df['MACD_Signal'] = 0
    df.loc[df['MACD'] > df['Signal_Line'], 'MACD_Signal'] = 1
    df.loc[df['MACD'] < df['Signal_Line'], 'MACD_Signal'] = -1
    df['Signal'] = df['SMA_Signal'] + df['MACD_Signal']
    return df

def backtest(start_date_str, end_date_str, initial_capital):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    df = pd.read_sql_query(f"SELECT * FROM btc_data WHERE Date BETWEEN '{start_date}' AND '{end_date}'", engine)
    
    df = calculate_indicators(df)
    df = generate_signals(df)
    
    capital = initial_capital
    positions = 0
    df['Position'] = 0
    for i in range(len(df)):
        if df['Signal'].iloc[i] == 2 and positions == 0:  # Buy signal
            positions = capital / df['Close'].iloc[i]
            capital = 0
        elif df['Signal'].iloc[i] == -2 and positions > 0:  # Sell signal
            capital = positions * df['Close'].iloc[i]
            positions = 0
        df['Position'].iloc[i] = positions if positions > 0 else capital

    final_portfolio_value = capital + positions * df['Close'].iloc[-1]

    final_return = (final_portfolio_value - initial_capital) / initial_capital
    num_trades = sum(df['Position']!= 0)
    winning_trades = sum((df['Position'] > 0) & (df['Close'] > df['Open']))
    losing_trades = sum((df['Position'] < 0) & (df['Close'] < df['Open']))
    max_drawdown = df['Close'].cummax().min() - df['Close'].cummin().max()
    sharpe_ratio = (final_portfolio_value - initial_capital) / np.std(df['Close']) * np.sqrt(252)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
# @app.route('/backtest', methods=['POST'])
# @jwt_required()
# def backtest1():
#     try:
#         print("Received backtest request")
#         data = request.get_json()
#         print("Request data:", data)
        
#         start_date = data['date_range']['start']
#         end_date = data['date_range']['end']
#         indicator = data['indicator']
#         params = data['params']

#         df = pd.read_sql('SELECT * FROM btc_data', engine)
#         df['Date'] = pd.to_datetime(df['date'])

#         df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

#         initial_capital = 100000
#         capital = initial_capital
#         positions = 0
#         df_filtered['Position'] = 0

#         print("Starting backtest loop")
#         for i in range(len(df_filtered)):
#             if df_filtered['Signal'].iloc[i] == 2 and positions == 0:  # Buy signal
#                 positions = capital / df_filtered['Close'].iloc[i]
#                 capital = 0
#             elif df_filtered['Signal'].iloc[i] == -2 and positions > 0:  # Sell signal
#                 capital = positions * df_filtered['Close'].iloc[i]
#                 positions = 0
#             df_filtered['Position'].iloc[i] = positions if positions > 0 else capital

#         final_portfolio_value = capital + positions * df_filtered['Close'].iloc[-1]
#         print(f'Final portfolio value: {final_portfolio_value}')

#         return jsonify({"message": "Backtesting completed", "final_portfolio_value": final_portfolio_value})
    
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return jsonify({"error": str(e)}), 500

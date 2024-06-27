from flask import Flask, request, jsonify
from config import Config
from extensions import db
from models import Userss, BTCData
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pandas as pd
from sqlalchemy import create_engine

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

@app.route('/backtest', methods=['POST'])
@jwt_required()
def backtest():
    try:
        print("Received backtest request")
        data = request.get_json()
        print("Request data:", data)
        
        start_date = data['date_range']['start']
        end_date = data['date_range']['end']
        indicator = data['indicator']
        params = data['params']

        df = pd.read_sql('SELECT * FROM btc_data', engine)
        df['Date'] = pd.to_datetime(df['date'])

        df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        initial_capital = 100000
        capital = initial_capital
        positions = 0
        df_filtered['Position'] = 0

        print("Starting backtest loop")
        for i in range(len(df_filtered)):
            if df_filtered['Signal'].iloc[i] == 2 and positions == 0:  # Buy signal
                positions = capital / df_filtered['Close'].iloc[i]
                capital = 0
            elif df_filtered['Signal'].iloc[i] == -2 and positions > 0:  # Sell signal
                capital = positions * df_filtered['Close'].iloc[i]
                positions = 0
            df_filtered['Position'].iloc[i] = positions if positions > 0 else capital

        final_portfolio_value = capital + positions * df_filtered['Close'].iloc[-1]
        print(f'Final portfolio value: {final_portfolio_value}')

        return jsonify({"message": "Backtesting completed", "final_portfolio_value": final_portfolio_value})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
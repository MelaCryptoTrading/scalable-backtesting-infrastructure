from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


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

def rebalance_index():
    market_data = fetch_market_data()
    filtered_data = exclude_stable_coins(market_data)
    new_index = create_index(filtered_data)
    return new_index

@app.route('/index-fund', methods=['GET'])
def get_index_fund():
    return jsonify(crypto_index)

@app.route('/index-fund/recapitalize', methods=['POST'])
def recapitalize_index_fund():
    global crypto_index
    crypto_index = rebalance_index()
    return jsonify(crypto_index)

if __name__ == '__main__':
    # Initial index creation
    market_data = fetch_market_data()
    filtered_data = exclude_stable_coins(market_data)
    crypto_index = create_index(filtered_data)

    # Start the Flask app
    app.run(debug=True)

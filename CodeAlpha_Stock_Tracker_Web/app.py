from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Hardcoded stock prices (internship requirement)
STOCK_PRICES = {
    "AAPL": 180.50,
    "TSLA": 250.00,
    "GOOGL": 140.20,
    "AMZN": 135.40,
    "MSFT": 330.10,
    "NVDA": 450.80
}

@app.route('/')
def index():
    if 'portfolio' not in session:
        session['portfolio'] = {}
    return render_template('index.html')

@app.route('/api/stocks')
def get_stocks():
    return jsonify(STOCK_PRICES)

@app.route('/api/portfolio')
def get_portfolio():
    if 'portfolio' not in session:
        session['portfolio'] = {}
        
    portfolio = session['portfolio']
    portfolio_data = []
    total_investment = 0.0
    
    for ticker, quantity in portfolio.items():
        price = STOCK_PRICES.get(ticker, 0)
        value = quantity * price
        total_investment += value
        
        portfolio_data.append({
            "ticker": ticker,
            "quantity": quantity,
            "price": price,
            "value": value
        })
        
    return jsonify({
        "holdings": portfolio_data,
        "total_investment": total_investment
    })

@app.route('/api/add', methods=['POST'])
def add_stock():
    if 'portfolio' not in session:
        session['portfolio'] = {}
        
    data = request.json
    ticker = data.get('ticker', '').upper()
    
    try:
        quantity = float(data.get('quantity', 0))
    except ValueError:
        return jsonify({"error": "Invalid quantity"}), 400
        
    if ticker not in STOCK_PRICES:
        return jsonify({"error": "Stock not found in database"}), 404
        
    if quantity <= 0:
        return jsonify({"error": "Quantity must be greater than zero"}), 400
        
    portfolio = session['portfolio']
    if ticker in portfolio:
        portfolio[ticker] += quantity
    else:
        portfolio[ticker] = quantity
        
    session.modified = True
    return get_portfolio()

@app.route('/api/remove', methods=['POST'])
def remove_stock():
    if 'portfolio' not in session:
        return get_portfolio()
        
    data = request.json
    ticker = data.get('ticker', '').upper()
    
    portfolio = session['portfolio']
    if ticker in portfolio:
        del portfolio[ticker]
        session.modified = True
        
    return get_portfolio()

@app.route('/api/reset', methods=['POST'])
def reset_portfolio():
    session['portfolio'] = {}
    session.modified = True
    return get_portfolio()

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Run on 5001 in case 5000 is still occupied

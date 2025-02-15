from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('new.html')

@app.route('/get_price', methods=['POST'])
def get_price():
    stock_symbol = request.form.get('stock_symbol')
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="1d")

    if not data.empty:
        latest_price = data['Close'].iloc[-1]
        return f"Latest Price of {stock_symbol}: ${latest_price:.2f}"
    else:
        return "Invalid stock symbol or no data available."

if __name__ == '__main__':
    app.run(debug=True)

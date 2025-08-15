# stocks.py
# Fetch stock market data from Yahoo Finance

import yfinance as yf

def get_stock_data(symbol: str):
    """
    Fetches latest market data for the given stock symbol.
    Uses Yahoo Finance (free API) to retrieve stock price, volume, and change.
    """
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1d")
    if hist.empty:
        return {"error": "Invalid symbol or no data"}
    
    latest = hist.iloc[-1]
    return {
        "price": round(latest["Close"], 2),
        "volume": int(latest["Volume"]),
        "open": round(latest["Open"], 2),
        "high": round(latest["High"], 2),
        "low": round(latest["Low"], 2)
    }

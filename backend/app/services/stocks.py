# app/services/stock_service.py
import yfinance as yf

def get_stock_data(symbol: str):
    """
    Fetches latest stock info for the given symbol using Yahoo Finance.
    """
    ticker = yf.Ticker(symbol)
    info = ticker.history(period="1d")

    if info.empty:
        return {"error": f"No data found for symbol {symbol}"}

    latest_row = info.tail(1).to_dict("records")[0]
    return {
        "symbol": symbol.upper(),
        "date": latest_row["Date"].strftime("%Y-%m-%d") if "Date" in latest_row else None,
        "open": latest_row["Open"],
        "high": latest_row["High"],
        "low": latest_row["Low"],
        "close": latest_row["Close"],
        "volume": latest_row["Volume"]
    }

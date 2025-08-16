# app/services/stock_service.py
import yfinance as yf

def get_stock_data(symbol: str, days: int = 7):
    """Get stock data with historical prices"""
    try:
        ticker = yf.Ticker(symbol)
        
        # Get current day data
        current = ticker.history(period="1d")
        if current.empty:
            return {"error": "No current data"}
            
        # Get historical data
        hist = ticker.history(period=f"{days}d")
        
        current_data = current.iloc[-1].to_dict()
        hist_data = {
            "start": hist.iloc[0].to_dict(),
            "end": hist.iloc[-1].to_dict()
        }
        
        change_pct = ((hist_data["end"]["Close"] - hist_data["start"]["Close"]) / 
                     hist_data["start"]["Close"]) * 100
        
        return {
            "symbol": symbol.upper(),
            "current": current_data,
            "change_pct": round(change_pct, 2),
            "history": hist_data
        }
    except Exception as e:
        return {"error": str(e)}
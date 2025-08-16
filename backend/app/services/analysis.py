# app/services/analysis.py

from typing import Dict
from app.services.stocks import get_stock_data
from app.services.sentiment import get_sentiment

def get_combined_analysis(symbol: str) -> Dict:
    try:
        symbol = symbol.upper()
        
        # 1) Get sentiment
        sentiment_res = get_sentiment(symbol)
        
        # 2) Get price data
        price_res = get_stock_data(symbol)
        
        # Calculate composite score
        sentiment_score = sentiment_res.get("average_sentiment", 0) * 10  # Scale to -10 to 10
        price_score = 0
        
        if "change_pct" in price_res:
            price_score = price_res["change_pct"] * 0.2  # Scale price impact
            
        composite_score = (sentiment_score + price_score) / 2
        
        # Determine verdict
        if composite_score > 2.5:
            verdict = "Strong Bullish"
        elif composite_score > 0.5:
            verdict = "Bullish"
        elif composite_score < -2.5:
            verdict = "Strong Bearish"
        elif composite_score < -0.5:
            verdict = "Bearish"
        else:
            verdict = "Neutral"
            
        return {
            "symbol": symbol,
            "sentiment": {
                "average": sentiment_res.get("average_sentiment"),
                "articles_analyzed": sentiment_res.get("articles_analyzed", 0),
            },
            "price": {
                "current": price_res.get("current", {}).get("Close"),
                "change_pct": price_res.get("change_pct"),
                "points": price_score,
            },
            "verdict": {
                "score": round(composite_score, 2),
                "label": verdict,
                "confidence": min(100, abs(composite_score) * 20)  # 0-100%
            }
        }
    except Exception as e:
        return {"error": str(e)}
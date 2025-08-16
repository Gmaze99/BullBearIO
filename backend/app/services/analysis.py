# app/services/analysis.py

from typing import Dict
from app.services.sentiment import get_sentiment

def get_combined_analysis(symbol: str) -> Dict:
    """
    Short-circuited analysis:
      - Fetch sentiment from Yahoo Finance
      - Skip candles for now
      - Always return a static verdict
    """
    symbol = symbol.upper()

    # 1) Sentiment
    sentiment_res = get_sentiment(symbol)
    avg_sentiment = sentiment_res.get("average_sentiment")
    articles = sentiment_res.get("articles_analyzed", 0)

    # 2) Static placeholder for price (skipped)
    change_pct = None
    start_close = None
    end_close = None

    # 3) Very simple verdict just based on sentiment
    if avg_sentiment is None:
        verdict = {"score": 0, "label": "Neutral"}
    elif avg_sentiment > 0.05:
        verdict = {"score": avg_sentiment, "label": "Bullish"}
    elif avg_sentiment < -0.05:
        verdict = {"score": avg_sentiment, "label": "Bearish"}
    else:
        verdict = {"score": avg_sentiment, "label": "Neutral"}

    return {
        "symbol": symbol,
        "sentiment": {
            "average": avg_sentiment,
            "articles_analyzed": articles,
        },
        "price": {
            "change_7d_pct": change_pct,
            "start_close": start_close,
            "end_close": end_close,
            "points": 0,
        },
        "verdict": verdict,
    }

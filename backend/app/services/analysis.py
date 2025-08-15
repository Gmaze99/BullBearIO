# app/services/analysis.py
import os
import time
import finnhub
from typing import Optional, Dict
from app.services.sentiment import get_sentiment

# Read Finnhub key once at import (fail fast if missing)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
if not FINNHUB_API_KEY:
    raise RuntimeError("FINNHUB_API_KEY not found. Set it in your environment or docker-compose.")

_client = finnhub.Client(api_key=FINNHUB_API_KEY)


def _get_price_change_pct(symbol: str, days: int = 7) -> Optional[Dict]:
    """
    Pulls last `days` daily candles and returns start/end close + % change.
    """
    now = int(time.time())              # current unix timestamp (seconds)
    frm = now - days * 24 * 3600        # N days ago
    candles = _client.stock_candles(symbol, "D", frm, now)

    # Finnhub returns {'s': 'ok', 'c': [...], 't': [...], ...} on success
    if not isinstance(candles, dict) or candles.get("s") != "ok":
        return None

    closes = candles.get("c") or []
    if len(closes) < 2:
        return None

    start = closes[0]
    end = closes[-1]
    change_pct = ((end - start) / start) * 100.0 if start else 0.0

    return {
        "start_close": start,
        "end_close": end,
        "change_pct": change_pct,
        "num_points": len(closes),
    }


def _classify(avg_sentiment: Optional[float], change_pct: Optional[float]) -> Dict:
    """
    Combine sentiment (-1..1) and price change (%) into a single score.
    Simple heuristic:
      score = (sentiment * 10) + (price_change_pct)
      > +1  -> Bullish
      < -1  -> Bearish
      else  -> Neutral
    """
    s = avg_sentiment if avg_sentiment is not None else 0.0
    p = change_pct     if change_pct is not None     else 0.0

    score = (s * 10.0) + p
    if score > 1.0:
        label = "Bullish"
    elif score < -1.0:
        label = "Bearish"
    else:
        label = "Neutral"

    return {"score": score, "label": label}


def get_combined_analysis(symbol: str) -> Dict:
    """
    Orchestrates:
      - Recent price trend from Finnhub candles
      - Average news sentiment from our sentiment service
      - Simple Bull/Bear/Neutral classification
    """
    symbol = symbol.upper()

    # 1) Sentiment (already implemented in services.sentiment)
    sentiment_res = get_sentiment(symbol)
    avg_sentiment = None
    articles = 0
    if isinstance(sentiment_res, dict) and "average_sentiment" in sentiment_res:
        avg_sentiment = sentiment_res["average_sentiment"]
        articles = sentiment_res.get("articles_analyzed", 0)

    # 2) Price change (last 7D)
    price_res = _get_price_change_pct(symbol, days=7)
    change_pct = price_res["change_pct"] if price_res else None

    # 3) Classification
    verdict = _classify(avg_sentiment, change_pct)

    return {
        "symbol": symbol,
        "sentiment": {
            "average": avg_sentiment,
            "articles_analyzed": articles,
        },
        "price": {
            "change_7d_pct": change_pct,
            "start_close": price_res["start_close"] if price_res else None,
            "end_close": price_res["end_close"] if price_res else None,
            "points": price_res["num_points"] if price_res else 0,
        },
        "verdict": verdict,  # {"score": float, "label": "Bullish|Bearish|Neutral"}
    }

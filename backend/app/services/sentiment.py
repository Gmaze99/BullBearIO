# sentiment.py
# Simple sentiment analysis using financial news headlines

import requests
from textblob import TextBlob

NEWS_API_KEY = "YOUR_NEWS_API_KEY"  # You can use NewsAPI.org free tier

def get_sentiment(symbol: str):
    """
    Fetches recent news headlines for the stock and calculates average sentiment score.
    Returns a score between -1 (bearish) and +1 (bullish).
    """
    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])
    
    if not articles:
        return {"error": "No news found"}
    
    sentiment_scores = []
    for article in articles[:5]:  # limit to top 5 headlines
        analysis = TextBlob(article["title"])
        sentiment_scores.append(analysis.sentiment.polarity)
    
    avg_sentiment = round(sum(sentiment_scores) / len(sentiment_scores), 2)
    return avg_sentiment

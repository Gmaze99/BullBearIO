import finnhub
import os
from datetime import datetime, timedelta
from textblob import TextBlob

# Load your API key (can also use dotenv)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "YOUR_FINNHUB_API_KEY")

# Setup Finnhub client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def get_sentiment(symbol: str):
    try:
        # Date range for last 7 days
        today = datetime.today().strftime('%Y-%m-%d')
        last_week = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

        # Fetch news from Finnhub
        news = finnhub_client.company_news(symbol, _from=last_week, to=today)

        if not news:
            return {"error": "No news found"}

        sentiment_scores = []

        for article in news:
            headline = article.get("headline", "")
            if headline:
                sentiment = TextBlob(headline).sentiment.polarity
                sentiment_scores.append(sentiment)

        if not sentiment_scores:
            return {"error": "No headlines to analyze"}

        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)

        return {
            "average_sentiment": avg_sentiment,
            "articles_analyzed": len(sentiment_scores)
        }

    except Exception as e:
        return {"error": str(e)}

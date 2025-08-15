# Import FastAPI framework
from fastapi import FastAPI
# CORS middleware allows cross-origin requests (frontend → backend)
from fastapi.middleware.cors import CORSMiddleware
from app.services.sentiment import get_sentiment
from app.services.stocks import get_stock_data  

# Create the FastAPI app instance with metadata
app = FastAPI(
    title="BullBearIO API",   # Shown in Swagger UI
    version="0.1.0"           # API version
)

# Add CORS middleware to allow frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all origins for now (change later for security)
    allow_credentials=True,       # Allow cookies/authorization headers
    allow_methods=["*"],           # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],           # Allow all headers
)

# Basic health check endpoint
# This is used to verify that the backend is up and running
@app.get("/api/health")
def health():
    """
    Returns the API status.
    Can be used by frontend or monitoring systems to check if the backend is alive.
    """
    return {"status": "ok"}  # JSON response

@app.get("/stock/{symbol}")
async def stock_endpoint(symbol: str):
    """
    Endpoint to fetch latest stock price and details.
    Example: GET /stock/AAPL
    """
    data = get_stock_data(symbol)
    return {"symbol": symbol, "data": data}

@app.get("/sentiment/{symbol}")
async def sentiment_endpoint(symbol: str):
    """
    Endpoint to fetch sentiment analysis of latest news headlines for the stock.
    Example: GET /sentiment/GOOGL
    """
    sentiment_score = get_sentiment(symbol)
    return {"symbol": symbol, "sentiment": sentiment_score}

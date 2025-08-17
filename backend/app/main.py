# Import FastAPI framework
from fastapi import FastAPI, HTTPException
# CORS middleware allows cross-origin requests (frontend → backend)
from fastapi.middleware.cors import CORSMiddleware
import os
from app.services.sentiment import get_sentiment
from app.services.stocks import get_stock_data
from app.services.analysis import get_combined_analysis

# Create the FastAPI app instance with metadata
app = FastAPI(
    title="BullBearIO API",   # Shown in Swagger UI
    version="0.1.0"           # API version
)

# Load allowed origins from environment variable
# Format: "http://localhost:3000,https://example.com"
# Defaults to empty list if not set (blocking all cross-origin requests)
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")  # Returns list of origins or empty list

# Configure CORS middleware with security best practices
app.add_middleware(
    CORSMiddleware,
    # List of allowed origins - NEVER use ["*"] in production
    allow_origins=origins,
    
    # Allow credentials/cookies (only enable if your frontend needs authentication)
    allow_credentials=True,  # Set to False if not using cookies/auth
    
    # Restrict to only necessary HTTP methods
    allow_methods=["GET"],   # Add "POST", "PUT" etc. only if needed
    
    # Only allow specific headers (Content-Type is commonly needed for JSON APIs)
    allow_headers=["Content-Type"],  # Add others like "Authorization" if needed
    
    # Security Note: For APIs that don't need CORS (same-origin only), 
    # consider completely disabling this middleware instead
)

# Basic health check endpoint
# This is used to verify that the backend is up and running
@app.get("/")
def root():
    """
    Root endpoint — provides basic API info.
    """
    return {
        "message": "Welcome to BullBearIO API 🚀",
        "docs_url": "/docs",
        "endpoints": ["/api/health", "/stock/{symbol}", "/sentiment/{symbol}"]
    }

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
    sentiment_score = get_sentiment(symbol.upper())
    return {"symbol": symbol.upper(), "sentiment": sentiment_score}

@app.get("/analysis/{symbol}")
async def analysis_endpoint(symbol: str):
    try:
        result = get_combined_analysis(symbol)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# Use official lightweight Python image
FROM python:3.11-slim

WORKDIR /backend

# Copy requirements file first (for better caching during builds)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV FINNHUB_API_KEY="your_api_key_here"
ENV PYTHONPATH="${PYTHONPATH}:/backend"

# Expose backend port (FastAPI default is 8000)
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

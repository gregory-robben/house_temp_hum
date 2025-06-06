# Multi-stage Dockerfile for Raspberry Pi deployment
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Adafruit DHT library for Pi
RUN pip install --no-cache-dir Adafruit-DHT

# Copy source code
COPY src/ ./src/
COPY .env* ./

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash sensor \
    && chown -R sensor:sensor /app

USER sensor

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.sensor import DHT22Sensor; s=DHT22Sensor(4); print('OK' if s.read() else 'FAIL')" || exit 1

CMD ["python", "-m", "src.main"]

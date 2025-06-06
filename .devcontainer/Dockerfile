FROM python:3.11-slim

# Install system dependencies for development
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash vscode \
    && usermod -aG sudo vscode

WORKDIR /workspace

# Copy requirements and install Python dependencies
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

USER vscode

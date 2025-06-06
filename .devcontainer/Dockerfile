FROM python:3.11-slim

# Install system dependencies for development
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Fix Python packaging tools
RUN pip install --upgrade pip wheel setuptools

# Create non-root user
RUN useradd --create-home --shell /bin/bash vscode \
    && usermod -aG sudo vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

WORKDIR /workspace

# Copy requirements and install Python dependencies
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

USER vscode

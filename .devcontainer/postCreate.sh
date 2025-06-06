#!/bin/bash

# Update pip and setuptools first
pip install --upgrade pip setuptools wheel

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

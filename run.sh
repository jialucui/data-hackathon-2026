#!/bin/bash

# A robust run script to handle broken Python environments
# Sometimes pre-existing virtual environments have hardcoded absolute paths that break when moved
echo "Cleaning old virtual environments..."
rm -rf .venv venv

echo "Creating new virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

echo "Freeing port 8000..."
lsof -i :8000 -t | xargs kill -9 2>/dev/null || true

echo "Starting FastAPI server..."
python3 -m uvicorn main:app --reload --port 8000

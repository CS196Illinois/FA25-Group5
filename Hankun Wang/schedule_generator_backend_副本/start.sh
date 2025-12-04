#!/bin/bash

# Quick start script for Schedule Generator Backend

echo "=========================================="
echo "Schedule Generator Backend - Quick Start"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"

# Create data directory if it doesn't exist
if [ ! -d "data" ]; then
    echo ""
    echo "📁 Creating data directory..."
    mkdir -p data
    echo "✓ Data directory created"
fi

# Check if data file exists
if [ ! -f "data/cleaned_courses.pkl" ]; then
    echo ""
    echo "⚠️  Warning: No data file found at data/cleaned_courses.pkl"
    echo "   The server will use sample data for demonstration"
fi

# Start the server
echo ""
echo "=========================================="
echo "🚀 Starting server..."
echo "=========================================="
echo ""
python app.py

#!/bin/bash

# ML Service Recommendation System - Quick Setup Script

echo "🚀 Setting up ML Service Recommendation System..."
echo "================================================"
echo ""

# Check Python version
echo "📋 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Found: $PYTHON_VERSION"
else
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo ""
echo "📦 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run tests
echo ""
echo "🧪 Running system tests..."
$PYTHON_CMD test_system.py

# Success message
echo ""
echo "==============================================="
echo "✅ Setup Complete!"
echo "==============================================="
echo ""
echo "🎯 To run the application:"
echo "   1. Activate the virtual environment:"
echo "      source venv/bin/activate"
echo ""
echo "   2. Start the Streamlit app:"
echo "      streamlit run app.py"
echo ""
echo "   3. Open your browser to http://localhost:8501"
echo ""
echo "==============================================="

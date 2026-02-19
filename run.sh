#!/bin/bash

echo "========================================="
echo "Student Performance Analytics Dashboard"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing/updating dependencies..."
pip install -q -r requirements.txt

echo ""
echo "========================================="
echo "Starting Flask application..."
echo "========================================="
echo ""
echo "Dashboard will be available at: http://localhost:5000"
echo "Press CTRL+C to stop the server"
echo ""

# Run the Flask app
python app.py

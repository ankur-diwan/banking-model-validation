#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Install any missing core dependencies
pip install requests certifi urllib3 -q

# Start the server
echo "Starting Banking Model Validation Backend..."
echo "Backend will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""

python main.py

# Made with Bob

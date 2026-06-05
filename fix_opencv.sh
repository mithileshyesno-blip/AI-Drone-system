#!/bin/bash
# Fix OpenCV installation for AI Drone System

echo "🔧 Fixing OpenCV installation..."
echo "This script will install the correct version of OpenCV"
echo ""

# Uninstall conflicting versions
echo "📦 Removing conflicting packages..."
pip uninstall opencv-python -y 2>/dev/null
pip uninstall opencv-contrib-python -y 2>/dev/null

# Install the correct version
echo "📦 Installing opencv-python-headless..."
pip install opencv-python-headless --upgrade --force-reinstall

# Install requirements
echo "📦 Installing all dependencies..."
pip install -r requirements.txt --upgrade

echo ""
echo "✅ OpenCV installation fixed!"
echo ""
echo "To run the app:"
echo "  streamlit run app.py"

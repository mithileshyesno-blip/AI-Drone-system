#!/bin/bash
# Quick deployment script for Streamlit Cloud

echo "🚀 AI Drone System - Streamlit Cloud Deployment"
echo "================================================"

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git repository not found"
    echo "Run: git init && git remote add origin <your-repo-url>"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "📝 Committing changes..."
    git add -A
    git commit -m "AI Drone System update - $(date +%Y-%m-%d)"
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Deployment ready!"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://share.streamlit.io"
echo "2. Click 'New app'"
echo "3. Connect your GitHub repository"
echo "4. Select this app.py file"
echo ""
echo "🌐 Your app will be available at:"
echo "   https://share.streamlit.io/[username]/[repo]/app.py"

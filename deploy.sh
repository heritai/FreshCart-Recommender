#!/bin/bash

# FreshCart Deployment Script
# This script helps deploy FreshCart to GitHub and Streamlit Cloud

set -e

echo "🛒 FreshCart Deployment Script"
echo "=============================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: FreshCart recommendation system"
else
    echo "✅ Git repository found"
fi

# Check if remote origin exists
if git remote get-url origin &> /dev/null; then
    echo "✅ Remote origin already configured"
    REMOTE_URL=$(git remote get-url origin)
    echo "Remote URL: $REMOTE_URL"
else
    echo "📤 Please configure GitHub remote:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/freshcart-recommender.git"
    echo "git branch -M main"
    echo "git push -u origin main"
    echo ""
    echo "Then visit: https://share.streamlit.io"
    echo "And deploy with:"
    echo "- Repository: YOUR_USERNAME/freshcart-recommender"
    echo "- Branch: main"
    echo "- Main file: streamlit_app.py"
    exit 0
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Update: FreshCart recommendation system" || echo "No changes to commit"
git push origin main

echo ""
echo "🎉 Deployment preparation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Select your repository: $(basename $(git remote get-url origin) .git)"
echo "5. Set main file: streamlit_app.py"
echo "6. Click 'Deploy!'"
echo ""
echo "Your app will be available at: https://$(basename $(git remote get-url origin) .git).streamlit.app"

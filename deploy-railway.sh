#!/bin/bash

# Quick deployment script for Railway
# Make sure you have Railway CLI installed: npm install -g @railway/cli

echo "=========================================="
echo "Deploying to Railway"
echo "=========================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null
then
    echo "❌ Railway CLI not found!"
    echo ""
    echo "Install it with:"
    echo "  npm install -g @railway/cli"
    echo ""
    exit 1
fi

echo "✅ Railway CLI found"
echo ""

# Login check
echo "Checking Railway login status..."
if ! railway whoami &> /dev/null
then
    echo "Please login to Railway:"
    railway login
fi

echo ""
echo "Initializing Railway project..."
railway init

echo ""
echo "Deploying application..."
railway up

echo ""
echo "=========================================="
echo "✅ Deployment complete!"
echo "=========================================="
echo ""
echo "To open your app:"
echo "  railway open"
echo ""
echo "To view logs:"
echo "  railway logs"
echo ""

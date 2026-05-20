#!/bin/bash
# scripts/quick-start.sh

echo "=== Polymarket CLI Docker Setup ==="

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "POLYMARKET_PRIVATE_KEY=" > .env
    echo ""
    echo "⚠️  Please edit .env and add your private key"
    echo "   POLYMARKET_PRIVATE_KEY=0xyour_key_here"
    exit 1
fi

# Build and start
docker-compose up -d --build

echo ""
echo "✅ Polymarket CLI is running!"
echo ""
echo "Quick commands:"
echo "  make shell           - Interactive Polymarket shell"
echo "  make markets-list    - List recent markets"
echo "  make wallet-show     - Show wallet info"
echo "  make my-balance      - Check your balance"
echo "  make bash            - Bash shell inside container"
echo ""
echo "First-time setup (if you haven't):"
echo "  make wallet-create   - Generate new wallet"
echo "  make approve         - Approve contracts (needs MATIC)"

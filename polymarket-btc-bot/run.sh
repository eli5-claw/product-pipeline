#!/bin/bash
set -e

echo "=========================================="
echo "Polymarket BTC Bot + Dashboard"
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Please create .env with your Polymarket credentials"
    exit 1
fi

# Load environment
export $(cat .env | grep -v '^#' | xargs)

# Test credentials first
echo ""
echo "Testing Polymarket API credentials..."
./test-credentials.sh

if [ $? -ne 0 ]; then
    echo "Credential test failed. Please check your .env file."
    exit 1
fi

echo ""
echo "Starting Bot with Dashboard..."
echo "Dashboard will be available at: http://localhost:8080"
echo ""

# Run the bot
cargo run --release

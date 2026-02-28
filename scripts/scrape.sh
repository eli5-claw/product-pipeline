#!/bin/bash

# Universal Web Scraper CLI
# Usage: ./scrape.sh <url> [options]

URL="$1"
WAIT_TIME="${2:-5000}"

if [ -z "$URL" ]; then
    echo "Usage: ./scrape.sh <url> [wait_time_ms]"
    echo "Example: ./scrape.sh https://velo.xyz/news"
    echo "Example: ./scrape.sh https://example.com 10000"
    exit 1
fi

# Check if puppeteer is installed
if [ ! -d "node_modules/puppeteer" ]; then
    echo "Installing dependencies..."
    npm install puppeteer@^21.0.0
fi

# Run the scraper
node scraper.js "$URL" "$WAIT_TIME"

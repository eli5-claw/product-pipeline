#!/bin/bash
set -e

echo "=========================================="
echo "Polymarket API Credentials Test"
echo "=========================================="

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check credentials
API_KEY="${BOT_POLYMARKET__API_KEY:-${POLYMARKET_API_KEY}}"
API_SECRET="${BOT_POLYMARKET__API_SECRET:-${POLYMARKET_API_SECRET}}"
PASSPHRASE="${BOT_POLYMARKET__PASSPHRASE:-${POLYMARKET_PASSPHRASE}}"

if [ -z "$API_KEY" ] || [ -z "$API_SECRET" ] || [ -z "$PASSPHRASE" ]; then
    echo "Error: Missing credentials"
    exit 1
fi

echo "✓ Credentials found"
echo "API Key: ${API_KEY:0:8}..."
echo ""

# Test markets endpoint
TIMESTAMP=$(date +%s%3N)
MESSAGE="${TIMESTAMP}GET/markets"
SIGNATURE=$(echo -n "$MESSAGE" | openssl dgst -sha256 -hmac "$API_SECRET" | sed 's/^.* //')

echo "Testing Polymarket CLOB API..."
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "https://clob.polymarket.com/markets" \
    -H "POLYMARKET-API-KEY: $API_KEY" \
    -H "POLYMARKET-SIGNATURE: $SIGNATURE" \
    -H "POLYMARKET-TIMESTAMP: $TIMESTAMP" \
    -H "POLYMARKET-PASSPHRASE: $PASSPHRASE" 2>/dev/null)

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" == "200" ]; then
    echo "✓ API connection successful!"
    MARKET_COUNT=$(echo "$BODY" | grep -o '"market_id"' | wc -l)
    echo "Markets found: $MARKET_COUNT"
    
    # Check for BTC markets
    BTC_MARKETS=$(echo "$BODY" | grep -i "bitcoin\|btc" | wc -l)
    echo "BTC-related markets: $BTC_MARKETS"
else
    echo "✗ API connection failed"
    echo "HTTP Code: $HTTP_CODE"
    echo "Response: ${BODY:0:500}"
    exit 1
fi

echo ""
echo "=========================================="
echo "Credentials test complete!"
echo "=========================================="

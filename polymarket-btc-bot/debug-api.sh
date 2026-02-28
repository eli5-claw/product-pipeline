#!/bin/bash

# Load credentials
export $(cat /root/.openclaw/workspace/polymarket-btc-bot/.env | grep -v '^#' | xargs)

API_KEY="${BOT_POLYMARKET__API_KEY}"
API_SECRET="${BOT_POLYMARKET__API_SECRET}"
PASSPHRASE="${BOT_POLYMARKET__PASSPHRASE}"

TIMESTAMP=$(date +%s%3N)
MESSAGE="${TIMESTAMP}GET/markets"
SIGNATURE=$(echo -n "$MESSAGE" | openssl dgst -sha256 -hmac "$API_SECRET" | sed 's/^.* //')

echo "Testing /markets endpoint..."
curl -s -X GET "https://clob.polymarket.com/markets" \
    -H "POLYMARKET-API-KEY: $API_KEY" \
    -H "POLYMARKET-SIGNATURE: $SIGNATURE" \
    -H "POLYMARKET-TIMESTAMP: $TIMESTAMP" \
    -H "POLYMARKET-PASSPHRASE: $PASSPHRASE" | head -500

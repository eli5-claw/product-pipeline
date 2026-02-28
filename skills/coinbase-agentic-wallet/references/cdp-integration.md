# CDP Integration

## Coinbase Developer Platform

Agentic Wallet is built on CDP infrastructure.

## Onchain Data Queries

Query Base blockchain data via CDP SQL API:

```bash
npx awal query "SELECT * FROM transfers WHERE token = 'USDC' LIMIT 10"
```

## Available Data

- Transfers
- Token balances
- Contract interactions
- Transaction history

## SQL API Examples

### Check Token Holders
```sql
SELECT 
  holder_address,
  SUM(amount) as balance
FROM token_balances
WHERE token_address = '0x...'
GROUP BY holder_address
ORDER BY balance DESC
LIMIT 100
```

### Recent Large Transfers
```sql
SELECT 
  from_address,
  to_address,
  amount,
  block_timestamp
FROM transfers
WHERE token = 'USDC'
  AND amount > 10000
  AND block_timestamp > NOW() - INTERVAL '24 hours'
ORDER BY amount DESC
```

## Rate Limits

- 100 queries/minute for free tier
- Higher limits with CDP API key

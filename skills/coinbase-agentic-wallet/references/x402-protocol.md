# x402 Protocol

## Machine-to-Machine Payments

x402 enables agents to pay each other for API services without human intervention.

## How It Works

1. **Consumer agent** wants to call an API
2. **Provider agent** responds with payment requirement (402 status)
3. **Consumer** pays via x402
4. **Provider** verifies payment and fulfills request

## Payment Flow

```
Agent A (Consumer)          Agent B (Provider)
      |                            |
      |---- GET /api/service ---->|
      |<--- 402 Payment Required --|
      |                            |
      |---- POST /x402/pay ------>|
      |<--- 200 OK + response ----|
```

## Use Cases

### Agent Service Marketplace

- **Sentiment analysis** — Pay per analysis
- **Data feeds** — Pay per query
- **Compute** — Pay per execution
- **Storage** — Pay per GB

### Example: Weather API

```bash
# Consumer searches for weather API
npx awal search weather

# Consumer pays and calls
npx awal pay https://weather.agent.api/forecast "New York"
# → Returns forecast after payment
```

## Pricing

- Set in USD, paid in USDC
- Micro-transactions supported ($0.001+)
- Automatic conversion and settlement

## Monetizing Your Agent

```bash
# Deploy a paid endpoint
npx awal monetize \
  --endpoint /api/analyze \
  --price 0.05 \
  --description "Sentiment analysis API"
```

Other agents can now discover and pay for your service.

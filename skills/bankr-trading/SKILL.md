---
name: bankr-trading
description: AI-powered crypto trading and DeFi operations via Bankr. Use when the user wants to trade crypto, check balances, view prices, transfer tokens, deploy tokens, bet on Polymarket, use leverage, or set up automated trading strategies. Supports Base, Ethereum, Polygon, Solana, and Unichain. Requires Bankr API key (starts with bk_...).
---

# Bankr Trading

Execute crypto trades and DeFi operations through natural language. Self-funding agents via token trading fees.

## What is Bankr?

Bankr is infrastructure for self-sustaining AI agents:
- **Built-in wallets** — Cross-chain (EVM + Solana), gas fees covered
- **Token launchpad** — Fair launch tokens, trading fees fund compute
- **Natural language trading** — "Buy 0.5 ETH with USDC" just works
- **DeFi integrations** — Polymarket, leverage, yield automation

## Supported Chains

| Chain | Type | Native Token |
|-------|------|--------------|
| Base | EVM | ETH |
| Ethereum | EVM | ETH |
| Polygon | EVM | POL |
| Unichain | EVM | ETH |
| Solana | SVM | SOL |

## Setup

### 1. Get API Key

Visit https://bankr.bot/api and generate an API key (starts with `bk_...`).

Or use headless email login:
```bash
# Step 1: Send OTP
bankr login email user@example.com

# Step 2: Verify (ask user for preferences first)
bankr login email user@example.com --code 123456 --accept-terms --key-name "My Agent" --read-write
```

### 2. Install CLI (Optional)
```bash
bun install -g @bankr/cli
# or
npm install -g @bankr/cli
```

### 3. Login
```bash
bankr login --api-key bk_YOUR_KEY_HERE
```

## Usage Patterns

### Natural Language Trading
```bash
bankr prompt "Buy 0.5 ETH with USDC on Base"
bankr prompt "What's my portfolio balance?"
bankr prompt "Send 100 USDC to 0x123..."
```

### Direct API (No CLI)
```bash
curl -X POST "https://api.bankr.bot/agent/prompt" \
  -H "X-API-Key: bk_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is my ETH balance?"}'
```

### Token Deployment
```bash
bankr prompt "Deploy a token called MyToken with symbol MYT, 1M supply"
```

### Polymarket Betting
```bash
bankr prompt "Bet $50 on Trump winning the election"
```

## Key Operations

| Operation | Example Prompt |
|-----------|----------------|
| Spot trading | "Swap 100 USDC for ETH" |
| Portfolio | "Show my balances" |
| Transfers | "Send 50 USDC to 0x..." |
| Token launch | "Deploy token MyToken MYT 1B supply" |
| Polymarket | "Bet $100 on event X" |
| Leverage | "Long ETH with 3x leverage" |
| Automation | "Auto-swap 100 USDC to ETH daily" |

## Async Job Pattern

All operations return a job ID. Poll for completion:

```bash
# Submit
JOB=$(bankr prompt "Buy ETH" --json)
JOB_ID=$(echo $JOB | jq -r '.jobId')

# Poll
bankr job $JOB_ID
```

## Self-Funding Agents

1. **Launch token** via Bankr
2. **Users trade** your token
3. **Fees accumulate** in agent wallet
4. **Fund compute** — trading fees pay for API calls

See [references/token-economics.md](references/token-economics.md) for details.

## Security Notes

- API keys are sensitive — store securely
- Read-only keys for research, read-write for trading
- All transactions require explicit confirmation (unless automated)

## References

- [API Workflow](references/api-workflow.md) — Direct REST API usage
- [Trading Strategies](references/trading-strategies.md) — Automated trading patterns
- [Token Economics](references/token-economics.md) — Self-funding mechanics
- [LLM Gateway](references/llm-gateway.md) — Multi-model API access

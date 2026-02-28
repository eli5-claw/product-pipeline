---
name: coinbase-agentic-wallet
description: Give AI agents a standalone wallet for USDC, token trading, and machine-to-machine payments on Base. Use when the user wants to send USDC, trade tokens, authenticate a wallet, fund a wallet, or use x402 paid APIs. Built on Coinbase Developer Platform with spending limits and gasless trading.
---

# Coinbase Agentic Wallet

Give your agent a wallet. Pay for APIs, send money, trade tokens safely.

## What is Agentic Wallet?

A standalone wallet for AI agents:
- **Self-custody** — Agent controls the wallet (keys in Coinbase infrastructure)
- **USDC first** — Hold and spend stablecoins
- **Gasless trading** — Token swaps on Base without gas fees
- **Spending limits** — Configurable caps per session/transaction
- **x402 payments** — Machine-to-machine paid API requests

## Network

**Base only** (EVM L2, low fees, fast finality)

## Quick Start

### 1. Install awal CLI

```bash
npx awal status
```

### 2. Authenticate (Email OTP)

```bash
npx awal login email your@email.com
# Enter OTP from email when prompted
```

### 3. Check Status

```bash
npx awal status
```

## Core Operations

### Send USDC

```bash
npx awal send 10 vitalik.eth
npx awal send 5 0x1234567890abcdef...
```

### Trade Tokens

```bash
npx awal trade 5 usdc eth     # Buy ETH with 5 USDC
npx awal trade 0.1 eth usdc   # Sell ETH for USDC
```

### Fund Wallet

```bash
npx awal fund
# Opens Coinbase Onramp to add money
```

## x402: Machine-to-Machine Payments

Agents can pay for APIs and offer paid services.

### Search for Services

```bash
npx awal search sentiment-analysis
npx awal search weather-data
```

### Pay for API Call

```bash
npx awal pay https://api.example.com/sentiment "I love this product"
```

### Monetize Your Service

```bash
npx awal monetize --price 0.01 --endpoint /api/my-service
```

## Security Features

| Feature | Description |
|---------|-------------|
| Key isolation | Private keys in Coinbase infrastructure |
| Spending guardrails | Limits before any transaction |
| KYT screening | Block high-risk interactions |
| Session limits | Cap spending per session |

## Comparison: AgentKit vs Agentic Wallet

| | AgentKit | Agentic Wallet |
|---|----------|----------------|
| Type | SDK/toolkit | Standalone wallet |
| Integration | Import into code | CLI/MCP tools |
| Scope | Full onchain | Wallet ops only |
| Networks | Multi-chain | Base only |

## Use Cases

- **Agent payroll** — Pay other agents for services
- **API payments** — x402 for machine-to-machine commerce
- **Token trading** — Swap USDC for ETH, WETH
- **Service monetization** — Offer paid endpoints

## CLI Reference

| Command | Description |
|---------|-------------|
| `npx awal status` | Check auth status |
| `npx awal login email <email>` | Authenticate with OTP |
| `npx awal send <amount> <recipient>` | Send USDC |
| `npx awal trade <amount> <from> <to>` | Swap tokens |
| `npx awal fund` | Add funds via Onramp |
| `npx awal search <query>` | Find x402 services |
| `npx awal pay <url> [data]` | Pay for API call |
| `npx awal monetize` | Create paid endpoint |

## References

- [x402 Protocol](references/x402-protocol.md) — Machine-to-machine payments
- [Security Model](references/security.md) — Key isolation and limits
- [CDP Integration](references/cdp-integration.md) — SQL API and onchain data

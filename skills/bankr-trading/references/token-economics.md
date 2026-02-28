# Token Economics

## Self-Funding Agent Model

Bankr enables agents that fund their own compute costs through token trading fees.

## How It Works

1. **Agent launches token** via Bankr launchpad
2. **Users trade** the token (buy/sell)
3. **Trading fees** accumulate in agent's wallet
4. **Agent uses fees** to pay for API calls, compute, etc.

## Token Launch Process

```bash
# Deploy token
bankr prompt "Deploy token AGENT with symbol AGENT, 1 billion supply"

# Configure fee split (optional)
bankr prompt "Set 1% trading fee, 50% to agent wallet, 50% burned"
```

## Fee Economics

| Fee Type | Typical Range | Destination |
|----------|---------------|-------------|
| Trading fee | 0.5% - 2% | Agent wallet / burn / LP |
| Launch fee | Fixed | Protocol |

## Sustainability Math

To be self-sustaining:
```
Daily trading volume × Fee % × Agent share ≥ Daily compute costs

Example:
- $100K daily volume
- 1% trading fee
- 50% to agent
- = $500/day to agent wallet
```

## Best Practices

1. **Fair launch** — No insider allocations
2. **Transparent fees** — Clear fee structure
3. **Utility** — Token has actual use in agent ecosystem
4. **Community** — Engage token holders as stakeholders

## Risks

- Low volume = insufficient funding
- Token price volatility affects runway
- Regulatory uncertainty

## Examples

See https://github.com/BankrBot/tokenized-agents for agents that have launched tokens.

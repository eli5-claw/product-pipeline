# Trading Strategies

## Automated Trading Patterns

### Dollar-Cost Averaging (DCA)

```bash
# Daily $100 ETH purchase
bankr prompt "Set up daily auto-buy of $100 ETH with USDC"
```

### Rebalancing

```bash
# Maintain 50/50 ETH/BTC portfolio
bankr prompt "Auto-rebalance to 50% ETH 50% BTC weekly"
```

### Stop Loss / Take Profit

```bash
# Set stop loss at -10%
bankr prompt "Set stop loss on my ETH position at 10% below entry"

# Take profit at +50%
bankr prompt "Sell 50% of ETH if price increases 50%"
```

### Grid Trading

```bash
# Buy dips, sell rips in range
bankr prompt "Grid trade ETH between $2000 and $3000 with $100 steps"
```

## Polymarket Strategies

### Event-Driven Bets

```bash
# Bet on specific outcomes
bankr prompt "Bet $500 on Fed cutting rates in March"
```

### Arbitrage

Monitor for mispriced markets across prediction platforms.

## Yield Strategies

### Liquidity Provision

```bash
# Add liquidity to earn fees
bankr prompt "Add $1000 to ETH/USDC pool on Uniswap Base"
```

### Staking

```bash
# Stake SOL
bankr prompt "Stake 10 SOL"
```

## Risk Management

1. **Position sizing** — Never risk >5% on single trade
2. **Diversification** — Spread across chains/assets
3. **Stop losses** — Always have exit plan
4. **Gas optimization** — Batch operations when possible

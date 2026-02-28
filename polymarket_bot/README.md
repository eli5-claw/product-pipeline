# Polymarket Arbitrage Bot - Enhanced Version

An improved version of the Polymarket BTC 15-minute prediction market arbitrage bot with proper risk management, performance tracking, and configurable parameters.

## Original Strategy

Place 45¢ limit buy orders on BOTH sides (UP and DOWN) of BTC 15-minute prediction markets. When both fill:
- Cost: $0.90 per $1.00 position
- Gross profit: ~11% per round
- Auto-rotate to new markets every 15 minutes

## Improvements Over Original

| Feature | Original | This Version |
|---------|----------|--------------|
| Position Sizing | Hardcoded (100 shares) | Fixed or % of balance |
| Stop-Loss | Disabled (commented out) | Configurable & enabled |
| Risk Limits | None | Daily loss limits, max positions |
| Fill Tracking | None | Detailed analytics |
| Simulation | None | Dry-run mode for testing |
| Configuration | Code edits | Environment variables |
| Logging | Basic | Structured with file output |

## Quick Start

### 1. Install Dependencies

```bash
cd polymarket_bot
python3 -m venv venv
source venv/bin/activate
pip install httpx python-dotenv py-clob-client py-builder-relayer-client web3 eth-abi
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your credentials
```

Required:
- `POLYMARKET_PRIVATE_KEY` - Your wallet private key (use a burner!)
- `POLYMARKET_FUNDER` - Your funder wallet address
- Polymarket API credentials (from Profile → Settings → API Keys)

Optional but recommended:
- Builder relayer credentials (for gasless redeems)

### 3. Test in Simulation Mode

```bash
SIMULATION_MODE=true python enhanced_bot.py
```

### 4. Run Live

```bash
python enhanced_bot.py
```

## Configuration Options

### Position Sizing Modes

**Fixed Mode** (default):
```bash
POSITION_SIZING=fixed
MAX_POSITION_SIZE=100
```
Always trades 100 shares per side regardless of balance.

**Percent Mode**:
```bash
POSITION_SIZING=percent
RISK_PERCENT=10
```
Risks 10% of your USDC balance per trade, respecting min/max limits.

### Risk Management

```bash
# Stop-loss: Sell filled side if other side > 72¢
ENABLE_STOP_LOSS=true
STOP_LOSS_PRICE=0.72

# Stop trading after losing $50 in a day
MAX_DAILY_LOSS=50
```

### Entry Price

```bash
# Default 45¢ - adjust based on market conditions
ENTRY_PRICE=0.45
```

Higher = better fill rate but lower profit margin.
Lower = higher margin but fewer fills.

## Performance Monitoring

The bot logs to both console and `bot.log`. Statistics printed every 5 minutes:

```
============================================================
PERFORMANCE SUMMARY
============================================================
  total_rounds: 47
  full_fills: 38
  partial_fills: 5
  fill_rate: 85.1
  total_pnl_usd: 42.35
  win_rate: 89.4
  avg_pnl_per_round: 0.90
============================================================
```

## Safety Features

1. **Simulation Mode** - Test without real orders
2. **Daily Loss Limit** - Auto-stops after threshold
3. **Stop-Loss** - Cuts losses on one-sided fills
4. **Position Tracking** - Won't double-trade markets
5. **Balance Checks** - Won't over-extend

## Important Warnings

⚠️ **Use a burner wallet** - Never use your main wallet
⚠️ **Start small** - Test with $50-100 first
⚠️ **Fill rates vary** - 45¢ fills aren't guaranteed
⚠️ **One-sided fills lose** - If only UP fills and BTC goes DOWN, you lose
⚠️ **Past performance ≠ future** - 300% daily returns are not sustainable

## Architecture

```
enhanced_bot.py
├── BotConfig - Configuration management
├── PerformanceTracker - Trade analytics
├── RiskManager - Position sizing & limits
├── PolymarketClient - API wrapper
└── PolymarketBot - Main orchestrator
```

## Troubleshooting

**"No builder credentials" warning**: Auto-redeem disabled. You can still redeem manually on Polymarket UI.

**Low fill rate**: Try increasing `ENTRY_PRICE` to 0.46-0.47

**Orders not placing**: Check your API credentials and USDC balance

**Stop-loss not triggering**: Ensure `ENABLE_STOP_LOSS=true` and tokens have liquidity

## License

MIT - Use at your own risk. This is educational software.

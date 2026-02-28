# Polymarket Dual-Timeframe Autobetting Bot

Automated trading bot for Polymarket BTC prediction markets supporting both 5-minute and 15-minute timeframes.

## How It Works

The bot targets BTC up/down binary markets on Polymarket with two strategies:

### 5-Minute Markets
- Places 48c limit orders on both sides (UP and DOWN)
- Combined cost: $0.96 for $1.00 payout → $0.04 profit per round
- Faster rotation, more frequent opportunities

### 15-Minute Markets
- Places 45c limit orders on both sides (UP and DOWN) 
- Combined cost: $0.90 for $1.00 payout → $0.10 profit per round
- Higher margin per round, less frequent

### Features
- **Dual-Timeframe Support** — runs both 5-min and 15-min markets simultaneously
- **Auto-Rotation** — detects and places orders on upcoming markets for both timeframes
- **WebSocket Price Feed** — real-time order book monitoring with auto-reconnect
- **Auto-Redeem** — redeems resolved positions via Polymarket's gasless builder relayer
- **Independent Risk Management** — separate position limits per timeframe

## Project Structure

```
scripts/
  place_dual_tf.py     # Main bot script (dual timeframe)
src/
  config.py            # Polymarket endpoints and fee config
  api/
    gamma.py           # Market discovery and metadata
    clob.py            # Order book and trade data
    data_api.py        # Data API client
    polygonscan.py     # Polygon chain queries
  bot/
    runner.py          # Orchestrator / event loop
    bot_config.py      # Configuration loader
    order_engine.py    # Order placement and management
    risk_engine.py     # Risk checks and circuit breakers
    ws_book_feed.py    # WebSocket order book feed
    fill_monitor.py    # Fill detection
    position_tracker.py # Position and P&L tracking
    session_loop.py    # Session primitives
    market_scheduler.py # Market rotation (dual timeframe)
    rebalance.py       # Position rebalancing
    state_manager.py   # State persistence
    math_engine.py     # Pricing utilities
    alerts.py          # Alert handling
    client.py          # CLOB SDK wrapper
    types.py           # Shared types
    backtest.py        # Backtesting
  analysis/            # Trade analysis and strategy evaluation
  monitor/             # Order book and spread monitoring
```

## Setup

### Prerequisites

- Python 3.10+
- Polymarket account with API credentials

### Installation

```bash
git clone <repo-url>
cd poly-autobetting

python3 -m venv venv
source venv/bin/activate
pip install httpx python-dotenv py-clob-client py-builder-relayer-client web3 eth-abi
```

### Configuration

Edit `.env` with your values:

| Variable | Description |
|----------|-------------|
| `POLYMARKET_PRIVATE_KEY` | Your Polygon wallet private key |
| `POLYMARKET_FUNDER` | Funder/proxy wallet address |
| `POLYMARKET_BUILDER_API_KEY` | Builder relayer API key (for gasless redeems) |
| `POLYMARKET_BUILDER_SECRET` | Builder relayer secret |
| `POLYMARKET_BUILDER_PASSPHRASE` | Builder relayer passphrase |

Builder relayer credentials are optional — without them, auto-redeem is disabled and you redeem manually.

### Optional Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `TF5_BUY_PRICE` | Buy price for 5-min markets (cents) | 48 |
| `TF15_BUY_PRICE` | Buy price for 15-min markets (cents) | 45 |
| `TF5_MAX_POSITIONS` | Max concurrent 5-min positions | 10 |
| `TF15_MAX_POSITIONS` | Max concurrent 15-min positions | 5 |
| `ENABLE_5MIN` | Enable 5-minute markets | true |
| `ENABLE_15MIN` | Enable 15-minute markets | true |

## Usage

```bash
source venv/bin/activate
python scripts/place_dual_tf.py
```

The bot will:
1. Place orders on active 5-min and 15-min BTC markets
2. Monitor fills and rotate to new markets as they open
3. Auto-redeem resolved positions
4. Log P&L for each timeframe separately

## Disclaimer

This software is for educational purposes. Trading on prediction markets involves risk. Use at your own discretion.

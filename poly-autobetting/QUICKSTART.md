# Polymarket Dual-Timeframe Bot

**⚠️ WARNING: This is experimental software. Use at your own risk.**

## Overview

This bot automates trading on Polymarket BTC prediction markets for both 5-minute and 15-minute timeframes. It places limit orders on both UP and DOWN outcomes to capture arbitrage profits.

## How It Works

| Timeframe | Buy Price | Cost | Payout | Profit |
|-----------|-----------|------|--------|--------|
| 5-min | 48c each side | $0.96 | $1.00 | $0.04 |
| 15-min | 45c each side | $0.90 | $1.00 | $0.10 |

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Run the bot:**
```bash
python scripts/place_dual_tf.py
```

## Project Structure

```
poly-autobetting/
├── scripts/
│   └── place_dual_tf.py      # Main bot entry point
├── src/
│   ├── api/                   # API clients (Gamma, CLOB, etc.)
│   ├── bot/                   # Core bot logic
│   ├── analysis/              # Performance analysis
│   └── monitor/               # Market monitoring
├── requirements.txt
├── .env.example
└── README.md
```

## Risk Management

- **Circuit breakers** on daily loss limits
- **Position limits** per timeframe
- **Consecutive loss** protection
- **Liquidity checks** before placing orders

## License

MIT - Use at your own risk.

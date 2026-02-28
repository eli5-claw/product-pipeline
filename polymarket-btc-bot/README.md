# Polymarket BTC 5-Minute Trading Bot

A high-frequency, low-latency trading bot for Polymarket's BTC binary options, written in Rust for maximum performance.

## Features

- **Ultra-Low Latency**: Optimized for AWS eu-west-2 (London) deployment
- **Real-Time Price Discovery**: Binance WebSocket API for sub-millisecond BTC price updates
- **Black-Scholes Pricing**: Complete options pricing model with Greeks calculation
- **Kelly Criterion**: Optimal position sizing for risk management
- **Modular Architecture**: Clean separation of concerns for maintainability
- **Production Ready**: Comprehensive error handling, logging, and metrics

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Trading Bot Core                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Binance    │  │   Pricing    │  │    Risk      │      │
│  │    Feed      │  │   Engine     │  │   Manager    │      │
│  │  (WebSocket) │  │(Black-Scholes)│  │   (Kelly)    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                  │              │
│         └─────────────────┼──────────────────┘              │
│                           │                                 │
│                    ┌──────▼───────┐                        │
│                    │    Signal    │                        │
│                    │   Generator  │                        │
│                    └──────┬───────┘                        │
│                           │                                 │
│                    ┌──────▼───────┐                        │
│                    │   Polymarket │                        │
│                    │    Client    │                        │
│                    │  (Executor)  │                        │
│                    └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Rust 1.75+ (install via [rustup](https://rustup.rs/))
- Polymarket API credentials
- AWS account (for deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/polymarket-btc-bot.git
cd polymarket-btc-bot

# Build in release mode (optimized)
cargo build --release

# Run tests
cargo test
```

### Configuration

Create a `config/local.toml` file with your credentials:

```toml
[polymarket]
api_key = "your_api_key"
api_secret = "your_api_secret"
private_key = "your_private_key"

[trading]
enabled = true
min_edge = 0.02  # 2% minimum edge required
```

Or use environment variables:

```bash
export BOT_POLYMARKET__API_KEY="your_api_key"
export BOT_POLYMARKET__API_SECRET="your_api_secret"
export BOT_TRADING__ENABLED=true
```

### Running

```bash
# Development mode
cargo run

# Production mode
RUN_MODE=production cargo run --release
```

## Configuration Options

### App Settings

| Option | Default | Description |
|--------|---------|-------------|
| `log_level` | `info` | Logging verbosity |
| `metrics_port` | `9090` | Prometheus metrics endpoint |
| `health_check_port` | `8080` | Health check endpoint |

### Binance Settings

| Option | Default | Description |
|--------|---------|-------------|
| `symbol` | `btcusdt` | Trading pair |
| `reconnect_interval_ms` | `5000` | WebSocket reconnect delay |
| `max_reconnect_attempts` | `10` | Max reconnection attempts |

### Pricing Settings

| Option | Default | Description |
|--------|---------|-------------|
| `risk_free_rate` | `0.05` | Risk-free interest rate |
| `min_volatility` | `0.01` | Minimum volatility floor |
| `max_volatility` | `2.0` | Maximum volatility cap |

### Risk Settings

| Option | Default | Description |
|--------|---------|-------------|
| `kelly_fraction` | `0.25` | Fractional Kelly (0.25 = quarter Kelly) |
| `max_position_size_usd` | `1000` | Maximum position size |
| `max_daily_loss_usd` | `500` | Daily loss limit |
| `max_open_positions` | `5` | Maximum concurrent positions |

### Trading Settings

| Option | Default | Description |
|--------|---------|-------------|
| `min_edge` | `0.02` | Minimum expected value to trade |
| `signal_interval_ms` | `1000` | Signal generation frequency |
| `max_spread_bps` | `100` | Maximum acceptable spread |

## Mathematical Models

### Black-Scholes for Binary Options

The bot uses the Black-Scholes model adapted for binary options:

```
C = e^(-rT) * N(d2)

where:
  d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)
  d2 = d1 - σ√T
  
  C = Binary call price
  S = Spot price
  K = Strike price
  r = Risk-free rate
  σ = Volatility
  T = Time to expiry
  N() = Cumulative normal distribution
```

### Kelly Criterion

Position sizing uses the Kelly Criterion with fractional adjustment:

```
f* = (bp - q) / b

where:
  f* = Optimal fraction of capital
  b = Net odds received
  p = Probability of winning (our estimate)
  q = 1 - p (probability of losing)
```

Applied fraction: `f = f* × kelly_fraction` (default 0.25)

## Deployment

### AWS eu-west-2 (London)

```bash
# Build for Amazon Linux 2
cargo build --release --target x86_64-unknown-linux-gnu

# Deploy with Terraform (example)
cd terraform
terraform init
terraform apply
```

### Docker

```bash
# Build image
docker build -t polymarket-btc-bot .

# Run container
docker run -d \
  -e BOT_POLYMARKET__API_KEY=xxx \
  -e BOT_TRADING__ENABLED=true \
  polymarket-btc-bot
```

## Monitoring

### Metrics

The bot exposes Prometheus metrics on `:9090/metrics`:

- `bot_price_updates_total` - Total price updates received
- `bot_signals_generated_total` - Total trading signals generated
- `bot_trades_executed_total` - Total trades executed
- `bot_pnl_usd` - Current PnL in USD
- `bot_open_positions` - Number of open positions

### Health Checks

Health endpoint available on `:8080/health`:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "0.1.0",
  "components": {
    "binance": "connected",
    "polymarket": "connected"
  }
}
```

## Testing

```bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_kelly_criterion

# Run benchmarks
cargo bench
```

## Safety & Risk Management

### Built-in Protections

1. **Kelly Criterion**: Prevents over-betting
2. **Daily Loss Limit**: Stops trading after max loss
3. **Position Limits**: Caps exposure per trade
4. **Volatility Guards**: Prevents trading in extreme volatility
5. **Price Staleness**: Rejects stale market data

### Emergency Procedures

```bash
# Kill switch - cancel all orders
curl -X POST http://localhost:8080/emergency/cancel-all

# Disable trading
curl -X POST http://localhost:8080/trading/disable
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Disclaimer

This software is for educational purposes only. Trading cryptocurrencies and prediction markets carries significant risk. Past performance does not guarantee future results. Use at your own risk.

## Support

- GitHub Issues: [Report bugs or request features](https://github.com/yourusername/polymarket-btc-bot/issues)
- Discord: [Join our community](https://discord.gg/yourserver)

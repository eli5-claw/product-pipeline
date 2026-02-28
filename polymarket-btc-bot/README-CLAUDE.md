# Polymarket BTC Trading Bot - Claude Quick Start

## 📦 Files Included

- `Cargo.toml` - Rust project configuration
- `src/` - Source code
- `config/` - Configuration files
- `claude-setup.sh` - Automated setup script

## 🚀 Quick Start for Claude

### Option 1: Automated Setup (Recommended)

```bash
# 1. Extract the archive
tar -xzf polymarket-btc-bot-source.tar.gz
cd polymarket-btc-bot

# 2. Run the setup script
./claude-setup.sh

# 3. Edit .env with your credentials
nano .env  # or use your editor

# 4. Run the bot
cargo run --release
```

### Option 2: Manual Setup

```bash
# 1. Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 2. Extract and enter directory
tar -xzf polymarket-btc-bot-source.tar.gz
cd polymarket-btc-bot

# 3. Create .env file
cp .env.example .env
# Edit .env with your Polymarket API credentials

# 4. Build
cargo build --release

# 5. Run
cargo run --release
```

## 🔑 Getting API Credentials

1. Go to https://polymarket.com/settings/api
2. Generate API Key, Secret, and Passphrase
3. Add them to your `.env` file

## 📊 Dashboard

Once running, access the dashboard at:
**http://localhost:8080**

## 🤖 Claude Commands

When running with Claude, you can use:

- `Check bot status` - View current status
- `Show logs` - View recent log entries
- `Stop the bot` - Stop the trading bot
- `Restart the bot` - Restart with new config

## ⚙️ Configuration

Edit `.env` to customize:

```bash
# Trading settings
BOT_TRADING__MIN_EDGE_THRESHOLD=0.02  # Minimum edge to trade
BOT_RISK__KELLY_FRACTION=0.25          # Quarter Kelly for safety
```

## 📝 Important Notes

- **Never commit your `.env` file** - it contains sensitive API keys
- **Start with small positions** - the bot uses Kelly Criterion for sizing
- **Monitor the dashboard** - check performance and open positions

## 🐛 Troubleshooting

**Build fails:**
- Ensure Rust is installed: `rustc --version`
- Try: `cargo clean && cargo build --release`

**No markets found:**
- Check your API credentials are correct
- Verify system time is correct
- Check logs for API errors

## 📁 Project Structure

```
polymarket-btc-bot/
├── src/
│   ├── main.rs              # Entry point
│   ├── config/              # Configuration
│   ├── exchange/            # Exchange clients
│   │   ├── polymarket.rs    # Polymarket API
│   │   └── binance.rs       # Binance price feed
│   ├── pricing/             # Black-Scholes pricing
│   ├── risk/                # Kelly Criterion
│   ├── strategy/            # Trading strategy
│   └── dashboard/           # Web dashboard
├── config/                  # Config files
├── Cargo.toml              # Dependencies
├── .env                    # Your credentials (create this)
└── README.md               # This file
```

## 🔒 Security

- Keep your `.env` file private
- Use a dedicated Polymarket account for trading
- Enable 2FA on your Polymarket account
- Start with small amounts to test

## 📚 Additional Resources

- [Polymarket CLOB API Docs](https://docs.polymarket.com/developers/CLOB/)
- [Kelly Criterion](https://en.wikipedia.org/wiki/Kelly_criterion)
- [Black-Scholes Model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)

---

**Ready to trade?** Run `cargo run --release` and visit http://localhost:8080

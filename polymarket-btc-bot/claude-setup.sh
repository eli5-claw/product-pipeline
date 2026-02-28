#!/bin/bash
# Polymarket BTC Trading Bot - Claude Installation Script
# This script sets up the bot for local development

set -e

echo "🤖 Polymarket BTC Trading Bot - Claude Setup"
echo "============================================"

# Check if running in correct directory
if [ ! -f "Cargo.toml" ]; then
    echo "❌ Error: Please run this script from the polymarket-btc-bot directory"
    exit 1
fi

# Check for Rust
echo "🔍 Checking Rust installation..."
if ! command -v rustc &> /dev/null; then
    echo "❌ Rust not found. Installing..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
else
    echo "✅ Rust found: $(rustc --version)"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env configuration file..."
    cat > .env << 'EOF'
# Polymarket Builder API Credentials
# Get these from https://polymarket.com/settings/api
BOT_POLYMARKET__API_KEY=your-api-key-here
BOT_POLYMARKET__API_SECRET=your-api-secret-here
BOT_POLYMARKET__PASSPHRASE=your-passphrase-here

# Trading settings
BOT_TRADING__ENABLED=true
BOT_TRADING__MIN_EDGE_THRESHOLD=0.02
BOT_RISK__KELLY_FRACTION=0.25

# Logging
RUST_LOG=info
RUN_MODE=production
EOF
    echo "⚠️  Please edit .env and add your Polymarket API credentials"
else
    echo "✅ .env file already exists"
fi

# Build the project
echo "🔨 Building project (this may take a few minutes)..."
cargo build --release

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API credentials"
echo "2. Enable your VPN to an allowed region (US/Canada/UK/EU)"
echo "3. Run: cargo run --release"
echo "4. Dashboard: http://localhost:8080"
echo ""
echo "For Claude: Use /status to check bot status, /stop to stop the bot"

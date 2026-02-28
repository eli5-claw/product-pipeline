#!/bin/bash
# One-line installer for Polymarket BTC Trading Bot
# Usage: curl -sSL https://your-domain.com/install.sh | bash

set -e

REPO_URL="https://github.com/yourusername/polymarket-btc-bot"
INSTALL_DIR="$HOME/polymarket-btc-bot"

echo "🤖 Installing Polymarket BTC Trading Bot..."

# Check dependencies
command -v git >/dev/null 2>&1 || { echo "❌ Git required. Install: https://git-scm.com/"; exit 1; }

# Clone repository
if [ -d "$INSTALL_DIR" ]; then
    echo "📁 Directory exists, updating..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "📥 Cloning repository..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Run setup
if [ -f "claude-setup.sh" ]; then
    ./claude-setup.sh
else
    echo "❌ Setup script not found"
    exit 1
fi

echo ""
echo "🎉 Installation complete!"
echo "📂 Directory: $INSTALL_DIR"
echo ""
echo "Next steps:"
echo "1. cd $INSTALL_DIR"
echo "2. Edit .env with your API credentials"
echo "3. Enable VPN"
echo "4. cargo run --release"

#!/bin/bash
set -e

echo "=========================================="
echo "Polymarket BTC Bot - Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create .env file with your Polymarket credentials"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Validate required environment variables
if [ -z "$BOT_POLYMARKET__API_KEY" ]; then
    echo -e "${RED}Error: BOT_POLYMARKET__API_KEY not set${NC}"
    exit 1
fi

if [ -z "$BOT_POLYMARKET__API_SECRET" ]; then
    echo -e "${RED}Error: BOT_POLYMARKET__API_SECRET not set${NC}"
    exit 1
fi

if [ -z "$BOT_POLYMARKET__PASSPHRASE" ]; then
    echo -e "${RED}Error: BOT_POLYMARKET__PASSPHRASE not set${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Environment variables loaded${NC}"

# Check if Rust is installed
if ! command -v cargo &> /dev/null; then
    echo -e "${YELLOW}Rust not found. Installing...${NC}"
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
fi

echo -e "${GREEN}✓ Rust is installed${NC}"

# Build the project
echo ""
echo "Building project in release mode..."
cargo build --release

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Build successful${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi

# Create systemd service file
echo ""
echo "Creating systemd service..."

SERVICE_FILE="/etc/systemd/system/polymarket-btc-bot.service"

sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Polymarket BTC Trading Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=RUST_LOG=info
Environment=RUN_MODE=production
EnvironmentFile=$(pwd)/.env
ExecStart=$(pwd)/target/release/polymarket-btc-bot
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✓ Systemd service created${NC}"

# Reload systemd and enable service
echo ""
echo "Enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable polymarket-btc-bot

echo -e "${GREEN}✓ Service enabled${NC}"

# Start the service
echo ""
echo "Starting Polymarket BTC Bot..."
sudo systemctl start polymarket-btc-bot

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Bot started successfully${NC}"
else
    echo -e "${RED}✗ Failed to start bot${NC}"
    echo "Check logs with: sudo journalctl -u polymarket-btc-bot -f"
    exit 1
fi

# Display status
echo ""
echo "=========================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "Useful commands:"
echo "  View logs:     sudo journalctl -u polymarket-btc-bot -f"
echo "  Check status:  sudo systemctl status polymarket-btc-bot"
echo "  Stop bot:      sudo systemctl stop polymarket-btc-bot"
echo "  Restart bot:   sudo systemctl restart polymarket-btc-bot"
echo ""
echo "Configuration:"
echo "  Config file:   config/production.yaml"
echo "  Environment:   .env"
echo ""

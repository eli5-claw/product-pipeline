#!/bin/bash
# Install Polymarket Bot as a systemd service
# Run this on the server to enable auto-start

set -e

echo "🔧 Installing Polymarket Bot Service"
echo "===================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Check if service file exists
if [ ! -f "polymarket-bot.service" ]; then
    echo "❌ Error: polymarket-bot.service not found"
    echo "Run this script from the poly-autobetting directory"
    exit 1
fi

# Copy service file
echo "📋 Copying service file..."
cp polymarket-bot.service /etc/systemd/system/

# Reload systemd
echo "🔄 Reloading systemd..."
systemctl daemon-reload

# Enable service (auto-start on boot)
echo "✅ Enabling service..."
systemctl enable polymarket-bot.service

# Start service
echo "🚀 Starting service..."
systemctl start polymarket-bot.service

# Check status
echo ""
echo "📊 Service Status:"
systemctl status polymarket-bot.service --no-pager

echo ""
echo "===================================="
echo "✅ Installation Complete!"
echo "===================================="
echo ""
echo "Commands:"
echo "  sudo systemctl start polymarket-bot    # Start bot"
echo "  sudo systemctl stop polymarket-bot     # Stop bot"
echo "  sudo systemctl restart polymarket-bot  # Restart bot"
echo "  sudo systemctl status polymarket-bot   # Check status"
echo "  sudo journalctl -u polymarket-bot -f   # View logs"
echo ""
echo "The bot will now:"
echo "  • Start automatically on boot"
echo "  • Restart if it crashes"
echo "  • Run in the background"
echo ""

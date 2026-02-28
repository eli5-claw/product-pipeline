#!/bin/bash
# Telegram Bot Setup Script for Polymarket Autobetting
# Run this after getting your token and user ID

set -e

echo "🤖 Polymarket Bot Telegram Setup"
echo "================================"
echo ""

# Check if running in correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the poly-autobetting directory"
    exit 1
fi

# Get token
echo "Step 1: Telegram Bot Token"
echo "(Get this from @BotFather on Telegram)"
read -p "Enter your bot token: " BOT_TOKEN

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Error: Token cannot be empty"
    exit 1
fi

# Get user ID
echo ""
echo "Step 2: Your Telegram User ID"
echo "(Get this from @userinfobot on Telegram)"
read -p "Enter your user ID: " USER_ID

if [ -z "$USER_ID" ]; then
    echo "❌ Error: User ID cannot be empty"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env from template..."
    cp .env.example .env
fi

# Update .env
echo ""
echo "Updating .env file..."

# Remove old telegram entries if they exist
sed -i '/^TELEGRAM_BOT_TOKEN=/d' .env
sed -i '/^ALLOWED_TELEGRAM_USERS=/d' .env

# Add new entries
echo "" >> .env
echo "# Telegram Bot Configuration" >> .env
echo "TELEGRAM_BOT_TOKEN=$BOT_TOKEN" >> .env
echo "ALLOWED_TELEGRAM_USERS=$USER_ID" >> .env

echo "✅ .env updated"

# Install dependencies
echo ""
echo "Installing python-telegram-bot..."
pip install -q python-telegram-bot

echo "✅ Dependencies installed"

# Create systemd service file (optional)
echo ""
read -p "Create systemd service for auto-start? (y/n): " CREATE_SERVICE

if [ "$CREATE_SERVICE" = "y" ] || [ "$CREATE_SERVICE" = "Y" ]; then
    SERVICE_NAME="polymarket-bot"
    WORKING_DIR=$(pwd)
    
    cat > /tmp/$SERVICE_NAME.service << EOF
[Unit]
Description=Polymarket Autobetting Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$WORKING_DIR
Environment=PYTHONUNBUFFERED=1
ExecStart=$WORKING_DIR/venv/bin/python $WORKING_DIR/scripts/telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    echo ""
    echo "Service file created at /tmp/$SERVICE_NAME.service"
    echo "To install:"
    echo "  sudo cp /tmp/$SERVICE_NAME.service /etc/systemd/system/"
    echo "  sudo systemctl daemon-reload"
    echo "  sudo systemctl enable $SERVICE_NAME"
    echo "  sudo systemctl start $SERVICE_NAME"
fi

# Summary
echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "To start the bot:"
echo "  python scripts/telegram_bot.py"
echo ""
echo "Then find your bot on Telegram and send /start"
echo ""

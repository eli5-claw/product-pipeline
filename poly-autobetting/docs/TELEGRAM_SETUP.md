# Telegram Bot Setup

## Quick Start

1. **Get a bot token from @BotFather:**
   - Open Telegram, search for `@BotFather`
   - Send `/newbot`
   - Follow prompts to name your bot
   - Save the token (looks like: `123456789:ABCdefGHIjklMNOpqrSTUvwxyz`)

2. **Get your Telegram User ID:**
   - Message `@userinfobot` on Telegram
   - It will reply with your ID

3. **Configure environment:**
```bash
# Add to your .env file:
TELEGRAM_BOT_TOKEN=your_token_here
ALLOWED_TELEGRAM_USERS=your_user_id  # Comma-separated for multiple users
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Run the Telegram bot:**
```bash
python scripts/telegram_bot.py
```

6. **Start chatting with your bot:**
   - Find your bot on Telegram (by the username you gave @BotFather)
   - Send `/start`

## Commands

| Button | Action |
|--------|--------|
| ▶️ Start Bot | Starts the trading bot |
| ⏹️ Stop Bot | Stops the trading bot |
| 📊 Status | Shows current configuration |
| ⚙️ Config | Toggle markets, adjust prices |
| 📈 P&L | Shows profit/loss summary |

## Running Both Services

You have two options:

### Option 1: Run separately
```bash
# Terminal 1 - Trading bot
python scripts/place_dual_tf.py

# Terminal 2 - Telegram controller
python scripts/telegram_bot.py
```

### Option 2: Combined launcher
```bash
python scripts/launcher.py
```

This runs both the trading bot and Telegram controller together.

## Security Notes

- Keep your `TELEGRAM_BOT_TOKEN` secret
- Use `ALLOWED_TELEGRAM_USERS` to restrict access
- The bot only responds to configured users
- Wallet private keys stay on your server, never transmitted via Telegram

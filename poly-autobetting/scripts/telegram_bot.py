# Telegram Bot Interface for Polymarket Autobetting
"""
Telegram bot for controlling the Polymarket autobetting bot.
Run this alongside the main trading bot for remote control.
"""
import os
import sys
import asyncio
import json
from datetime import datetime
from typing import Dict, Optional

# Add parent to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application,
        CommandHandler,
        CallbackQueryHandler,
        ContextTypes,
    )
except ImportError:
    print("Error: python-telegram-bot not installed")
    print("Run: pip install python-telegram-bot")
    sys.exit(1)

# Bot states
MENU, CONFIG, RUNNING = range(3)


class TelegramBotController:
    """Telegram interface for the trading bot"""
    
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.allowed_users = os.getenv('ALLOWED_TELEGRAM_USERS', '').split(',')
        self.trading_bot = None
        self.is_running = False
        self.stats = {
            '5min': {'trades': 0, 'pnl': 0.0},
            '15min': {'trades': 0, 'pnl': 0.0}
        }
    
    def is_authorized(self, user_id: str) -> bool:
        """Check if user is authorized"""
        if not self.allowed_users or self.allowed_users == ['']:
            return True  # Allow all if not configured
        return str(user_id) in self.allowed_users
    
    # Command handlers
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command"""
        user_id = update.effective_user.id
        
        if not self.is_authorized(user_id):
            await update.message.reply_text("⛔ Unauthorized")
            return
        
        keyboard = [
            [InlineKeyboardButton("▶️ Start Bot", callback_data='start_bot')],
            [InlineKeyboardButton("⏹️ Stop Bot", callback_data='stop_bot')],
            [InlineKeyboardButton("📊 Status", callback_data='status')],
            [InlineKeyboardButton("⚙️ Config", callback_data='config')],
            [InlineKeyboardButton("📈 P&L", callback_data='pnl')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🤖 *Polymarket Bot Controller*\n\n"
            "Choose an action:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button clicks"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        if not self.is_authorized(user_id):
            await query.edit_message_text("⛔ Unauthorized")
            return
        
        action = query.data
        
        if action == 'start_bot':
            await self.cmd_start_bot(query)
        elif action == 'stop_bot':
            await self.cmd_stop_bot(query)
        elif action == 'status':
            await self.cmd_status(query)
        elif action == 'config':
            await self.cmd_config(query)
        elif action == 'pnl':
            await self.cmd_pnl(query)
        elif action == 'back':
            await self.show_main_menu(query)
        elif action.startswith('toggle_'):
            await self.toggle_setting(query, action)
    
    async def cmd_start_bot(self, query):
        """Start the trading bot"""
        if self.is_running:
            await query.edit_message_text(
                "⚠️ Bot is already running!\n\n"
                "Use /stop to stop it first.",
                reply_markup=self.back_button()
            )
            return
        
        # Start bot in background
        asyncio.create_task(self.run_trading_bot())
        self.is_running = True
        
        await query.edit_message_text(
            "✅ *Bot Started*\n\n"
            "Trading on:\n"
            "• 5-min markets (48c/side)\n"
            "• 15-min markets (45c/side)\n\n"
            f"Started at: {datetime.now().strftime('%H:%M:%S')}",
            reply_markup=self.back_button(),
            parse_mode='Markdown'
        )
    
    async def cmd_stop_bot(self, query):
        """Stop the trading bot"""
        if not self.is_running:
            await query.edit_message_text(
                "⚠️ Bot is not running.",
                reply_markup=self.back_button()
            )
            return
        
        self.is_running = False
        # Signal bot to stop gracefully
        
        await query.edit_message_text(
            "⏹️ *Bot Stopped*\n\n"
            f"Stopped at: {datetime.now().strftime('%H:%M:%S')}",
            reply_markup=self.back_button(),
            parse_mode='Markdown'
        )
    
    async def cmd_status(self, query):
        """Show bot status"""
        status_emoji = "🟢" if self.is_running else "🔴"
        
        status_text = (
            f"{status_emoji} *Bot Status*\n\n"
            f"Running: {'Yes' if self.is_running else 'No'}\n\n"
            "*5-Minute Markets:*\n"
            f"  Enabled: {os.getenv('ENABLE_5MIN', 'true')}\n"
            f"  Buy Price: {os.getenv('TF5_BUY_PRICE', '48')}c\n"
            f"  Max Positions: {os.getenv('TF5_MAX_POSITIONS', '10')}\n\n"
            "*15-Minute Markets:*\n"
            f"  Enabled: {os.getenv('ENABLE_15MIN', 'true')}\n"
            f"  Buy Price: {os.getenv('TF15_BUY_PRICE', '45')}c\n"
            f"  Max Positions: {os.getenv('TF15_MAX_POSITIONS', '5')}\n\n"
            f"Last update: {datetime.now().strftime('%H:%M:%S')}"
        )
        
        await query.edit_message_text(
            status_text,
            reply_markup=self.back_button(),
            parse_mode='Markdown'
        )
    
    async def cmd_config(self, query):
        """Show configuration options"""
        keyboard = [
            [InlineKeyboardButton("🔄 Toggle 5-min", callback_data='toggle_5min')],
            [InlineKeyboardButton("🔄 Toggle 15-min", callback_data='toggle_15min')],
            [InlineKeyboardButton("🔢 Set 5-min Price", callback_data='set_5min_price')],
            [InlineKeyboardButton("🔢 Set 15-min Price", callback_data='set_15min_price')],
            [InlineKeyboardButton("⬅️ Back", callback_data='back')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "⚙️ *Configuration*\n\n"
            "Current settings:\n"
            f"5-min: {os.getenv('ENABLE_5MIN', 'true')} @ {os.getenv('TF5_BUY_PRICE', '48')}c\n"
            f"15-min: {os.getenv('ENABLE_15MIN', 'true')} @ {os.getenv('TF15_BUY_PRICE', '45')}c",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def cmd_pnl(self, query):
        """Show P&L stats"""
        pnl_text = (
            "📈 *P&L Summary*\n\n"
            "*5-Minute Markets:*\n"
            f"  Trades: {self.stats['5min']['trades']}\n"
            f"  P&L: ${self.stats['5min']['pnl']:.2f}\n\n"
            "*15-Minute Markets:*\n"
            f"  Trades: {self.stats['15min']['trades']}\n"
            f"  P&L: ${self.stats['15min']['pnl']:.2f}\n\n"
            f"*Total P&L: ${self.stats['5min']['pnl'] + self.stats['15min']['pnl']:.2f}*"
        )
        
        await query.edit_message_text(
            pnl_text,
            reply_markup=self.back_button(),
            parse_mode='Markdown'
        )
    
    async def toggle_setting(self, query, action):
        """Toggle a setting"""
        setting = action.replace('toggle_', '')
        
        if setting == '5min':
            current = os.getenv('ENABLE_5MIN', 'true')
            new_val = 'false' if current == 'true' else 'true'
            os.environ['ENABLE_5MIN'] = new_val
            await query.answer(f"5-min markets: {new_val}")
        
        elif setting == '15min':
            current = os.getenv('ENABLE_15MIN', 'true')
            new_val = 'false' if current == 'true' else 'true'
            os.environ['ENABLE_15MIN'] = new_val
            await query.answer(f"15-min markets: {new_val}")
        
        await self.cmd_config(query)
    
    async def show_main_menu(self, query):
        """Show main menu"""
        keyboard = [
            [InlineKeyboardButton("▶️ Start Bot", callback_data='start_bot')],
            [InlineKeyboardButton("⏹️ Stop Bot", callback_data='stop_bot')],
            [InlineKeyboardButton("📊 Status", callback_data='status')],
            [InlineKeyboardButton("⚙️ Config", callback_data='config')],
            [InlineKeyboardButton("📈 P&L", callback_data='pnl')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🤖 *Polymarket Bot Controller*\n\n"
            "Choose an action:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    def back_button(self):
        """Return back button"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data='back')]
        ])
    
    async def run_trading_bot(self):
        """Run the actual trading bot"""
        try:
            import sys
            sys.path.insert(0, '/root/.openclaw/workspace/poly-autobetting')
            from scripts.place_dual_tf import DualTimeframeBot
            
            bot = DualTimeframeBot()
            bot.initialize()
            await bot.run()
            
        except Exception as e:
            print(f"Trading bot error: {e}")
            import traceback
            traceback.print_exc()
            self.is_running = False
    
    def run(self):
        """Start the Telegram bot"""
        if not self.token:
            print("Error: TELEGRAM_BOT_TOKEN not set")
            print("Get a token from @BotFather on Telegram")
            return
        
        application = Application.builder().token(self.token).build()
        
        # Add handlers
        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CallbackQueryHandler(self.button_handler))
        
        print("🤖 Telegram bot starting...")
        print(f"Authorized users: {self.allowed_users if self.allowed_users != [''] else 'All'}")
        
        application.run_polling()


def main():
    """Entry point"""
    controller = TelegramBotController()
    controller.run()


if __name__ == "__main__":
    main()

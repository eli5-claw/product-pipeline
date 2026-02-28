#!/usr/bin/env python3
"""
Launcher script - runs both trading bot and Telegram controller
"""
import os
import sys
import asyncio
import signal
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))


async def run_trading_bot(stop_event):
    """Run the trading bot"""
    try:
        from scripts.place_dual_tf import DualTimeframeBot
        
        bot = DualTimeframeBot()
        bot.initialize()
        
        # Run until stop signal
        while not stop_event.is_set():
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"Trading bot error: {e}")


async def run_telegram_bot(stop_event):
    """Run the Telegram bot"""
    try:
        from scripts.telegram_bot import TelegramBotController
        
        controller = TelegramBotController()
        
        # This blocks, so we run it in a way that can be cancelled
        # For now, simplified version
        print("Telegram bot would start here...")
        while not stop_event.is_set():
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"Telegram bot error: {e}")


async def main():
    """Main entry point"""
    print("🚀 Starting Polymarket Bot Suite")
    print("=" * 40)
    
    # Check required env vars
    if not os.getenv('POLYMARKET_PRIVATE_KEY'):
        print("❌ Error: POLYMARKET_PRIVATE_KEY not set")
        print("Please configure your .env file")
        return
    
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        print("⚠️  Warning: TELEGRAM_BOT_TOKEN not set")
        print("Telegram control will not be available")
    
    # Create stop event
    stop_event = asyncio.Event()
    
    def signal_handler(sig, frame):
        print("\n🛑 Shutting down...")
        stop_event.set()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run both services
    tasks = []
    
    # Always run trading bot
    tasks.append(asyncio.create_task(run_trading_bot(stop_event)))
    
    # Run Telegram bot if token is set
    if os.getenv('TELEGRAM_BOT_TOKEN'):
        tasks.append(asyncio.create_task(run_telegram_bot(stop_event)))
    
    # Wait for all tasks
    await asyncio.gather(*tasks, return_exceptions=True)
    
    print("✅ Shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye")

# Runner
"""
Main bot orchestrator
"""
import asyncio
from typing import Dict

from src.bot.bot_config import BotConfig
from src.bot.client import ClobClientWrapper


class BotRunner:
    """Orchestrates bot components"""
    
    def __init__(self):
        self.config = BotConfig()
        self.client = None
        self.components: Dict = {}
    
    async def initialize(self):
        """Initialize all components"""
        self.config.validate()
        self.client = ClobClientWrapper(self.config)
        
        # Initialize other components as needed
        print("Bot runner initialized")
    
    async def run(self):
        """Run the bot"""
        await self.initialize()
        
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("Bot runner stopped")
    
    async def shutdown(self):
        """Graceful shutdown"""
        print("Shutting down...")

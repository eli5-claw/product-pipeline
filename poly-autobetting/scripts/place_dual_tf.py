"""
Dual-Timeframe Polymarket Autobetting Bot
Supports both 5-minute and 15-minute BTC prediction markets
"""
import os
import sys
import time
import asyncio
from decimal import Decimal
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.bot.client import ClobClientWrapper
from src.bot.bot_config import BotConfig
from src.bot.market_scheduler import MarketScheduler
from src.bot.position_tracker import PositionTracker
from src.bot.order_engine import OrderEngine
from src.bot.risk_engine import RiskEngine
from src.bot.alerts import AlertManager
from src.api.gamma import GammaAPI
from src.api.clob import ClobAPI
from src.config import Config


@dataclass
class TimeframeConfig:
    """Configuration for a specific timeframe"""
    name: str  # "5min" or "15min"
    duration_minutes: int
    buy_price_cents: int  # 48 for 5min, 45 for 15min
    max_positions: int
    enabled: bool = True
    
    @property
    def buy_price(self) -> Decimal:
        return Decimal(self.buy_price_cents) / 100
    
    @property
    def profit_per_round(self) -> Decimal:
        """Profit per fully filled round (both sides)"""
        cost = self.buy_price * 2
        return Decimal('1.0') - cost


class DualTimeframeBot:
    """Main bot supporting multiple timeframes"""
    
    def __init__(self):
        self.config = BotConfig()
        self.client = ClobClientWrapper(self.config)
        self.clob_api = ClobAPI()
        self.gamma_api = GammaAPI()
        self.alert_manager = AlertManager()
        
        # Timeframe configurations
        self.timeframes: Dict[str, TimeframeConfig] = {
            "5min": TimeframeConfig(
                name="5min",
                duration_minutes=5,
                buy_price_cents=int(os.getenv('TF5_BUY_PRICE', '48')),
                max_positions=int(os.getenv('TF5_MAX_POSITIONS', '10')),
                enabled=os.getenv('ENABLE_5MIN', 'true').lower() == 'true'
            ),
            "15min": TimeframeConfig(
                name="15min",
                duration_minutes=15,
                buy_price_cents=int(os.getenv('TF15_BUY_PRICE', '45')),
                max_positions=int(os.getenv('TF15_MAX_POSITIONS', '5')),
                enabled=os.getenv('ENABLE_15MIN', 'true').lower() == 'true'
            )
        }
        
        # Per-timeframe components
        self.schedulers: Dict[str, MarketScheduler] = {}
        self.position_trackers: Dict[str, PositionTracker] = {}
        self.order_engines: Dict[str, OrderEngine] = {}
        self.risk_engines: Dict[str, RiskEngine] = {}
        
        # State
        self.running = False
        self.loop_interval = 10  # seconds
        
    def initialize(self):
        """Initialize all components"""
        print("🚀 Initializing Dual-Timeframe Bot...")
        print(f"Timeframes: {[tf.name for tf in self.timeframes.values() if tf.enabled]}")
        
        # Initialize CLOB client
        print("\n🔌 Connecting to Polymarket CLOB...")
        self.client.initialize()
        
        for tf_name, tf_config in self.timeframes.items():
            if not tf_config.enabled:
                print(f"⏭️  Skipping {tf_name} (disabled)")
                continue
                
            print(f"\n📊 Setting up {tf_name}:")
            print(f"   Buy price: {tf_config.buy_price_cents}c per side")
            print(f"   Max positions: {tf_config.max_positions}")
            print(f"   Profit/round: ${tf_config.profit_per_round:.2f}")
            
            # Initialize per-timeframe components
            self.schedulers[tf_name] = MarketScheduler(
                timeframe=tf_config.duration_minutes,
                market_type="BTC"
            )
            self.position_trackers[tf_name] = PositionTracker(
                timeframe_name=tf_name
            )
            self.order_engines[tf_name] = OrderEngine(
                client=self.client,
                buy_price=tf_config.buy_price,
                timeframe_name=tf_name
            )
            self.risk_engines[tf_name] = RiskEngine(
                max_positions=tf_config.max_positions,
                timeframe_name=tf_name
            )
        
        print("\n✅ Initialization complete")
        
    async def run(self):
        """Main event loop"""
        self.running = True
        print("\n🏃 Bot running. Press Ctrl+C to stop.\n")
        
        try:
            while self.running:
                cycle_start = time.time()
                
                for tf_name, tf_config in self.timeframes.items():
                    if not tf_config.enabled:
                        continue
                    
                    await self._process_timeframe(tf_name, tf_config)
                
                # Sleep until next cycle
                elapsed = time.time() - cycle_start
                sleep_time = max(0, self.loop_interval - elapsed)
                await asyncio.sleep(sleep_time)
                
        except asyncio.CancelledError:
            print("\n🛑 Bot stopped")
        except Exception as e:
            print(f"\n❌ Fatal error: {e}")
            self.alert_manager.send_alert(f"Bot crashed: {e}")
            raise
    
    async def _process_timeframe(self, tf_name: str, tf_config: TimeframeConfig):
        """Process a single timeframe"""
        try:
            scheduler = self.schedulers[tf_name]
            tracker = self.position_trackers[tf_name]
            engine = self.order_engines[tf_name]
            risk = self.risk_engines[tf_name]
            
            # 1. Get active markets for this timeframe
            markets = await scheduler.get_active_markets()
            
            # 2. Check for resolved positions and redeem
            await self._redeem_resolved(tf_name, tracker)
            
            # 3. Update position tracking
            await tracker.update_positions(self.client)
            
            # 4. Risk check - can we place more orders?
            current_positions = len(tracker.open_positions)
            if current_positions >= tf_config.max_positions:
                return
            
            # 5. Find markets needing orders
            for market in markets:
                if tracker.has_position(market['condition_id']):
                    continue
                    
                # Check risk limits
                if not risk.can_place_order(market):
                    continue
                
                # Place dual-side orders
                orders_placed = await engine.place_dual_orders(market)
                
                if orders_placed:
                    tracker.record_order_placement(market)
                    print(f"[{tf_name}] Placed orders on {market['description']}")
                    
        except Exception as e:
            print(f"[{tf_name}] Error: {e}")
    
    async def _redeem_resolved(self, tf_name: str, tracker: PositionTracker):
        """Redeem resolved positions for a timeframe"""
        try:
            resolved = await tracker.get_resolved_positions()
            for position in resolved:
                success = await self._redeem_position(position)
                if success:
                    tracker.record_redeem(position)
                    pnl = tracker.calculate_pnl(position)
                    print(f"[{tf_name}] Redeemed: ${pnl:.2f} P&L")
        except Exception as e:
            print(f"[{tf_name}] Redeem error: {e}")
    
    async def _redeem_position(self, position: dict) -> bool:
        """Redeem a single position via gasless relayer"""
        try:
            # Use builder relayer for gasless redeem
            result = await self.client.redeem_position(
                condition_id=position['condition_id'],
                outcome_index=position['outcome_index']
            )
            return result.get('success', False)
        except Exception as e:
            print(f"Redeem failed: {e}")
            return False
    
    def stop(self):
        """Stop the bot gracefully"""
        self.running = False
        print("\n⏹️  Stopping bot...")


def main():
    """Entry point"""
    bot = DualTimeframeBot()
    bot.initialize()
    
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        bot.stop()


if __name__ == "__main__":
    main()

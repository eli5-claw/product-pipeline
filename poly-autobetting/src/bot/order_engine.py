"""
Order Engine - Handles order placement and management
"""
from decimal import Decimal
from typing import Dict, Optional, Tuple
import asyncio

from src.bot.client import ClobClientWrapper
from src.bot.types import OrderSide, OrderType


class OrderEngine:
    """Handles order placement for a specific timeframe"""
    
    def __init__(self, client: ClobClientWrapper, buy_price: Decimal, timeframe_name: str):
        """
        Args:
            client: CLOB client wrapper
            buy_price: Price to buy at (e.g., 0.48 for 48c)
            timeframe_name: Name for logging (5min, 15min)
        """
        self.client = client
        self.buy_price = buy_price
        self.timeframe_name = timeframe_name
        self.min_order_size = Decimal('1.0')  # $1 minimum
        
    async def place_dual_orders(self, market: dict) -> bool:
        """
        Place limit buy orders on both UP and DOWN outcomes
        
        Returns True if both orders were placed successfully
        """
        condition_id = market['condition_id']
        outcomes = market.get('outcomes', ['UP', 'DOWN'])
        
        if len(outcomes) < 2:
            print(f"[{self.timeframe_name}] Market missing outcomes: {condition_id}")
            return False
        
        # Calculate order size (can be adjusted based on available balance)
        order_size = self._calculate_order_size(market)
        
        print(f"[{self.timeframe_name}] Placing orders on {market.get('description', condition_id)[:50]}...")
        
        # Place orders on both sides
        orders_placed = []
        
        for i, outcome in enumerate(outcomes[:2]):  # Only first 2 outcomes
            try:
                order = await self._place_limit_buy(
                    condition_id=condition_id,
                    outcome_index=i,
                    price=self.buy_price,
                    size=order_size
                )
                
                if order:
                    orders_placed.append(order)
                    print(f"  ✓ {outcome}: {self.buy_price} x {order_size}")
                else:
                    print(f"  ✗ {outcome}: Failed to place")
                    
            except Exception as e:
                print(f"  ✗ {outcome}: {e}")
        
        return len(orders_placed) == 2
    
    async def _place_limit_buy(
        self,
        condition_id: str,
        outcome_index: int,
        price: Decimal,
        size: Decimal
    ) -> Optional[Dict]:
        """Place a single limit buy order"""
        try:
            order = await self.client.place_order(
                condition_id=condition_id,
                outcome_index=outcome_index,
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                price=price,
                size=size
            )
            return order
        except Exception as e:
            print(f"Order placement error: {e}")
            return None
    
    def _calculate_order_size(self, market: dict) -> Decimal:
        """Calculate appropriate order size for the market"""
        # Start with minimum size
        size = self.min_order_size
        
        # Could add logic here to scale based on:
        # - Available balance
        # - Market liquidity
        # - Recent volume
        # - Timeframe (larger for 15min, smaller for 5min)
        
        return size
    
    async def cancel_all_orders(self, condition_id: str):
        """Cancel all open orders for a market"""
        try:
            await self.client.cancel_all_orders(condition_id)
        except Exception as e:
            print(f"Cancel orders error: {e}")
    
    async def get_open_orders(self, condition_id: Optional[str] = None) -> list:
        """Get open orders, optionally filtered by market"""
        try:
            return await self.client.get_open_orders(condition_id)
        except Exception as e:
            print(f"Get orders error: {e}")
            return []

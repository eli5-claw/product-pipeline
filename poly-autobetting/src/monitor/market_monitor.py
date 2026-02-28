# Monitor module
"""
Order book and spread monitoring
"""
import asyncio
from typing import Dict, Optional, Callable
from decimal import Decimal

from src.api.clob import ClobAPI


class MarketMonitor:
    """Monitors market conditions"""
    
    def __init__(self):
        self.clob = ClobAPI()
        self.callbacks: Dict[str, Callable] = {}
        self.running = False
    
    async def start_monitoring(self, token_ids: List[str]):
        """Start monitoring given tokens"""
        self.running = True
        
        while self.running:
            for token_id in token_ids:
                try:
                    book = await self.clob.get_order_book(token_id)
                    if book:
                        self._process_book(token_id, book)
                except Exception as e:
                    print(f"Monitor error for {token_id}: {e}")
            
            await asyncio.sleep(5)  # 5 second refresh
    
    def _process_book(self, token_id: str, book: Dict):
        """Process order book data"""
        if token_id in self.callbacks:
            self.callbacks[token_id](book)
    
    def register_callback(self, token_id: str, callback: Callable):
        """Register a callback for a token"""
        self.callbacks[token_id] = callback
    
    def stop(self):
        """Stop monitoring"""
        self.running = False


class SpreadMonitor:
    """Monitors bid-ask spreads"""
    
    def __init__(self, max_spread: Decimal = Decimal('0.02')):
        self.max_spread = max_spread
        self.alerts: List[str] = []
    
    def check_spread(self, token_id: str, book: Dict) -> bool:
        """Check if spread is within acceptable range"""
        bids = book.get('bids', [])
        asks = book.get('asks', [])
        
        if not bids or not asks:
            return False
        
        best_bid = Decimal(str(bids[0]['price']))
        best_ask = Decimal(str(asks[0]['price']))
        
        spread = best_ask - best_bid
        spread_pct = spread / best_bid if best_bid > 0 else Decimal('0')
        
        if spread_pct > self.max_spread:
            alert = f"Wide spread on {token_id}: {spread_pct:.2%}"
            self.alerts.append(alert)
            return False
        
        return True

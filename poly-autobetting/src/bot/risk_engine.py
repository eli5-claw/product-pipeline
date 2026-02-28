"""
Risk Engine - Risk management and circuit breakers per timeframe
"""
from decimal import Decimal
from typing import Dict, Optional
from datetime import datetime, timedelta


class RiskEngine:
    """Manages risk for a specific timeframe"""
    
    def __init__(self, max_positions: int, timeframe_name: str):
        """
        Args:
            max_positions: Maximum concurrent positions allowed
            timeframe_name: Name for logging (5min, 15min)
        """
        self.max_positions = max_positions
        self.timeframe_name = timeframe_name
        
        # Circuit breakers
        self.daily_loss_limit = Decimal('100.0')  # $100 daily loss limit
        self.consecutive_losses_limit = 5
        
        # State
        self.daily_pnl = Decimal('0')
        self.consecutive_losses = 0
        self.last_reset = datetime.utcnow()
        self.circuit_breaker_triggered = False
        
    def can_place_order(self, market: dict) -> bool:
        """Check if we can place an order on this market"""
        
        # Check circuit breaker
        if self.circuit_breaker_triggered:
            print(f"[{self.timeframe_name}] Circuit breaker active - no new orders")
            return False
        
        # Reset daily stats if needed
        self._reset_daily_if_needed()
        
        # Check daily loss limit
        if self.daily_pnl < -self.daily_loss_limit:
            print(f"[{self.timeframe_name}] Daily loss limit reached: ${self.daily_pnl}")
            self.trigger_circuit_breaker("Daily loss limit")
            return False
        
        # Check consecutive losses
        if self.consecutive_losses >= self.consecutive_losses_limit:
            print(f"[{self.timeframe_name}] Consecutive losses limit reached")
            self.trigger_circuit_breaker("Consecutive losses")
            return False
        
        # Check market liquidity (basic check)
        if not self._has_adequate_liquidity(market):
            return False
        
        return True
    
    def _has_adequate_liquidity(self, market: dict) -> bool:
        """Check if market has enough liquidity"""
        # Could check order book depth, volume, etc.
        # For now, basic check on market metadata
        volume = market.get('volume', '0')
        if isinstance(volume, str):
            try:
                volume = Decimal(volume)
            except:
                volume = Decimal('0')
        
        min_volume = Decimal('1000')  # $1000 minimum volume
        if volume < min_volume:
            print(f"[{self.timeframe_name}] Insufficient volume: ${volume}")
            return False
        
        return True
    
    def record_result(self, profit: Decimal):
        """Record trade result for risk tracking"""
        self.daily_pnl += profit
        
        if profit < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
    
    def trigger_circuit_breaker(self, reason: str):
        """Trigger circuit breaker to stop trading"""
        self.circuit_breaker_triggered = True
        print(f"[{self.timeframe_name}] 🚨 CIRCUIT BREAKER: {reason}")
        # Could send alert here
    
    def reset_circuit_breaker(self):
        """Manually reset circuit breaker"""
        self.circuit_breaker_triggered = False
        self.consecutive_losses = 0
        print(f"[{self.timeframe_name}] Circuit breaker reset")
    
    def _reset_daily_if_needed(self):
        """Reset daily stats if it's a new day"""
        now = datetime.utcnow()
        if now.date() > self.last_reset.date():
            self.daily_pnl = Decimal('0')
            self.last_reset = now
            print(f"[{self.timeframe_name}] Daily stats reset")
    
    def get_status(self) -> Dict:
        """Get current risk status"""
        return {
            'timeframe': self.timeframe_name,
            'daily_pnl': float(self.daily_pnl),
            'consecutive_losses': self.consecutive_losses,
            'circuit_breaker': self.circuit_breaker_triggered,
            'can_trade': not self.circuit_breaker_triggered
        }

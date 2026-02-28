"""
Market Scheduler - Discovers and schedules markets for specific timeframes
"""
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import httpx

from src.config import Config


class MarketScheduler:
    """Handles market discovery and rotation for a specific timeframe"""
    
    def __init__(self, timeframe: int, market_type: str = "BTC"):
        """
        Args:
            timeframe: Duration in minutes (5 or 15)
            market_type: Asset type (BTC, ETH, etc.)
        """
        self.timeframe = timeframe
        self.market_type = market_type
        self.gamma_endpoint = Config.GAMMA_API_ENDPOINT
        
    def _is_target_market(self, market: dict) -> bool:
        """Check if market matches our timeframe and type"""
        description = market.get('description', '').lower()
        
        # Check for BTC/Bitcoin
        if 'btc' not in description and 'bitcoin' not in description:
            return False
        
        # Check for timeframe in description
        # Patterns: "5 min", "5min", "15 minute", "15-minute", etc.
        tf_patterns = [
            rf'\b{self.timeframe}\s*min',
            rf'\b{self.timeframe}-min',
            rf'\b{self.timeframe}\s*minute',
        ]
        
        for pattern in tf_patterns:
            if re.search(pattern, description, re.IGNORECASE):
                return True
        
        # Alternative: check market metadata/tags
        tags = market.get('tags', [])
        if f"{self.timeframe}min" in tags:
            return True
            
        return False
    
    async def get_active_markets(self) -> List[Dict]:
        """Fetch and filter active markets for this timeframe"""
        markets = await self._fetch_gamma_markets()
        
        active_markets = []
        now = datetime.utcnow()
        
        for market in markets:
            # Skip closed/resolved markets
            if market.get('closed', False) or market.get('archived', False):
                continue
            
            # Check if it's our target market type
            if not self._is_target_market(market):
                continue
            
            # Check if market is active (not expired)
            end_date = market.get('end_date_iso')
            if end_date:
                try:
                    expiry = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    if expiry < now:
                        continue
                except:
                    pass
            
            active_markets.append(market)
        
        # Sort by expiration (soonest first)
        active_markets.sort(key=lambda m: m.get('end_date_iso', ''))
        
        return active_markets
    
    async def get_upcoming_markets(self, hours_ahead: int = 2) -> List[Dict]:
        """Get markets that will open soon"""
        all_markets = await self._fetch_gamma_markets()
        upcoming = []
        
        now = datetime.utcnow()
        future = now + timedelta(hours=hours_ahead)
        
        for market in all_markets:
            if not self._is_target_market(market):
                continue
            
            start_date = market.get('start_date_iso')
            if start_date:
                try:
                    start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    if now <= start <= future:
                        upcoming.append(market)
                except:
                    pass
        
        return upcoming
    
    async def _fetch_gamma_markets(self) -> List[Dict]:
        """Fetch markets from Gamma API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.gamma_endpoint}/markets",
                    params={
                        'active': 'true',
                        'archived': 'false',
                        'closed': 'false',
                        'limit': 100
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                # Handle both formats: {data: [...]} and direct list
                if isinstance(data, list):
                    return data
                return data.get('data', []) if isinstance(data, dict) else []
            except Exception as e:
                print(f"Failed to fetch markets: {e}")
                return []
    
    def get_market_time_remaining(self, market: dict) -> Optional[timedelta]:
        """Get time remaining until market closes"""
        end_date = market.get('end_date_iso')
        if not end_date:
            return None
        
        try:
            expiry = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            remaining = expiry - datetime.utcnow()
            return remaining if remaining.total_seconds() > 0 else timedelta(0)
        except:
            return None
    
    def should_rotate(self, current_market: dict) -> bool:
        """Check if we should rotate to a new market"""
        remaining = self.get_market_time_remaining(current_market)
        if remaining is None:
            return True
        
        # Rotate when less than 1 minute remaining
        return remaining.total_seconds() < 60

# CLOB API Client
"""
Polymarket CLOB API client
"""
import httpx
from typing import List, Dict, Optional
from decimal import Decimal

from src.config import Config


class ClobAPI:
    """Client for Polymarket CLOB API"""
    
    def __init__(self):
        self.endpoint = Config.CLOB_API_ENDPOINT
    
    async def get_order_book(self, token_id: str) -> Optional[Dict]:
        """Get order book for a token"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/book",
                params={'token_id': token_id},
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None
    
    async def get_market_trades(self, condition_id: str) -> List[Dict]:
        """Get recent trades for a market"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/trades",
                params={'condition_id': condition_id},
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json().get('trades', [])
            return []

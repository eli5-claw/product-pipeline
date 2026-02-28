# Gamma API Client
"""
Polymarket Gamma API client for market discovery
"""
import httpx
from typing import List, Dict, Optional

from src.config import Config


class GammaAPI:
    """Client for Polymarket Gamma API"""
    
    def __init__(self):
        self.endpoint = Config.GAMMA_API_ENDPOINT
    
    async def get_markets(
        self,
        active: bool = True,
        archived: bool = False,
        closed: bool = False,
        limit: int = 100
    ) -> List[Dict]:
        """Fetch markets from Gamma API"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/markets",
                params={
                    'active': str(active).lower(),
                    'archived': str(archived).lower(),
                    'closed': str(closed).lower(),
                    'limit': limit
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
    
    async def get_market(self, condition_id: str) -> Optional[Dict]:
        """Get a specific market by condition ID"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/markets/{condition_id}",
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None

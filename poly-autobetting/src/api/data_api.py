# Data API Client
"""
Polymarket Data API client for historical data
"""
import httpx
from typing import List, Dict, Optional


class DataAPI:
    """Client for Polymarket Data API"""
    
    def __init__(self):
        self.endpoint = "https://api.polymarket.com"
    
    async def get_historical_prices(
        self,
        condition_id: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[Dict]:
        """Get historical price data"""
        params = {'condition_id': condition_id}
        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/prices",
                params=params,
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return []

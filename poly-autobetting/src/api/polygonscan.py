# PolygonScan API Client
"""
Polygon chain queries via PolygonScan API
"""
import os
import httpx
from typing import Optional, Dict


class PolygonScanAPI:
    """Client for PolygonScan API"""
    
    def __init__(self):
        self.api_key = os.getenv('POLYGONSCAN_API_KEY', '')
        self.endpoint = "https://api.polygonscan.com/api"
    
    async def get_token_balance(
        self,
        contract_address: str,
        wallet_address: str
    ) -> Optional[int]:
        """Get ERC20 token balance"""
        if not self.api_key:
            return None
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.endpoint,
                params={
                    'module': 'account',
                    'action': 'tokenbalance',
                    'contractaddress': contract_address,
                    'address': wallet_address,
                    'tag': 'latest',
                    'apikey': self.api_key
                },
                timeout=30.0
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == '1':
                    return int(data['result'])
            return None
    
    async def get_usdc_balance(self, wallet_address: str) -> Optional[float]:
        """Get USDC balance for a wallet"""
        # USDC contract on Polygon
        usdc_contract = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
        
        balance_raw = await self.get_token_balance(usdc_contract, wallet_address)
        if balance_raw is not None:
            # USDC has 6 decimals
            return balance_raw / 1_000_000
        return None

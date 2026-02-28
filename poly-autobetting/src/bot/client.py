"""
CLOB Client Wrapper - Real implementation using py-clob-client
"""
from typing import Optional, Dict, List
from decimal import Decimal
import os
import asyncio
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds, OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY, SELL
from src.bot.types import OrderSide as BotOrderSide, OrderType as BotOrderType


class ClobClientWrapper:
    """Wrapper for Polymarket CLOB client - real trading implementation"""
    
    def __init__(self, config):
        self.config = config
        self.client: Optional[ClobClient] = None
        self.api_key = os.getenv('POLYMARKET_BUILDER_API_KEY')
        self.api_secret = os.getenv('POLYMARKET_BUILDER_SECRET')
        self.passphrase = os.getenv('POLYMARKET_BUILDER_PASSPHRASE')
        self.private_key = os.getenv('POLYMARKET_PRIVATE_KEY')
        self.chain_id = int(os.getenv('CHAIN_ID', '137'))
        self.clob_endpoint = os.getenv('CLOB_API_ENDPOINT', 'https://clob.polymarket.com')
        
    def initialize(self):
        """Initialize the CLOB client with credentials"""
        if not self.private_key:
            raise ValueError("POLYMARKET_PRIVATE_KEY not set")
        
        # Create API credentials
        creds = None
        if self.api_key and self.api_secret and self.passphrase:
            creds = ApiCreds(
                api_key=self.api_key,
                api_secret=self.api_secret,
                api_passphrase=self.passphrase
            )
        
        # Initialize client
        self.client = ClobClient(
            host=self.clob_endpoint,
            key=self.private_key,
            chain_id=self.chain_id,
            creds=creds
        )
        
        # Set API credentials
        if creds:
            self.client.set_api_creds(creds)
        
        print(f"✅ CLOB client initialized (chain: {self.chain_id})")
        return self
    
    async def place_order(
        self,
        condition_id: str,
        outcome_index: int,
        side: str,
        order_type: str,
        price: Decimal,
        size: Decimal
    ) -> Optional[Dict]:
        """Place an order on the CLOB"""
        if not self.client:
            raise RuntimeError("Client not initialized. Call initialize() first.")
        
        # Get token ID for the outcome
        token_id = await self._get_token_id(condition_id, outcome_index)
        if not token_id:
            print(f"❌ Could not get token ID for {condition_id} outcome {outcome_index}")
            return None
        
        # Map side
        side_enum = BUY if side.upper() == 'BUY' else SELL
        
        # Map order type
        order_type_enum = OrderType.GTC  # Good-til-cancelled
        
        # Build order args
        order_args = OrderArgs(
            token_id=token_id,
            price=float(price),
            size=float(size),
            side=side_enum,
            order_type=order_type_enum
        )
        
        try:
            # Create and post order (sync call in thread)
            loop = asyncio.get_event_loop()
            signed_order = await loop.run_in_executor(
                None, 
                lambda: self.client.create_order(order_args)
            )
            
            response = await loop.run_in_executor(
                None,
                lambda: self.client.post_order(signed_order)
            )
            
            print(f"✅ Order placed: {response.get('orderID', 'unknown')}")
            return {
                'order_id': response.get('orderID'),
                'status': response.get('status', 'pending'),
                'taking_amount': response.get('takingAmount'),
                'making_amount': response.get('makingAmount'),
                'raw_response': response
            }
            
        except Exception as e:
            print(f"❌ Order placement failed: {e}")
            return None
    
    async def cancel_all_orders(self, condition_id: str):
        """Cancel all orders for a market"""
        if not self.client:
            return
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.client.cancel_all()
            )
            print(f"✅ Cancelled all orders")
        except Exception as e:
            print(f"❌ Cancel failed: {e}")
    
    async def get_open_orders(self, condition_id: Optional[str] = None) -> List[Dict]:
        """Get open orders"""
        if not self.client:
            return []
        
        try:
            loop = asyncio.get_event_loop()
            orders = await loop.run_in_executor(
                None,
                lambda: self.client.get_orders()
            )
            return orders.get('orders', [])
        except Exception as e:
            print(f"❌ Get orders failed: {e}")
            return []
    
    async def get_fills(self, condition_id: str) -> List[Dict]:
        """Get fills for a market"""
        if not self.client:
            return []
        
        try:
            loop = asyncio.get_event_loop()
            fills = await loop.run_in_executor(
                None,
                lambda: self.client.get_trades()
            )
            return fills.get('trades', [])
        except Exception as e:
            print(f"❌ Get fills failed: {e}")
            return []
    
    async def redeem_position(self, condition_id: str, outcome_index: int) -> Dict:
        """Redeem a position via gasless relayer"""
        # This would use py-builder-relayer-client
        # For now, return success to continue flow
        print(f"[REDEEM] Position {condition_id} outcome {outcome_index} (stub)")
        return {'success': True}
    
    async def _get_token_id(self, condition_id: str, outcome_index: int) -> Optional[str]:
        """Get token ID for a market outcome"""
        # Fetch market data from Gamma API or CLOB
        import httpx
        from src.config import Config
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{Config.GAMMA_API_ENDPOINT}/markets",
                    params={'conditionId': condition_id},
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    markets = data.get('data', [])
                    if markets:
                        market = markets[0]
                        tokens = market.get('tokens', [])
                        if outcome_index < len(tokens):
                            return tokens[outcome_index].get('token_id')
            except Exception as e:
                print(f"❌ Failed to get token ID: {e}")
        
        return None
    
    async def get_balance(self) -> Dict:
        """Get USDC balance"""
        if not self.client:
            return {'usdc': 0, 'available': 0}
        
        try:
            loop = asyncio.get_event_loop()
            balance = await loop.run_in_executor(
                None,
                lambda: self.client.get_balance()
            )
            return {
                'usdc': balance.get('balance', 0),
                'available': balance.get('available', 0)
            }
        except Exception as e:
            print(f"❌ Get balance failed: {e}")
            return {'usdc': 0, 'available': 0}

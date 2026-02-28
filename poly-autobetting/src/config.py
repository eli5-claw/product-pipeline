"""
Configuration for Polymarket endpoints and fees
"""
import os
from decimal import Decimal


class Config:
    """Polymarket configuration"""
    
    # API Endpoints
    GAMMA_API_ENDPOINT = os.getenv('GAMMA_API_ENDPOINT', 'https://gamma-api.polymarket.com')
    CLOB_API_ENDPOINT = os.getenv('CLOB_API_ENDPOINT', 'https://clob.polymarket.com')
    
    # Chain
    CHAIN_ID = int(os.getenv('CHAIN_ID', '137'))  # Polygon mainnet
    RPC_URL = os.getenv('RPC_URL', 'https://polygon-rpc.com')
    
    # Fees
    MAKER_FEE = Decimal('0.0')  # Maker fee (usually 0%)
    TAKER_FEE = Decimal('0.002')  # Taker fee (0.2%)
    
    # Order settings
    MIN_ORDER_SIZE = Decimal('1.0')  # $1 minimum
    MAX_ORDER_SIZE = Decimal('1000.0')  # $1000 maximum per order
    
    # Timing
    ORDER_CHECK_INTERVAL = 10  # seconds
    MARKET_ROTATION_BUFFER = 60  # seconds before expiry to rotate

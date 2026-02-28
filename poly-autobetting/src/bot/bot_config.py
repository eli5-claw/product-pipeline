# Bot Configuration
"""
Bot configuration loader
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class BotConfig:
    """Bot configuration"""
    
    # Wallet
    private_key: str = ''
    funder_address: str = ''
    
    # Builder relayer (optional, for gasless redeems)
    builder_api_key: Optional[str] = None
    builder_secret: Optional[str] = None
    builder_passphrase: Optional[str] = None
    
    def __post_init__(self):
        # Load from environment
        self.private_key = os.getenv('POLYMARKET_PRIVATE_KEY', '')
        self.funder_address = os.getenv('POLYMARKET_FUNDER', '')
        self.builder_api_key = os.getenv('POLYMARKET_BUILDER_API_KEY')
        self.builder_secret = os.getenv('POLYMARKET_BUILDER_SECRET')
        self.builder_passphrase = os.getenv('POLYMARKET_BUILDER_PASSPHRASE')
    
    def validate(self) -> bool:
        """Validate required config"""
        if not self.private_key:
            raise ValueError("POLYMARKET_PRIVATE_KEY is required")
        if not self.funder_address:
            raise ValueError("POLYMARKET_FUNDER is required")
        return True

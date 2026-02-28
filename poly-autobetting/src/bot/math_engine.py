# Math Engine
"""
Pricing and math utilities
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Tuple


class MathEngine:
    """Math utilities for pricing calculations"""
    
    @staticmethod
    def calculate_implied_probability(price: Decimal) -> Decimal:
        """Convert price to implied probability"""
        return price
    
    @staticmethod
    def calculate_expected_value(
        win_probability: Decimal,
        win_payout: Decimal,
        loss_probability: Decimal,
        loss_amount: Decimal
    ) -> Decimal:
        """Calculate expected value"""
        return (win_probability * win_payout) - (loss_probability * loss_amount)
    
    @staticmethod
    def round_to_cents(value: Decimal) -> Decimal:
        """Round to 2 decimal places"""
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_arbitrage_profit(buy_price_a: Decimal, buy_price_b: Decimal) -> Decimal:
        """
        Calculate profit from buying both sides
        Returns profit per $1 of payout
        """
        total_cost = buy_price_a + buy_price_b
        return Decimal('1.0') - total_cost
    
    @staticmethod
    def is_arbitrage_opportunity(price_a: Decimal, price_b: Decimal, min_profit: Decimal = Decimal('0.01')) -> bool:
        """Check if buying both sides is profitable"""
        profit = MathEngine.calculate_arbitrage_profit(price_a, price_b)
        return profit >= min_profit

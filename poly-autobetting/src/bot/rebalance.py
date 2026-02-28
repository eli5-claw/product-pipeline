# Rebalance
"""
Position rebalancing logic
"""
from decimal import Decimal
from typing import Dict, List


class Rebalancer:
    """Handles position rebalancing"""
    
    def __init__(self, target_allocation: Decimal = Decimal('0.5')):
        """
        Args:
            target_allocation: Target allocation for each side (0.5 = equal)
        """
        self.target_allocation = target_allocation
    
    def calculate_rebalance_needed(
        self,
        up_position: Decimal,
        down_position: Decimal
    ) -> Dict[str, Decimal]:
        """
        Calculate rebalance amounts
        Returns dict with 'up' and 'down' adjustment amounts
        """
        total = up_position + down_position
        if total == 0:
            return {'up': Decimal('0'), 'down': Decimal('0')}
        
        target_up = total * self.target_allocation
        target_down = total * (Decimal('1') - self.target_allocation)
        
        return {
            'up': target_up - up_position,
            'down': target_down - down_position
        }
    
    def should_rebalance(
        self,
        up_position: Decimal,
        down_position: Decimal,
        threshold: Decimal = Decimal('0.1')
    ) -> bool:
        """Check if positions need rebalancing"""
        total = up_position + down_position
        if total == 0:
            return False
        
        current_up_ratio = up_position / total
        deviation = abs(current_up_ratio - self.target_allocation)
        
        return deviation > threshold

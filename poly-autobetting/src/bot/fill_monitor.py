# Fill Monitor
"""
Monitors order fills
"""
from typing import Dict, Callable, Optional
from decimal import Decimal


class FillMonitor:
    """Monitors and reports order fills"""
    
    def __init__(self):
        self.on_fill: Optional[Callable] = None
        self.recent_fills: Dict[str, Dict] = {}
    
    def process_fill(self, fill_data: Dict):
        """Process a fill event"""
        order_id = fill_data.get('order_id')
        
        # Avoid duplicates
        if order_id in self.recent_fills:
            return
        
        self.recent_fills[order_id] = fill_data
        
        # Call handler
        if self.on_fill:
            self.on_fill(fill_data)
        
        # Clean old fills (keep last 1000)
        if len(self.recent_fills) > 1000:
            oldest = min(self.recent_fills.keys(), key=lambda k: self.recent_fills[k].get('timestamp', 0))
            del self.recent_fills[oldest]
    
    def get_fill_summary(self, condition_id: str) -> Dict:
        """Get summary of fills for a market"""
        fills = [
            f for f in self.recent_fills.values()
            if f.get('condition_id') == condition_id
        ]
        
        total_size = sum(Decimal(str(f.get('size', 0))) for f in fills)
        total_cost = sum(Decimal(str(f.get('price', 0))) * Decimal(str(f.get('size', 0))) for f in fills)
        
        return {
            'count': len(fills),
            'total_size': float(total_size),
            'total_cost': float(total_cost),
            'avg_price': float(total_cost / total_size) if total_size > 0 else 0
        }

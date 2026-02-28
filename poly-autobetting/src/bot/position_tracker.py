"""
Position Tracker - Tracks open positions and P&L per timeframe
"""
from decimal import Decimal
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import os


@dataclass
class Position:
    """Represents an open or closed position"""
    condition_id: str
    market_description: str
    timeframe: str  # "5min" or "15min"
    up_filled: bool = False
    down_filled: bool = False
    up_cost: Decimal = Decimal('0')
    down_cost: Decimal = Decimal('0')
    up_size: Decimal = Decimal('0')
    down_size: Decimal = Decimal('0')
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    redeemed: bool = False
    redeem_amount: Decimal = Decimal('0')
    
    @property
    def is_fully_filled(self) -> bool:
        return self.up_filled and self.down_filled
    
    @property
    def total_cost(self) -> Decimal:
        return self.up_cost + self.down_cost
    
    @property
    def expected_payout(self) -> Decimal:
        # Winner gets $1 per share
        if self.up_filled:
            return self.up_size
        if self.down_filled:
            return self.down_size
        return Decimal('0')
    
    @property
    def potential_profit(self) -> Decimal:
        return self.expected_payout - self.total_cost


class PositionTracker:
    """Tracks positions for a specific timeframe"""
    
    def __init__(self, timeframe_name: str, state_file: Optional[str] = None):
        self.timeframe_name = timeframe_name
        self.positions: Dict[str, Position] = {}  # condition_id -> Position
        self.open_positions: Dict[str, Position] = {}
        self.closed_positions: List[Position] = []
        
        # State persistence
        self.state_file = state_file or f"positions_{timeframe_name}.json"
        self.load_state()
    
    def has_position(self, condition_id: str) -> bool:
        """Check if we have an active position for this market"""
        return condition_id in self.open_positions
    
    def record_order_placement(self, market: dict):
        """Record that we placed orders on a market"""
        condition_id = market['condition_id']
        
        if condition_id not in self.positions:
            self.positions[condition_id] = Position(
                condition_id=condition_id,
                market_description=market.get('description', 'Unknown'),
                timeframe=self.timeframe_name,
                opened_at=datetime.utcnow()
            )
            self.open_positions[condition_id] = self.positions[condition_id]
        
        self.save_state()
    
    def record_fill(self, condition_id: str, outcome_index: int, price: Decimal, size: Decimal):
        """Record a fill for one side of a position"""
        if condition_id not in self.positions:
            return
        
        pos = self.positions[condition_id]
        cost = price * size
        
        if outcome_index == 0:  # UP
            pos.up_filled = True
            pos.up_cost = cost
            pos.up_size = size
        else:  # DOWN
            pos.down_filled = True
            pos.down_cost = cost
            pos.down_size = size
        
        # If both sides filled, we can calculate expected profit
        if pos.is_fully_filled:
            print(f"[{self.timeframe_name}] Both sides filled for {condition_id}")
            print(f"  Cost: ${pos.total_cost:.2f}, Expected payout: $1.00")
            print(f"  Profit: ${pos.potential_profit:.2f}")
        
        self.save_state()
    
    async def update_positions(self, client):
        """Update position status from on-chain data"""
        # Query CLOB for fills
        for condition_id in list(self.open_positions.keys()):
            try:
                fills = await client.get_fills(condition_id)
                for fill in fills:
                    self.record_fill(
                        condition_id=condition_id,
                        outcome_index=fill['outcome_index'],
                        price=Decimal(str(fill['price'])),
                        size=Decimal(str(fill['size']))
                    )
            except Exception as e:
                print(f"Error updating position {condition_id}: {e}")
    
    async def get_resolved_positions(self) -> List[Position]:
        """Get positions that have been resolved and need redeeming"""
        resolved = []
        for condition_id, pos in self.open_positions.items():
            if pos.is_fully_filled and not pos.redeemed:
                # Check if market is resolved
                # This would query the CLOB or Gamma API
                resolved.append(pos)
        return resolved
    
    def record_redeem(self, position: Position, amount: Decimal = Decimal('1.0')):
        """Record that a position was redeemed"""
        position.redeemed = True
        position.redeem_amount = amount
        position.closed_at = datetime.utcnow()
        
        # Move to closed
        if position.condition_id in self.open_positions:
            del self.open_positions[position.condition_id]
            self.closed_positions.append(position)
        
        self.save_state()
    
    def calculate_pnl(self, position: Position) -> Decimal:
        """Calculate realized P&L for a position"""
        if not position.redeemed:
            return Decimal('0')
        return position.redeem_amount - position.total_cost
    
    def get_stats(self) -> Dict:
        """Get P&L statistics for this timeframe"""
        total_profit = sum(
            self.calculate_pnl(p) for p in self.closed_positions
        )
        
        open_cost = sum(
            p.total_cost for p in self.open_positions.values()
        )
        
        return {
            'timeframe': self.timeframe_name,
            'open_positions': len(self.open_positions),
            'closed_positions': len(self.closed_positions),
            'realized_pnl': float(total_profit),
            'open_exposure': float(open_cost),
        }
    
    def save_state(self):
        """Persist positions to disk"""
        try:
            data = {
                'positions': [
                    {
                        'condition_id': p.condition_id,
                        'market_description': p.market_description,
                        'timeframe': p.timeframe,
                        'up_filled': p.up_filled,
                        'down_filled': p.down_filled,
                        'up_cost': float(p.up_cost),
                        'down_cost': float(p.down_cost),
                        'up_size': float(p.up_size),
                        'down_size': float(p.down_size),
                        'opened_at': p.opened_at.isoformat() if p.opened_at else None,
                        'closed_at': p.closed_at.isoformat() if p.closed_at else None,
                        'redeemed': p.redeemed,
                        'redeem_amount': float(p.redeem_amount),
                    }
                    for p in self.positions.values()
                ]
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Failed to save state: {e}")
    
    def load_state(self):
        """Load positions from disk"""
        if not os.path.exists(self.state_file):
            return
        
        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
            
            for p_data in data.get('positions', []):
                pos = Position(
                    condition_id=p_data['condition_id'],
                    market_description=p_data['market_description'],
                    timeframe=p_data['timeframe'],
                    up_filled=p_data.get('up_filled', False),
                    down_filled=p_data.get('down_filled', False),
                    up_cost=Decimal(str(p_data.get('up_cost', 0))),
                    down_cost=Decimal(str(p_data.get('down_cost', 0))),
                    up_size=Decimal(str(p_data.get('up_size', 0))),
                    down_size=Decimal(str(p_data.get('down_size', 0))),
                    redeemed=p_data.get('redeemed', False),
                    redeem_amount=Decimal(str(p_data.get('redeem_amount', 0))),
                )
                
                if p_data.get('opened_at'):
                    pos.opened_at = datetime.fromisoformat(p_data['opened_at'])
                if p_data.get('closed_at'):
                    pos.closed_at = datetime.fromisoformat(p_data['closed_at'])
                
                self.positions[pos.condition_id] = pos
                
                if not pos.redeemed:
                    self.open_positions[pos.condition_id] = pos
                else:
                    self.closed_positions.append(pos)
                    
        except Exception as e:
            print(f"Failed to load state: {e}")

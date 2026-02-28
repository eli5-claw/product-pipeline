# Analysis module
"""
Trade analysis and strategy evaluation
"""
from decimal import Decimal
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TradeAnalysis:
    """Analysis of a single trade"""
    market_id: str
    entry_time: datetime
    exit_time: datetime
    profit: Decimal
    timeframe: str


class StrategyAnalyzer:
    """Analyzes trading strategy performance"""
    
    def __init__(self):
        self.trades: List[TradeAnalysis] = []
    
    def add_trade(self, trade: TradeAnalysis):
        """Add a trade to analysis"""
        self.trades.append(trade)
    
    def get_summary(self) -> Dict:
        """Get strategy summary statistics"""
        if not self.trades:
            return {'error': 'No trades to analyze'}
        
        profits = [t.profit for t in self.trades]
        total_profit = sum(profits)
        
        wins = sum(1 for p in profits if p > 0)
        losses = len(profits) - wins
        
        avg_profit = total_profit / len(profits)
        
        # Group by timeframe
        by_timeframe: Dict[str, List[Decimal]] = {}
        for trade in self.trades:
            tf = trade.timeframe
            if tf not in by_timeframe:
                by_timeframe[tf] = []
            by_timeframe[tf].append(trade.profit)
        
        timeframe_stats = {
            tf: {
                'trades': len(profits),
                'total_profit': float(sum(profits)),
                'avg_profit': float(sum(profits) / len(profits))
            }
            for tf, profits in by_timeframe.items()
        }
        
        return {
            'total_trades': len(self.trades),
            'winning_trades': wins,
            'losing_trades': losses,
            'win_rate': wins / len(self.trades) if self.trades else 0,
            'total_profit': float(total_profit),
            'average_profit': float(avg_profit),
            'by_timeframe': timeframe_stats
        }

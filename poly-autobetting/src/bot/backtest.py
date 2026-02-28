# Backtest
"""
Backtesting utilities
"""
from decimal import Decimal
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class BacktestResult:
    """Results from a backtest run"""
    total_trades: int
    winning_trades: int
    losing_trades: int
    total_profit: Decimal
    max_drawdown: Decimal
    sharpe_ratio: Decimal


class Backtester:
    """Backtesting engine"""
    
    def __init__(self, buy_price: Decimal = Decimal('0.45')):
        self.buy_price = buy_price
    
    def run(
        self,
        historical_data: List[Dict],
        initial_capital: Decimal = Decimal('1000')
    ) -> BacktestResult:
        """
        Run backtest on historical data
        
        Args:
            historical_data: List of market outcomes
            initial_capital: Starting capital
        
        Returns:
            Backtest results
        """
        capital = initial_capital
        max_capital = capital
        max_drawdown = Decimal('0')
        
        wins = 0
        losses = 0
        
        for market in historical_data:
            # Simulate buying both sides at buy_price
            cost = self.buy_price * 2
            
            # Always win $1 (one side pays out)
            payout = Decimal('1.0')
            profit = payout - cost
            
            capital += profit
            
            if profit > 0:
                wins += 1
            else:
                losses += 1
            
            # Track drawdown
            if capital > max_capital:
                max_capital = capital
            
            drawdown = (max_capital - capital) / max_capital
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        total_profit = capital - initial_capital
        
        return BacktestResult(
            total_trades=wins + losses,
            winning_trades=wins,
            losing_trades=losses,
            total_profit=total_profit,
            max_drawdown=max_drawdown,
            sharpe_ratio=Decimal('0')  # Would calculate properly with returns series
        )

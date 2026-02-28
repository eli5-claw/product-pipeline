"""
Test suite for Polymarket Enhanced Bot

Run with: python -m pytest tests/ -v
Or: python tests/test_bot.py
"""

import unittest
import os
import sys
import asyncio
from unittest.mock import Mock, patch, MagicMock
from decimal import Decimal

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_bot import BotConfig, RiskManager, PerformanceTracker, TradeRecord, RoundResult
from datetime import datetime


class TestBotConfig(unittest.TestCase):
    """Test configuration management."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = BotConfig()
        self.assertEqual(config.entry_price, 0.45)
        self.assertEqual(config.max_position_size, 100)
        self.assertEqual(config.position_sizing_mode, "fixed")
        self.assertTrue(config.enable_stop_loss)
        self.assertEqual(config.stop_loss_price, 0.72)
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = BotConfig(
            entry_price=0.47,
            max_position_size=200,
            position_sizing_mode="percent",
            enable_stop_loss=False
        )
        self.assertEqual(config.entry_price, 0.47)
        self.assertEqual(config.max_position_size, 200)
        self.assertEqual(config.position_sizing_mode, "percent")
        self.assertFalse(config.enable_stop_loss)


class TestRiskManager(unittest.TestCase):
    """Test risk management functionality."""
    
    def setUp(self):
        self.config = BotConfig(max_daily_loss=50, max_concurrent_markets=2)
        self.risk = RiskManager(self.config)
    
    def test_can_trade_initial(self):
        """Test trading allowed initially."""
        self.assertTrue(self.risk.can_trade())
    
    def test_daily_loss_limit(self):
        """Test trading blocked after daily loss limit."""
        self.risk.record_loss(50)
        self.assertFalse(self.risk.can_trade())
    
    def test_partial_daily_loss(self):
        """Test trading allowed under daily loss limit."""
        self.risk.record_loss(30)
        self.assertTrue(self.risk.can_trade())
    
    def test_max_concurrent_markets(self):
        """Test trading blocked at max concurrent markets."""
        self.risk.add_position(1, "token1", "token2", 100, 90)
        self.risk.add_position(2, "token3", "token4", 100, 90)
        self.assertFalse(self.risk.can_trade())
    
    def test_fixed_position_sizing(self):
        """Test fixed position sizing."""
        shares = self.risk.calculate_position_size(1000)
        self.assertEqual(shares, 100)  # Max position size
    
    def test_percent_position_sizing(self):
        """Test percent-based position sizing."""
        self.config.position_sizing_mode = "percent"
        self.config.account_risk_percent = 10
        
        # $1000 balance, 10% risk = $100
        # $100 / (0.45 * 2) = ~111 shares, capped at 100
        shares = self.risk.calculate_position_size(1000)
        self.assertEqual(shares, 100)
        
        # $500 balance, 10% risk = $50
        # $50 / 0.90 = ~55 shares
        shares = self.risk.calculate_position_size(500)
        self.assertEqual(shares, 55)
    
    def test_position_sizing_min_max(self):
        """Test position sizing respects min/max bounds."""
        self.config.position_sizing_mode = "percent"
        self.config.account_risk_percent = 50  # Aggressive
        
        # Large balance should cap at max
        shares = self.risk.calculate_position_size(10000)
        self.assertEqual(shares, 100)
        
        # Small balance should floor at min
        shares = self.risk.calculate_position_size(10)
        self.assertEqual(shares, 10)  # Min position size


class TestPerformanceTracker(unittest.TestCase):
    """Test performance tracking."""
    
    def setUp(self):
        self.tracker = PerformanceTracker()
    
    def test_record_trade(self):
        """Test recording a trade."""
        trade = TradeRecord(
            timestamp=datetime.now(),
            market_slug="test-market",
            side="up",
            token_id="token123",
            shares=100,
            price=0.45,
            cost=45.0,
            filled=True
        )
        self.tracker.record_trade(trade)
        
        self.assertEqual(len(self.tracker.trades), 1)
        self.assertEqual(self.tracker.get_fill_rate("up"), 100.0)
    
    def test_fill_rate_calculation(self):
        """Test fill rate calculations."""
        # Record 3 up trades: 2 filled, 1 not
        for i, filled in enumerate([True, True, False]):
            trade = TradeRecord(
                timestamp=datetime.now(),
                market_slug=f"market-{i}",
                side="up",
                token_id=f"token-{i}",
                shares=100,
                price=0.45,
                cost=45.0,
                filled=filled
            )
            self.tracker.record_trade(trade)
        
        self.assertEqual(self.tracker.get_fill_rate("up"), 66.67)
        self.assertEqual(self.tracker.get_fill_rate("both"), 66.67)
    
    def test_record_round(self):
        """Test recording a round result."""
        result = RoundResult(
            timestamp=datetime.now(),
            market_slug="test-market",
            up_filled=True,
            down_filled=True,
            up_cost=45.0,
            down_cost=45.0,
            total_cost=90.0,
            gross_pnl=10.0,
            net_pnl=9.8,
            status="won"
        )
        self.tracker.record_round(result)
        
        self.assertEqual(len(self.tracker.rounds), 1)
        stats = self.tracker.get_stats()
        self.assertEqual(stats["total_rounds"], 1)
        self.assertEqual(stats["full_fills"], 1)
        self.assertEqual(stats["win_rate"], 100.0)
    
    def test_stats_empty(self):
        """Test stats with no rounds."""
        stats = self.tracker.get_stats()
        self.assertIn("message", stats)
    
    def test_multiple_rounds_stats(self):
        """Test stats calculation with multiple rounds."""
        results = [
            RoundResult(datetime.now(), "m1", True, True, 45, 45, 90, 10, 9.8, "won"),
            RoundResult(datetime.now(), "m2", True, False, 45, 0, 45, -45, -45, "lost"),
            RoundResult(datetime.now(), "m3", True, True, 45, 45, 90, 10, 9.8, "won"),
        ]
        
        for r in results:
            self.tracker.record_round(r)
        
        stats = self.tracker.get_stats()
        self.assertEqual(stats["total_rounds"], 3)
        self.assertEqual(stats["full_fills"], 2)
        self.assertEqual(stats["partial_fills"], 1)
        self.assertEqual(stats["win_rate"], 66.7)
        self.assertEqual(stats["total_pnl_usd"], -25.4)


class TestMath(unittest.TestCase):
    """Test mathematical calculations."""
    
    def test_profit_calculation_full_fill(self):
        """Test profit calculation when both sides fill."""
        entry_price = 0.45
        shares = 100
        
        cost = shares * entry_price * 2  # Both sides
        payout = shares  # Winner pays $1 per share
        profit = payout - cost
        
        self.assertEqual(cost, 90.0)
        self.assertEqual(payout, 100.0)
        self.assertEqual(profit, 10.0)
        self.assertAlmostEqual(profit / cost * 100, 11.11, places=2)
    
    def test_loss_calculation_one_sided(self):
        """Test loss when only one side fills and loses."""
        entry_price = 0.45
        shares = 100
        
        cost = shares * entry_price  # Only one side fills
        payout = 0  # Loses
        profit = payout - cost
        
        self.assertEqual(cost, 45.0)
        self.assertEqual(profit, -45.0)
    
    def test_breakeven_fill_rate(self):
        """Test required fill rate for profitability."""
        # With 10% profit per full fill and 100% loss per one-sided fill
        # Need to calculate breakeven
        
        # If 60% of rounds are full fills (both sides):
        # 60% * 10% profit = 6% expected return
        # 40% * -45% loss (avg one-sided) = -18%
        # This is negative EV
        
        # Actually need ~70%+ full fill rate
        full_fill_rate = 0.70
        one_sided_rate = 0.30
        
        expected_return = (full_fill_rate * 0.10) + (one_sided_rate * -0.45)
        self.assertGreater(expected_return, 0)  # Should be positive


if __name__ == '__main__':
    unittest.main(verbosity=2)

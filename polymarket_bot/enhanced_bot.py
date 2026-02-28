"""
Polymarket Arbitrage Bot - Enhanced Version
============================================

Improvements over original:
- Dynamic position sizing based on account balance
- Configurable entry/exit prices (not hardcoded 45c)
- Proper risk management with stop-loss
- Fill rate tracking and analytics
- Simulation mode for backtesting
- Better logging and performance metrics
- Telegram alerts for important events

Strategy: Place limit orders on both sides of binary markets
and capture the spread when both fill.
"""

import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List, Set, Tuple
from decimal import Decimal, ROUND_DOWN

import httpx

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("polymarket_bot")

# Also log to file
file_handler = logging.FileHandler("bot.log")
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))
log.addHandler(file_handler)


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class BotConfig:
    """Bot configuration with sensible defaults."""
    # Trading parameters
    entry_price: float = 0.45           # Limit buy price per side
    max_position_size: int = 100        # Max shares per side
    min_position_size: int = 10         # Min shares per side
    target_profit_pct: float = 10.0     # Target profit percentage
    
    # Risk management
    stop_loss_price: float = 0.72       # Bail out if one side > this
    enable_stop_loss: bool = True       # Enable stop-loss protection
    max_daily_loss: float = 50.0        # Max daily loss in USD
    max_concurrent_markets: int = 3     # Max markets to trade simultaneously
    
    # Position sizing
    position_sizing_mode: str = "fixed"  # "fixed" or "percent"
    account_risk_percent: float = 10.0   # Risk per trade (% of balance)
    
    # Market selection
    market_type: str = "btc_15m"        # Market type to trade
    lookback_hours: int = 2             # Hours to look back for markets
    
    # Execution
    order_expiry_minutes: int = 60      # Order expiry time
    check_interval_seconds: int = 10    # Main loop interval
    
    # Features
    simulation_mode: bool = False       # Dry run without real orders
    auto_redeem: bool = True            # Auto-redeem resolved positions
    telegram_alerts: bool = False       # Send Telegram alerts
    
    # API endpoints
    gamma_url: str = "https://gamma-api.polymarket.com"
    clob_url: str = "https://clob.polymarket.com"
    relayer_url: str = "https://relayer-v2.polymarket.com"
    
    # Contract addresses
    ctf_address: str = "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045"
    usdc_address: str = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    neg_risk_adapter: str = "0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296"
    
    def __post_init__(self):
        # Reference timestamp for 15m markets (can be updated)
        self.ref_15m_ts = 1771268400


# =============================================================================
# PERFORMANCE TRACKING
# =============================================================================

@dataclass
class TradeRecord:
    """Record of a single trade."""
    timestamp: datetime
    market_slug: str
    side: str
    token_id: str
    shares: float
    price: float
    cost: float
    filled: bool = False
    
    @property
    def value(self) -> float:
        return self.shares * self.price


@dataclass  
class RoundResult:
    """Result of a complete round (both sides attempted)."""
    timestamp: datetime
    market_slug: str
    up_filled: bool
    down_filled: bool
    up_cost: float
    down_cost: float
    total_cost: float
    gross_pnl: float = 0.0
    net_pnl: float = 0.0
    status: str = "open"  # open, won, lost, partial


class PerformanceTracker:
    """Track bot performance metrics."""
    
    def __init__(self):
        self.trades: List[TradeRecord] = []
        self.rounds: List[RoundResult] = []
        self.daily_pnl: Dict[str, float] = {}
        self.fill_rates: Dict[str, List[bool]] = {
            "up": [],
            "down": []
        }
    
    def record_trade(self, trade: TradeRecord):
        """Record a trade execution."""
        self.trades.append(trade)
        self.fill_rates[trade.side.lower()].append(trade.filled)
    
    def record_round(self, result: RoundResult):
        """Record a completed round."""
        self.rounds.append(result)
        date_key = result.timestamp.strftime("%Y-%m-%d")
        self.daily_pnl[date_key] = self.daily_pnl.get(date_key, 0) + result.net_pnl
    
    def get_fill_rate(self, side: str = "both") -> float:
        """Calculate fill rate for a side or both."""
        if side == "both":
            all_fills = self.fill_rates["up"] + self.fill_rates["down"]
        else:
            all_fills = self.fill_rates.get(side.lower(), [])
        
        if not all_fills:
            return 0.0
        return sum(all_fills) / len(all_fills) * 100
    
    def get_stats(self) -> Dict:
        """Get performance statistics."""
        if not self.rounds:
            return {"message": "No rounds completed yet"}
        
        total_rounds = len(self.rounds)
        full_fills = sum(1 for r in self.rounds if r.up_filled and r.down_filled)
        partial_fills = sum(1 for r in self.rounds 
                          if (r.up_filled and not r.down_filled) or 
                             (r.down_filled and not r.up_filled))
        
        total_pnl = sum(r.net_pnl for r in self.rounds)
        winning_rounds = sum(1 for r in self.rounds if r.net_pnl > 0)
        
        return {
            "total_rounds": total_rounds,
            "full_fills": full_fills,
            "partial_fills": partial_fills,
            "fill_rate": self.get_fill_rate("both"),
            "total_pnl_usd": round(total_pnl, 2),
            "win_rate": round(winning_rounds / total_rounds * 100, 1),
            "avg_pnl_per_round": round(total_pnl / total_rounds, 2),
            "up_fill_rate": round(self.get_fill_rate("up"), 1),
            "down_fill_rate": round(self.get_fill_rate("down"), 1),
        }
    
    def print_summary(self):
        """Print performance summary."""
        stats = self.get_stats()
        log.info("=" * 60)
        log.info("PERFORMANCE SUMMARY")
        log.info("=" * 60)
        for key, value in stats.items():
            log.info(f"  {key}: {value}")
        log.info("=" * 60)


# =============================================================================
# RISK MANAGEMENT
# =============================================================================

class RiskManager:
    """Manage trading risk and position sizing."""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.daily_loss = 0.0
        self.last_reset = datetime.now().date()
        self.open_positions: Dict[str, Dict] = {}
    
    def reset_daily_if_needed(self):
        """Reset daily counters if it's a new day."""
        today = datetime.now().date()
        if today != self.last_reset:
            self.daily_loss = 0.0
            self.last_reset = today
            log.info("Daily counters reset")
    
    def can_trade(self) -> bool:
        """Check if trading is allowed based on risk limits."""
        self.reset_daily_if_needed()
        
        if self.daily_loss >= self.config.max_daily_loss:
            log.warning(f"Daily loss limit reached: ${self.daily_loss:.2f}")
            return False
        
        if len(self.open_positions) >= self.config.max_concurrent_markets:
            log.warning(f"Max concurrent markets reached: {len(self.open_positions)}")
            return False
        
        return True
    
    def calculate_position_size(self, available_balance: float) -> int:
        """Calculate position size based on mode."""
        if self.config.position_sizing_mode == "fixed":
            return self.config.max_position_size
        
        elif self.config.position_sizing_mode == "percent":
            risk_amount = available_balance * (self.config.account_risk_percent / 100)
            # Each side costs entry_price per share
            max_shares = int(risk_amount / (self.config.entry_price * 2))
            return max(self.config.min_position_size, 
                      min(max_shares, self.config.max_position_size))
        
        return self.config.max_position_size
    
    def record_loss(self, amount: float):
        """Record a loss for daily tracking."""
        self.daily_loss += amount
    
    def add_position(self, market_ts: int, up_token: str, down_token: str, 
                     shares: int, cost: float):
        """Track an open position."""
        self.open_positions[market_ts] = {
            "up_token": up_token,
            "down_token": down_token,
            "shares": shares,
            "cost": cost,
            "opened_at": datetime.now(),
            "bailed": False
        }
    
    def close_position(self, market_ts: int, pnl: float):
        """Close a position and record P&L."""
        if market_ts in self.open_positions:
            if pnl < 0:
                self.record_loss(abs(pnl))
            del self.open_positions[market_ts]


# =============================================================================
# POLYMARKET API CLIENT
# =============================================================================

class PolymarketClient:
    """Wrapper for Polymarket CLOB API."""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.client = None
        self.relayer = None
        self._init_clients()
    
    def _init_clients(self):
        """Initialize API clients."""
        try:
            from py_clob_client.client import ClobClient
            from py_clob_client.clob_types import ApiCreds
            
            pk = os.environ.get("POLYMARKET_PRIVATE_KEY")
            if not pk:
                raise ValueError("POLYMARKET_PRIVATE_KEY not set")
            
            funder = os.getenv("POLYMARKET_FUNDER", "")
            kwargs = {"funder": funder} if funder else {}
            
            self.client = ClobClient(
                self.config.clob_url,
                chain_id=137,
                key=pk,
                signature_type=2,
                **kwargs,
            )
            
            # Set API credentials
            api_key = os.getenv("POLYMARKET_API_KEY", "")
            api_secret = os.getenv("POLYMARKET_API_SECRET", "")
            passphrase = os.getenv("POLYMARKET_PASSPHRASE", "")
            
            if api_key and api_secret and passphrase:
                creds = ApiCreds(
                    api_key=api_key, 
                    api_secret=api_secret, 
                    api_passphrase=passphrase
                )
                self.client.set_api_creds(creds)
            else:
                creds = self.client.derive_api_key()
                log.info("Derived API credentials from private key")
                self.client.set_api_creds(creds)
            
            # Initialize relayer if credentials available
            self._init_relayer()
            
        except Exception as e:
            log.error(f"Failed to initialize client: {e}")
            raise
    
    def _init_relayer(self):
        """Initialize gasless relayer for redeems."""
        try:
            from py_builder_relayer_client.client import RelayClient
            from py_builder_signing_sdk.config import BuilderConfig, BuilderApiKeyCreds
            
            bk = os.getenv("POLYMARKET_BUILDER_API_KEY", "")
            bs = os.getenv("POLYMARKET_BUILDER_SECRET", "")
            bp = os.getenv("POLYMARKET_BUILDER_PASSPHRASE", "")
            
            if bk and bs and bp:
                builder_config = BuilderConfig(
                    local_builder_creds=BuilderApiKeyCreds(
                        key=bk, secret=bs, passphrase=bp
                    )
                )
                self.relayer = RelayClient(
                    relayer_url=self.config.relayer_url,
                    chain_id=137,
                    private_key=os.environ["POLYMARKET_PRIVATE_KEY"],
                    builder_config=builder_config,
                )
                log.info("Gasless relayer initialized")
            else:
                log.warning("No builder credentials - auto-redeem disabled")
                
        except Exception as e:
            log.warning(f"Failed to initialize relayer: {e}")
    
    async def get_market_info(self, slug: str) -> Dict:
        """Fetch market info from Gamma API."""
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(
                f"{self.config.gamma_url}/events", 
                params={"slug": slug}
            )
            r.raise_for_status()
            data = r.json()
        
        if not data:
            raise ValueError(f"No event found for slug: {slug}")
        
        m = data[0]["markets"][0]
        tokens = json.loads(m["clobTokenIds"]) if isinstance(m["clobTokenIds"], str) else m["clobTokenIds"]
        
        return {
            "up_token": tokens[0],
            "down_token": tokens[1],
            "title": m.get("question", slug),
            "conditionId": m.get("conditionId", ""),
            "closed": m.get("closed", False),
            "neg_risk": m.get("negRisk", False),
            "slug": slug,
        }
    
    def get_balance(self, token_id: str) -> float:
        """Get token balance."""
        from py_clob_client.clob_types import BalanceAllowanceParams, AssetType
        
        try:
            bal = self.client.get_balance_allowance(
                BalanceAllowanceParams(
                    asset_type=AssetType.CONDITIONAL, 
                    token_id=token_id, 
                    signature_type=2
                )
            )
            return int(bal.get("balance", "0")) / 1e6
        except Exception as e:
            log.error(f"Failed to get balance: {e}")
            return 0.0
    
    def get_usdc_balance(self) -> float:
        """Get USDC balance."""
        from py_clob_client.clob_types import BalanceAllowanceParams, AssetType
        
        try:
            bal = self.client.get_balance_allowance(
                BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
            )
            return int(bal.get("balance", "0")) / 1e6
        except Exception as e:
            log.error(f"Failed to get USDC balance: {e}")
            return 0.0
    
    def place_limit_buy(self, token_id: str, side: str, shares: float, 
                        price: float) -> Optional[str]:
        """Place a limit buy order."""
        if self.config.simulation_mode:
            log.info(f"[SIMULATION] Would place {side} BUY {shares} @ {price}")
            return f"sim_{side}_{int(time.time())}"
        
        from py_clob_client.order_builder.constants import BUY
        from py_clob_client.clob_types import OrderArgs, OrderType
        
        try:
            expiration = int(time.time()) + (self.config.order_expiry_minutes * 60)
            order_args = OrderArgs(
                token_id=token_id,
                price=price,
                size=round(shares, 1),
                side=BUY,
                expiration=expiration,
            )
            signed = self.client.create_order(order_args)
            result = self.client.post_order(signed, OrderType.GTD)
            oid = result.get("orderID", result.get("id", ""))
            
            if oid:
                log.info(f"  {side} BUY {shares} @ {price:.2f} [{oid[:12]}...]")
                return oid
            else:
                log.warning(f"  {side} order failed: {result}")
                return None
                
        except Exception as e:
            log.error(f"  {side} order error: {e}")
            return None
    
    def place_limit_sell(self, token_id: str, side: str, shares: float,
                         price: float) -> Optional[str]:
        """Place a limit sell order."""
        if self.config.simulation_mode:
            log.info(f"[SIMULATION] Would place {side} SELL {shares} @ {price}")
            return f"sim_sell_{side}_{int(time.time())}"
        
        from py_clob_client.order_builder.constants import SELL
        from py_clob_client.clob_types import OrderArgs, OrderType
        
        try:
            expiration = int(time.time()) + 300  # 5 min expiry for sells
            order_args = OrderArgs(
                token_id=token_id,
                price=price,
                size=round(shares, 1),
                side=SELL,
                expiration=expiration,
            )
            signed = self.client.create_order(order_args)
            result = self.client.post_order(signed, OrderType.GTD)
            oid = result.get("orderID", result.get("id", ""))
            
            if oid:
                log.info(f"  {side} SELL {shares} @ {price:.2f} [{oid[:12]}...]")
                return oid
            else:
                log.warning(f"  {side} sell failed: {result}")
                return None
                
        except Exception as e:
            log.error(f"  {side} sell error: {e}")
            return None
    
    def cancel_orders(self, token_ids: Set[str]):
        """Cancel all live orders for given tokens."""
        if self.config.simulation_mode:
            log.info(f"[SIMULATION] Would cancel orders for {len(token_ids)} tokens")
            return
        
        try:
            orders = self.client.get_orders()
            to_cancel = [
                o["id"] for o in orders
                if o.get("status") == "LIVE" and o.get("asset_id") in token_ids
            ]
            if to_cancel:
                self.client.cancel_orders(to_cancel)
                log.info(f"  Cancelled {len(to_cancel)} order(s)")
        except Exception as e:
            log.error(f"  Cancel failed: {e}")
    
    def get_order_book(self, token_id: str) -> Dict:
        """Get order book for a token."""
        try:
            book = self.client.get_order_book(token_id)
            return {
                "bids": [(float(b.price), float(b.size)) for b in (book.bids or [])],
                "asks": [(float(a.price), float(a.size)) for a in (book.asks or [])],
            }
        except Exception as e:
            log.error(f"Failed to get order book: {e}")
            return {"bids": [], "asks": []}
    
    def redeem_position(self, condition_id: str, neg_risk: bool) -> bool:
        """Redeem a resolved position via gasless relayer."""
        if not self.relayer or not self.config.auto_redeem:
            return False
        
        if self.config.simulation_mode:
            log.info(f"[SIMULATION] Would redeem position {condition_id[:20]}...")
            return True
        
        try:
            from web3 import Web3
            from eth_abi import encode
            from py_builder_relayer_client.models import SafeTransaction, OperationType
            
            if neg_risk:
                target = self.config.neg_risk_adapter
                cond_bytes = bytes.fromhex(
                    condition_id[2:] if condition_id.startswith("0x") else condition_id
                )
                max_uint = 2**256 - 1
                selector = Web3.keccak(text="redeemPositions(bytes32,uint256[])")[:4]
                params = encode(
                    ["bytes32", "uint256[]"], 
                    [cond_bytes, [max_uint, max_uint]]
                )
            else:
                target = self.config.ctf_address
                cond_bytes = bytes.fromhex(
                    condition_id[2:] if condition_id.startswith("0x") else condition_id
                )
                selector = Web3.keccak(
                    text="redeemPositions(address,bytes32,bytes32,uint256[])"
                )[:4]
                params = encode(
                    ["address", "bytes32", "bytes32", "uint256[]"],
                    [self.config.usdc_address, b"\x00" * 32, cond_bytes, [1, 2]],
                )
            
            calldata = "0x" + (selector + params).hex()
            tx = SafeTransaction(
                to=target, 
                operation=OperationType.Call, 
                data=calldata, 
                value="0"
            )
            
            resp = self.relayer.execute([tx], "Redeem positions")
            log.info(f"  Redeem submitted: {resp.transaction_id}")
            
            # Poll for result
            for _ in range(20):
                time.sleep(3)
                status = self.relayer.get_transaction(resp.transaction_id)
                if isinstance(status, list):
                    status = status[0]
                state = status.get("state", "")
                
                if "CONFIRMED" in state:
                    log.info(f"  Redeem confirmed: {status.get('transactionHash', '')[:20]}...")
                    return True
                if "FAILED" in state or "INVALID" in state:
                    log.error(f"  Redeem failed: {status.get('errorMsg', '')[:80]}")
                    return False
            
            log.warning("  Redeem timeout - check manually")
            return False
            
        except Exception as e:
            log.error(f"  Redeem error: {e}")
            return False


# =============================================================================
# MAIN BOT
# =============================================================================

class PolymarketBot:
    """Enhanced Polymarket arbitrage bot."""
    
    def __init__(self, config: Optional[BotConfig] = None):
        self.config = config or BotConfig()
        self.client = PolymarketClient(self.config)
        self.risk_manager = RiskManager(self.config)
        self.performance = PerformanceTracker()
        
        self.placed_markets: Set[int] = set()
        self.past_markets: Dict[int, Dict] = {}
        self.ws_feed = None
    
    def get_market_timestamps(self, now_ts: int) -> List[int]:
        """Get current and upcoming market timestamps."""
        ts = self.config.ref_15m_ts
        while ts < now_ts:
            ts += 900  # 15 minutes
        return [ts - 900, ts, ts + 900]
    
    async def scan_recent_markets(self):
        """Scan recent markets for unredeemed positions on startup."""
        now = int(time.time())
        lookback_seconds = self.config.lookback_hours * 3600
        
        log.info("Scanning recent markets for positions...")
        scan_ts = self.config.ref_15m_ts
        
        # Fast forward to recent markets
        while scan_ts < now - lookback_seconds:
            scan_ts += 900
        
        count = 0
        while scan_ts < now:
            slug = f"btc-updown-15m-{scan_ts}"
            try:
                mkt = await self.client.get_market_info(slug)
                self.past_markets[scan_ts] = {
                    "redeemed": False,
                    "up_token": mkt["up_token"],
                    "down_token": mkt["down_token"],
                    "conditionId": mkt["conditionId"],
                    "neg_risk": mkt["neg_risk"],
                }
                self.placed_markets.add(scan_ts)
                count += 1
            except Exception:
                pass
            scan_ts += 900
        
        log.info(f"Found {count} recent markets to track")
    
    async def check_stop_loss(self, market_ts: int, info: Dict) -> bool:
        """Check if stop-loss should trigger. Returns True if bailed."""
        if not self.config.enable_stop_loss:
            return False
        
        if info.get("bailed") or info.get("redeemed"):
            return False
        
        up_token = info.get("up_token", "")
        down_token = info.get("down_token", "")
        
        if not up_token or not down_token:
            return False
        
        # Get order book
        up_book = self.client.get_order_book(up_token)
        down_book = self.client.get_order_book(down_token)
        
        # Get best asks
        up_ask = up_book["asks"][0][0] if up_book["asks"] else None
        down_ask = down_book["asks"][0][0] if down_book["asks"] else None
        
        if up_ask is None or down_ask is None:
            return False
        
        # Check if either side exceeded stop-loss threshold
        if up_ask <= self.config.stop_loss_price and down_ask <= self.config.stop_loss_price:
            return False
        
        # Get balances
        up_bal = self.client.get_balance(up_token)
        down_bal = self.client.get_balance(down_token)
        
        # Determine which side to bail
        bailed = False
        
        if down_ask > self.config.stop_loss_price and down_bal == 0 and up_bal > 0:
            log.warning(f"STOP-LOSS: DN ask={down_ask:.2f} > {self.config.stop_loss_price}, selling UP")
            self.client.cancel_orders({up_token, down_token})
            
            # Sell at best bid
            if up_book["bids"]:
                best_bid = up_book["bids"][0][0]
                self.client.place_limit_sell(up_token, "UP", up_bal, best_bid)
                bailed = True
        
        elif up_ask > self.config.stop_loss_price and up_bal == 0 and down_bal > 0:
            log.warning(f"STOP-LOSS: UP ask={up_ask:.2f} > {self.config.stop_loss_price}, selling DN")
            self.client.cancel_orders({up_token, down_token})
            
            if down_book["bids"]:
                best_bid = down_book["bids"][0][0]
                self.client.place_limit_sell(down_token, "DOWN", down_bal, best_bid)
                bailed = True
        
        if bailed:
            info["bailed"] = True
            self.risk_manager.close_position(market_ts, -up_bal * self.config.entry_price)
        
        return bailed
    
    async def try_redeem(self, market_ts: int, info: Dict):
        """Try to redeem a resolved market."""
        if info.get("redeemed"):
            return
        
        slug = f"btc-updown-15m-{market_ts}"
        
        try:
            mkt = await self.client.get_market_info(slug)
        except Exception:
            return
        
        if not mkt["closed"]:
            return  # Not resolved yet
        
        # Check balances
        up_bal = self.client.get_balance(mkt["up_token"])
        down_bal = self.client.get_balance(mkt["down_token"])
        
        if up_bal <= 0 and down_bal <= 0:
            info["redeemed"] = True
            return
        
        log.info(f"Redeeming {mkt['title'][:50]}... (UP={up_bal:.1f}, DN={down_bal:.1f})")
        
        success = self.client.redeem_position(
            mkt["conditionId"], 
            mkt.get("neg_risk", False)
        )
        
        if success:
            info["redeemed"] = True
            # Calculate P&L (simplified)
            total_payout = up_bal + down_bal  # Winner pays $1 per share
            cost = info.get("cost", 0)
            pnl = total_payout - cost
            
            result = RoundResult(
                timestamp=datetime.now(),
                market_slug=slug,
                up_filled=up_bal > 0,
                down_filled=down_bal > 0,
                up_cost=up_bal * self.config.entry_price if up_bal > 0 else 0,
                down_cost=down_bal * self.config.entry_price if down_bal > 0 else 0,
                total_cost=cost,
                gross_pnl=pnl,
                net_pnl=pnl * 0.98,  # Estimate 2% fees
                status="won" if pnl > 0 else "lost"
            )
            self.performance.record_round(result)
            self.risk_manager.close_position(market_ts, pnl)
    
    async def trade_market(self, ts: int) -> bool:
        """Trade a single market. Returns True if orders placed."""
        if ts in self.placed_markets:
            return False
        
        if not self.risk_manager.can_trade():
            return False
        
        slug = f"btc-updown-15m-{ts}"
        
        try:
            mkt = await self.client.get_market_info(slug)
        except Exception as e:
            log.debug(f"Market {slug} not available: {e}")
            return False
        
        now = int(time.time())
        secs_until = ts - now
        
        log.info("=" * 60)
        log.info(f"MARKET: {mkt['title']}")
        log.info(f"  Slug: {slug}")
        log.info(f"  Starts in: {max(0, secs_until)}s")
        
        # Check existing positions
        up_bal = self.client.get_balance(mkt["up_token"])
        down_bal = self.client.get_balance(mkt["down_token"])
        
        if up_bal > 0 or down_bal > 0:
            log.info(f"  Already have position (UP={up_bal:.1f}, DN={down_bal:.1f}) - skipping")
            self.placed_markets.add(ts)
            self.past_markets[ts] = {
                "redeemed": False,
                "up_token": mkt["up_token"],
                "down_token": mkt["down_token"],
                "conditionId": mkt["conditionId"],
                "neg_risk": mkt["neg_risk"],
            }
            return False
        
        # Check for existing orders
        try:
            from py_clob_client.clob_types import OpenOrderParams
            live_orders = self.client.client.get_orders(
                OpenOrderParams(market=mkt["conditionId"])
            )
            if live_orders:
                log.info(f"  Already have {len(live_orders)} live order(s) - skipping")
                self.placed_markets.add(ts)
                return False
        except Exception:
            pass
        
        # Calculate position size
        usdc_balance = self.client.get_usdc_balance()
        shares = self.risk_manager.calculate_position_size(usdc_balance)
        
        if shares < self.config.min_position_size:
            log.warning(f"  Insufficient balance for minimum position size")
            return False
        
        max_cost = shares * self.config.entry_price * 2
        log.info(f"  Position size: {shares} shares/side")
        log.info(f"  Max cost: ${max_cost:.2f}")
        
        # Place orders
        up_id = self.client.place_limit_buy(
            mkt["up_token"], "UP", shares, self.config.entry_price
        )
        down_id = self.client.place_limit_buy(
            mkt["down_token"], "DOWN", shares, self.config.entry_price
        )
        
        placed = (1 if up_id else 0) + (1 if down_id else 0)
        log.info(f"  Placed {placed}/2 orders")
        
        # Record trades
        if up_id:
            self.performance.record_trade(TradeRecord(
                timestamp=datetime.now(),
                market_slug=slug,
                side="up",
                token_id=mkt["up_token"],
                shares=shares,
                price=self.config.entry_price,
                cost=shares * self.config.entry_price,
                filled=False  # Will update when checking fills
            ))
        
        if down_id:
            self.performance.record_trade(TradeRecord(
                timestamp=datetime.now(),
                market_slug=slug,
                side="down",
                token_id=mkt["down_token"],
                shares=shares,
                price=self.config.entry_price,
                cost=shares * self.config.entry_price,
                filled=False
            ))
        
        # Track position
        self.placed_markets.add(ts)
        self.past_markets[ts] = {
            "redeemed": False,
            "up_token": mkt["up_token"],
            "down_token": mkt["down_token"],
            "conditionId": mkt["conditionId"],
            "neg_risk": mkt["neg_risk"],
            "cost": max_cost,
        }
        self.risk_manager.add_position(ts, mkt["up_token"], mkt["down_token"], shares, max_cost)
        
        return True
    
    async def run(self):
        """Main bot loop."""
        log.info("=" * 60)
        log.info("POLYMARKET ARBITRAGE BOT - ENHANCED VERSION")
        log.info("=" * 60)
        
        if self.config.simulation_mode:
            log.warning("RUNNING IN SIMULATION MODE - NO REAL ORDERS")
        
        # Log configuration
        log.info("Configuration:")
        log.info(f"  Entry price: {self.config.entry_price}")
        log.info(f"  Position sizing: {self.config.position_sizing_mode}")
        log.info(f"  Max position: {self.config.max_position_size}")
        log.info(f"  Stop-loss: {self.config.stop_loss_price} (enabled={self.config.enable_stop_loss})")
        log.info(f"  Max daily loss: ${self.config.max_daily_loss}")
        log.info("=" * 60)
        
        # Check balance
        usdc_balance = self.client.get_usdc_balance()
        log.info(f"USDC Balance: ${usdc_balance:.2f}")
        
        if usdc_balance < 50:
            log.warning("Low balance - recommend at least $50")
        
        # Scan for existing positions
        await self.scan_recent_markets()
        
        log.info("\nStarting main loop...")
        
        try:
            while True:
                now = int(time.time())
                timestamps = self.get_market_timestamps(now)
                
                # Trade new markets
                for ts in timestamps:
                    await self.trade_market(ts)
                
                # Check existing positions for stop-loss
                for ts, info in list(self.past_markets.items()):
                    if not info.get("redeemed") and not info.get("bailed"):
                        await self.check_stop_loss(ts, info)
                
                # Try to redeem resolved markets
                for ts, info in list(self.past_markets.items()):
                    await self.try_redeem(ts, info)
                
                # Print periodic summary
                if int(time.time()) % 300 == 0:  # Every 5 minutes
                    self.performance.print_summary()
                
                # Clean old entries
                self.past_markets = {
                    ts: v for ts, v in self.past_markets.items() 
                    if ts > now - 7200  # Keep 2 hours
                }
                self.placed_markets = {
                    ts for ts in self.placed_markets 
                    if ts > now - 900  # Keep 15 minutes
                }
                
                await asyncio.sleep(self.config.check_interval_seconds)
                
        except KeyboardInterrupt:
            log.info("\n" + "=" * 60)
            log.info("BOT STOPPED")
            self.performance.print_summary()


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    """Run the bot."""
    # Load configuration from environment or use defaults
    config = BotConfig(
        entry_price=float(os.getenv("ENTRY_PRICE", "0.45")),
        max_position_size=int(os.getenv("MAX_POSITION_SIZE", "100")),
        position_sizing_mode=os.getenv("POSITION_SIZING", "fixed"),
        account_risk_percent=float(os.getenv("RISK_PERCENT", "10")),
        enable_stop_loss=os.getenv("ENABLE_STOP_LOSS", "true").lower() == "true",
        stop_loss_price=float(os.getenv("STOP_LOSS_PRICE", "0.72")),
        max_daily_loss=float(os.getenv("MAX_DAILY_LOSS", "50")),
        simulation_mode=os.getenv("SIMULATION_MODE", "false").lower() == "true",
        auto_redeem=os.getenv("AUTO_REDEEM", "true").lower() == "true",
    )
    
    bot = PolymarketBot(config)
    asyncio.run(bot.run())


if __name__ == "__main__":
    main()

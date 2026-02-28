"""
Alert Manager - Send notifications on important events
"""
import os
from typing import Optional


class AlertManager:
    """Sends alerts for important bot events"""
    
    def __init__(self):
        self.webhook_url = os.getenv('ALERT_WEBHOOK_URL')
        self.enabled = self.webhook_url is not None
    
    def send_alert(self, message: str):
        """Send an alert message"""
        print(f"🚨 ALERT: {message}")
        
        if self.webhook_url:
            # Would send to webhook (Discord, Telegram, etc.)
            pass
    
    def send_pnl_summary(self, timeframe: str, pnl: float):
        """Send P&L summary"""
        emoji = "🟢" if pnl >= 0 else "🔴"
        self.send_alert(f"{emoji} {timeframe} P&L: ${pnl:.2f}")

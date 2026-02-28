# WebSocket Order Book Feed
"""
Real-time WebSocket order book feed with auto-reconnect
"""
import asyncio
import json
from typing import Callable, Optional
import websockets


class WebSocketBookFeed:
    """WebSocket feed for real-time order book data"""
    
    def __init__(self, endpoint: str = "wss://clob.polymarket.com/ws"):
        self.endpoint = endpoint
        self.ws = None
        self.running = False
        self.subscriptions = set()
        self.on_message: Optional[Callable] = None
        self.reconnect_delay = 5  # seconds
    
    async def connect(self):
        """Connect to WebSocket"""
        while self.running:
            try:
                self.ws = await websockets.connect(self.endpoint)
                print("WebSocket connected")
                
                # Resubscribe to previous subscriptions
                for token_id in self.subscriptions:
                    await self._subscribe(token_id)
                
                # Listen for messages
                await self._listen()
                
            except Exception as e:
                print(f"WebSocket error: {e}")
                await asyncio.sleep(self.reconnect_delay)
    
    async def _listen(self):
        """Listen for WebSocket messages"""
        try:
            async for message in self.ws:
                data = json.loads(message)
                if self.on_message:
                    self.on_message(data)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket disconnected")
    
    async def subscribe(self, token_id: str):
        """Subscribe to a token's order book"""
        self.subscriptions.add(token_id)
        if self.ws:
            await self._subscribe(token_id)
    
    async def _subscribe(self, token_id: str):
        """Send subscription message"""
        if self.ws:
            await self.ws.send(json.dumps({
                'type': 'subscribe',
                'channel': 'book',
                'token_id': token_id
            }))
    
    async def unsubscribe(self, token_id: str):
        """Unsubscribe from a token"""
        self.subscriptions.discard(token_id)
        if self.ws:
            await self.ws.send(json.dumps({
                'type': 'unsubscribe',
                'channel': 'book',
                'token_id': token_id
            }))
    
    def start(self):
        """Start the WebSocket connection"""
        self.running = True
        asyncio.create_task(self.connect())
    
    def stop(self):
        """Stop the WebSocket connection"""
        self.running = False
        if self.ws:
            asyncio.create_task(self.ws.close())

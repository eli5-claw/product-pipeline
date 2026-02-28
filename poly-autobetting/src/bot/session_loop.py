# Session Loop
"""
Session management primitives
"""
import asyncio
from typing import Optional
from contextlib import asynccontextmanager


class SessionLoop:
    """Manages the main bot session loop"""
    
    def __init__(self, interval: float = 10.0):
        self.interval = interval
        self.running = False
        self._task: Optional[asyncio.Task] = None
    
    async def start(self, callback):
        """Start the session loop"""
        self.running = True
        self._task = asyncio.create_task(self._loop(callback))
    
    async def _loop(self, callback):
        """Main loop"""
        while self.running:
            try:
                await callback()
            except Exception as e:
                print(f"Session loop error: {e}")
            
            await asyncio.sleep(self.interval)
    
    async def stop(self):
        """Stop the session loop"""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass


@asynccontextmanager
async def managed_session(interval: float = 10.0):
    """Context manager for session loop"""
    loop = SessionLoop(interval)
    try:
        yield loop
    finally:
        await loop.stop()

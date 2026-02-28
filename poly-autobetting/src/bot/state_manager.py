# State Manager
"""
State persistence and management
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class StateManager:
    """Manages bot state persistence"""
    
    def __init__(self, state_dir: str = "state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)
    
    def save(self, name: str, data: Dict[str, Any]):
        """Save state to file"""
        filepath = self.state_dir / f"{name}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def load(self, name: str) -> Optional[Dict[str, Any]]:
        """Load state from file"""
        filepath = self.state_dir / f"{name}.json"
        if not filepath.exists():
            return None
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def delete(self, name: str):
        """Delete state file"""
        filepath = self.state_dir / f"{name}.json"
        if filepath.exists():
            filepath.unlink()

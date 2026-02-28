"""
Eli5AI Publisher
Publishes threads to X/Twitter via Typefully API.
"""

import requests
from typing import List
from pathlib import Path


class TypefullyPublisher:
    """Publish threads using Typefully API."""
    
    BASE_URL = "https://api.typefully.com/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
    
    def publish_thread(self, tweets: List[str], schedule: bool = False, 
                       auto_retweet: bool = False, auto_plug: bool = False) -> dict:
        """
        Publish a thread to X via Typefully.
        
        Args:
            tweets: List of tweet texts
            schedule: Whether to schedule (requires schedule_date)
            auto_retweet: Auto-retweet after 24h
            auto_plug: Auto-plug top tweet after 3 days
        
        Returns:
            API response dict
        """
        content = "\n\n".join(tweets)
        
        payload = {
            "content": content,
            "threadify": True,  # Split by newlines into thread
            "auto_retweet": auto_retweet,
            "auto_plug": auto_plug
        }
        
        if schedule:
            # Typefully will schedule based on optimal timing
            payload["schedule"] = True
        
        response = requests.post(
            f"{self.BASE_URL}/drafts",
            headers=self.headers,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        return response.json()
    
    def get_drafts(self, limit: int = 10) -> List[dict]:
        """Get recent drafts."""
        response = requests.get(
            f"{self.BASE_URL}/drafts",
            headers=self.headers,
            params={"limit": limit},
            timeout=30
        )
        response.raise_for_status()
        return response.json().get('drafts', [])
    
    def delete_draft(self, draft_id: str) -> bool:
        """Delete a draft."""
        response = requests.delete(
            f"{self.BASE_URL}/drafts/{draft_id}",
            headers=self.headers,
            timeout=30
        )
        return response.status_code == 200

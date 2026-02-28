"""
Eli5AI Data Ingestion
Fetches stories from various sources.
"""

import requests
import feedparser
from datetime import datetime
from typing import List, Dict
from dataclasses import asdict
from ranker import Story


class DuneIngestor:
    """Fetch trending dashboards/queries from Dune Analytics."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api.dune.com/api/v1"
    
    def fetch(self, limit: int = 10) -> List[Story]:
        """Fetch trending queries."""
        # Note: Dune API requires key for most endpoints
        # This is a placeholder structure
        stories = []
        
        if not self.api_key:
            return stories
        
        try:
            headers = {"X-DUNE-API-KEY": self.api_key}
            # Fetch popular queries
            resp = requests.get(
                f"{self.base_url}/queries",
                headers=headers,
                timeout=30
            )
            data = resp.json()
            
            for item in data.get('queries', [])[:limit]:
                story = Story(
                    id=f"dune_{item.get('id')}",
                    title=item.get('name', ''),
                    summary=item.get('description', ''),
                    source='dune',
                    url=f"https://dune.com/queries/{item.get('id')}",
                    published_at=datetime.now(),  # Dune doesn't always have this
                    tags=['crypto', 'analytics'],
                    engagement_score=item.get('view_count', 0) / 1000
                )
                stories.append(story)
        
        except Exception as e:
            print(f"Dune fetch error: {e}")
        
        return stories


class ArXivIngestor:
    """Fetch recent AI/ML papers from ArXiv."""
    
    CATEGORIES = ['cs.AI', 'cs.LG', 'cs.CL', 'cs.CV']
    
    def fetch(self, limit: int = 10) -> List[Story]:
        """Fetch recent papers."""
        stories = []
        
        try:
            categories = '+OR+'.join(f'cat:{c}' for c in self.CATEGORIES)
            url = f"http://export.arxiv.org/api/query?search_query={categories}&sortBy=submittedDate&max_results={limit}"
            
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:limit]:
                # Extract simple summary (ArXiv abstracts are long)
                summary = entry.summary[:200] + "..." if len(entry.summary) > 200 else entry.summary
                
                story = Story(
                    id=f"arxiv_{entry.id.split('/')[-1]}",
                    title=entry.title,
                    summary=summary,
                    source='arxiv',
                    url=entry.link,
                    published_at=datetime(*entry.published_parsed[:6]),
                    tags=['ai', 'research', 'machine-learning'],
                    engagement_score=None
                )
                stories.append(story)
        
        except Exception as e:
            print(f"ArXiv fetch error: {e}")
        
        return stories


class GitHubIngestor:
    """Fetch trending repositories."""
    
    LANGUAGES = ['Python', 'TypeScript', 'Rust', 'Go']
    
    def fetch(self, limit: int = 10) -> List[Story]:
        """Fetch trending repos."""
        stories = []
        
        try:
            # GitHub trending doesn't have an official API
            # Using search API for recently starred repos
            headers = {"Accept": "application/vnd.github.v3+json"}
            
            for lang in self.LANGUAGES[:2]:  # Limit to avoid rate limits
                url = f"https://api.github.com/search/repositories?q=language:{lang}+created:>2024-01-01&sort=stars&order=desc&per_page=5"
                
                resp = requests.get(url, headers=headers, timeout=30)
                data = resp.json()
                
                for item in data.get('items', [])[:5]:
                    story = Story(
                        id=f"github_{item.get('id')}",
                        title=item.get('name', ''),
                        summary=item.get('description', '') or 'No description',
                        source='github',
                        url=item.get('html_url', ''),
                        published_at=datetime.now(),  # GitHub doesn't expose exact creation well
                        tags=['open-source', 'developer-tools', lang.lower()],
                        engagement_score=item.get('stargazers_count', 0) / 1000
                    )
                    stories.append(story)
        
        except Exception as e:
            print(f"GitHub fetch error: {e}")
        
        return stories[:limit]


class CryptoNewsIngestor:
    """Fetch crypto news from RSS feeds."""
    
    FEEDS = [
        'https://cointelegraph.com/rss',
        'https://coindesk.com/arc/outboundfeeds/rss/',
    ]
    
    def fetch(self, limit: int = 10) -> List[Story]:
        """Fetch from RSS feeds."""
        stories = []
        
        for feed_url in self.FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:limit]:
                    summary = entry.get('summary', '')[:200]
                    if len(entry.get('summary', '')) > 200:
                        summary += "..."
                    
                    story = Story(
                        id=f"rss_{entry.get('id', entry.link)}",
                        title=entry.title,
                        summary=summary,
                        source='rss',
                        url=entry.link,
                        published_at=datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now(),
                        tags=['crypto', 'news'],
                        engagement_score=None
                    )
                    stories.append(story)
            
            except Exception as e:
                print(f"RSS fetch error for {feed_url}: {e}")
        
        return stories[:limit]


class IngestionPipeline:
    """Orchestrates all ingestors."""
    
    def __init__(self, dune_key: str = None):
        self.ingestors = [
            ArXivIngestor(),
            GitHubIngestor(),
            CryptoNewsIngestor(),
        ]
        
        if dune_key:
            self.ingestors.append(DuneIngestor(dune_key))
    
    def fetch_all(self, limit_per_source: int = 10) -> List[Story]:
        """Fetch from all sources."""
        all_stories = []
        
        for ingestor in self.ingestors:
            try:
                stories = ingestor.fetch(limit_per_source)
                all_stories.extend(stories)
                print(f"{ingestor.__class__.__name__}: fetched {len(stories)} stories")
            except Exception as e:
                print(f"Error with {ingestor.__class__.__name__}: {e}")
        
        return all_stories

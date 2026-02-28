"""
Eli5AI Story Ranker
Ranks incoming stories by relevance, novelty, and fit for Eli5AI style.
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import json

@dataclass
class Story:
    id: str
    title: str
    summary: str
    source: str  # 'dune', 'arxiv', 'github', 'twitter', etc.
    url: str
    published_at: datetime
    tags: List[str]
    engagement_score: Optional[float] = None  # from source if available
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'source': self.source,
            'url': self.url,
            'published_at': self.published_at.isoformat(),
            'tags': self.tags,
            'engagement_score': self.engagement_score
        }


class StoryRanker:
    """Ranks stories based on Eli5AI criteria."""
    
    # Topics Eli5AI covers (in order of priority)
    PRIORITY_TOPICS = [
        'ai-agents', 'defi', 'layer2', 'bitcoin', 'ethereum',
        'crypto-infrastructure', 'ai-models', 'open-source',
        'developer-tools', 'consumer-crypto', 'memecoins'
    ]
    
    # Topics to deprioritize
    LOW_PRIORITY = ['nft', 'celebrity-coins', 'politics']
    
    def __init__(self):
        self.seen_stories = set()  # Simple dedup by URL
    
    def score_story(self, story: Story) -> float:
        """Score a story 0-100 based on fit for Eli5AI."""
        score = 50.0  # Base score
        
        # Check if already seen
        if story.url in self.seen_stories:
            return 0.0
        
        # Topic alignment (0-30 points)
        topic_score = self._score_topics(story.tags)
        score += topic_score
        
        # Source quality (0-10 points)
        score += self._score_source(story.source)
        
        # Engagement signal (0-10 points)
        if story.engagement_score:
            score += min(story.engagement_score * 10, 10)
        
        # Recency bonus (0-10 points)
        hours_old = (datetime.now() - story.published_at).total_seconds() / 3600
        if hours_old < 6:
            score += 10
        elif hours_old < 24:
            score += 5
        
        # Explainability bonus — can we explain this simply? (0-10 points)
        score += self._score_explainability(story.title, story.summary)
        
        return min(score, 100.0)
    
    def _score_topics(self, tags: List[str]) -> float:
        """Score based on topic alignment."""
        score = 0.0
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower in self.PRIORITY_TOPICS:
                idx = self.PRIORITY_TOPICS.index(tag_lower)
                score += 30 - (idx * 2)  # Higher score for higher priority
            elif tag_lower in self.LOW_PRIORITY:
                score -= 15
        return min(score, 30.0)
    
    def _score_source(self, source: str) -> float:
        """Score based on source reliability/quality."""
        scores = {
            'dune': 10,
            'github': 9,
            'arxiv': 9,
            'producthunt': 8,
            'twitter': 6,
            'rss': 7
        }
        return scores.get(source, 5)
    
    def _score_explainability(self, title: str, summary: str) -> float:
        """Estimate how well this can be explained simply."""
        text = (title + " " + summary).lower()
        
        # Good signals
        good_signals = ['what is', 'how to', 'guide', 'explained', 'introduction']
        bad_signals = ['scandal', 'lawsuit', 'drama', 'controversy', 'accused']
        
        score = 5.0  # Neutral
        for signal in good_signals:
            if signal in text:
                score += 2.5
        for signal in bad_signals:
            if signal in text:
                score -= 5
        
        return max(0, min(score, 10))
    
    def rank_stories(self, stories: List[Story], top_n: int = 5) -> List[Story]:
        """Rank stories and return top N."""
        scored = [(story, self.score_story(story)) for story in stories]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Mark top stories as seen
        for story, score in scored[:top_n]:
            if score > 0:
                self.seen_stories.add(story.url)
        
        return [story for story, score in scored[:top_n] if score > 30]
    
    def save_state(self, path: str):
        """Save seen stories to disk."""
        with open(path, 'w') as f:
            json.dump(list(self.seen_stories), f)
    
    def load_state(self, path: str):
        """Load seen stories from disk."""
        try:
            with open(path, 'r') as f:
                self.seen_stories = set(json.load(f))
        except FileNotFoundError:
            pass

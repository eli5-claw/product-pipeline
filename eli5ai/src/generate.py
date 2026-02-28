"""
Eli5AI Content Generator
Generates threads in Eli5DeFi style using LLM.
"""

import json
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Thread:
    topic: str
    tweets: List[str]
    infographic_spec: Dict  # Specification for visual renderer
    sources: List[str]
    tags: List[str]
    
    def to_x_format(self) -> List[str]:
        """Return tweets ready for X API."""
        return self.tweets
    
    def to_string(self) -> str:
        """Pretty print for debugging."""
        output = f"🧵 Thread: {self.topic}\n\n"
        for i, tweet in enumerate(self.tweets, 1):
            output += f"[{i}/{len(self.tweets)}]\n{tweet}\n\n"
        return output


class ThreadGenerator:
    """Generates Eli5AI-style threads from story data."""
    
    STYLE_PROMPT = """You are Eli5AI, an autonomous media agent that explains tech, AI, and crypto topics in a simple, accessible way.

Your style is based on @Eli5DeFi. Follow these formatting rules EXACTLY:

THREAD STRUCTURE (10 tweets max):
1. Hook: "[Topic]: [Value prop] in 30s 🧵" or interesting statement + 🧵
2. What Is: "► What is [X]?" + 1-2 sentence definition
3. How It Works: "► How it Works" + 3-5 numbered steps (❶ ❷ ❸ ❹ ❺), 1 short sentence each
4. Why It Matters: "► Why It Matters" + why retail should care
5. Numbers: Real metrics with "▸" bullets (if available, otherwise skip)
6. Ecosystem: "► Ecosystem" + categorized @mentions
7. Wrap-Up: One paragraph summary
8. Credits: "CC - @handle1 | @handle2 | @handle3"

FORMATTING:
- Use ► for headers, ▸ for bullets
- Use K/M/B for large numbers
- @mention relevant projects
- Title case headers, sentence case body
- Confident but not hype-y

Write the complete thread now."""

    def __init__(self, model_client=None):
        """
        Args:
            model_client: Callable that takes prompt and returns text
        """
        self.model_client = model_client or self._default_client
    
    def _default_client(self, prompt: str) -> str:
        """Placeholder — replace with actual LLM call."""
        raise NotImplementedError("Provide a model client (Kimi, Claude, etc.)")
    
    def generate(self, story_data: Dict) -> Thread:
        """
        Generate a thread from story data.
        
        Args:
            story_data: Dict with keys: title, summary, source, url, tags, etc.
        
        Returns:
            Thread object
        """
        prompt = self._build_prompt(story_data)
        response = self.model_client(prompt)
        
        # Parse response into tweets
        tweets = self._parse_tweets(response)
        
        # Generate infographic spec
        infographic_spec = self._generate_infographic_spec(story_data, tweets)
        
        return Thread(
            topic=story_data.get('title', 'Unknown Topic'),
            tweets=tweets,
            infographic_spec=infographic_spec,
            sources=[story_data.get('url', '')],
            tags=story_data.get('tags', [])
        )
    
    def _build_prompt(self, story_data: Dict) -> str:
        """Build the generation prompt."""
        context = f"""TOPIC: {story_data.get('title')}

SUMMARY: {story_data.get('summary')}

SOURCE: {story_data.get('source')}
URL: {story_data.get('url')}

TAGS: {', '.join(story_data.get('tags', []))}

ADDITIONAL CONTEXT:
{story_data.get('extra_context', '')}
"""
        return f"{self.STYLE_PROMPT}\n\n{context}\n\nWrite the thread:"
    
    def _parse_tweets(self, response: str) -> List[str]:
        """Parse LLM response into individual tweets (max 280 chars each)."""
        tweets = []
        
        # Split by the section headers we know
        import re
        
        # First, split by major section breaks
        sections = re.split(r'\n—\s*—\s*—\n|\n—\s*\n', response)
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Split section into tweets (max 280 chars)
            lines = section.split('\n')
            current_tweet = []
            current_len = 0
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if adding this line would exceed limit
                line_len = len(line)
                if current_len + line_len + 1 > 280 and current_tweet:
                    # Save current tweet and start new one
                    tweets.append('\n'.join(current_tweet))
                    current_tweet = [line]
                    current_len = line_len
                else:
                    current_tweet.append(line)
                    current_len += line_len + 1
            
            if current_tweet:
                tweets.append('\n'.join(current_tweet))
        
        # Clean up: merge very short tweets with next one if possible
        cleaned = []
        for tweet in tweets:
            tweet = tweet.strip()
            if len(tweet) < 50 and cleaned and len(cleaned[-1]) + len(tweet) + 1 <= 280:
                # Merge with previous
                cleaned[-1] = cleaned[-1] + '\n' + tweet
            else:
                cleaned.append(tweet)
        
        return cleaned
    
    def _generate_infographic_spec(self, story_data: Dict, tweets: List[str]) -> Dict:
        """Generate specification for the visual renderer."""
        # Extract key info from tweets
        what_is = ""
        how_it_works = []
        ecosystem = []
        
        for tweet in tweets:
            if '► What is' in tweet:
                # Extract definition (line after header)
                lines = tweet.split('\n')
                for i, line in enumerate(lines):
                    if '► What is' in line and i + 1 < len(lines):
                        what_is = lines[i + 1]
                        break
            elif '❶' in tweet or '❷' in tweet:
                # Extract step lines
                for line in tweet.split('\n'):
                    if line.strip().startswith(('❶', '❷', '❸', '❹', '❺')):
                        how_it_works.append(line.strip())
            elif '► Ecosystem' in tweet or ('▸ @' in tweet and 'CC -' not in tweet):
                for line in tweet.split('\n'):
                    if '▸ @' in line:
                        ecosystem.append(line.strip())
        
        return {
            'template': 'step_flow',  # or 'definition_card', 'ecosystem_map'
            'title': story_data.get('title', ''),
            'subtitle': what_is[:100] if what_is else story_data.get('summary', '')[:100],
            'steps': how_it_works[:5] if how_it_works else ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5'],
            'ecosystem_items': ecosystem[:8],
            'accent_color': self._pick_accent_color(story_data.get('tags', []))
        }
    
    def _pick_accent_color(self, tags: List[str]) -> str:
        """Pick accent color based on topic."""
        tag_colors = {
            'ai': '#10b981',      # Green
            'ai-agents': '#10b981',
            'ethereum': '#627eea', # Blue
            'bitcoin': '#f7931a',  # Orange
            'solana': '#9945ff',   # Purple
            'defi': '#00d4aa',     # Teal
        }
        
        for tag in tags:
            if tag in tag_colors:
                return tag_colors[tag]
        
        return '#3b82f6'  # Default blue

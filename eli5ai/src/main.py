"""
Eli5AI Main Orchestrator
Ties everything together for autonomous operation.
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path

from ingest import IngestionPipeline
from ranker import StoryRanker
from generate import ThreadGenerator
from visual import InfographicRenderer
from publish import TypefullyPublisher


class Eli5AI:
    """Autonomous media agent."""
    
    def __init__(self, config_path: str = "config/config.json"):
        self.config = self._load_config(config_path)
        self.state_dir = Path("logs")
        self.state_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.ingestor = IngestionPipeline(
            dune_key=self.config.get('dune_api_key')
        )
        self.ranker = StoryRanker()
        self.ranker.load_state(self.state_dir / "seen_stories.json")
        
        # Generator needs LLM client
        self.generator = ThreadGenerator(model_client=self._llm_client)
        self.visual = InfographicRenderer()
        
        # Publisher (Typefully)
        typefully_key = self.config.get('typefully_api_key')
        self.publisher = TypefullyPublisher(typefully_key) if typefully_key else None
    
    def _load_config(self, path: str) -> dict:
        """Load config from file or env."""
        config = {
            'dune_api_key': os.getenv('DUNE_API_KEY'),
            'x_api_key': os.getenv('X_API_KEY'),
            'x_api_secret': os.getenv('X_API_SECRET'),
            'openai_key': os.getenv('OPENAI_KEY'),
        }
        
        if Path(path).exists():
            with open(path) as f:
                file_config = json.load(f)
                config.update(file_config)
        
        return config
    
    def _llm_client(self, prompt: str) -> str:
        """Call Kimi API."""
        import requests
        
        api_key = self.config.get('kimi_api_key')
        if not api_key:
            raise ValueError("KIMI_API_KEY not set in config")
        
        response = requests.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "kimi-k2-5",
                "messages": [
                    {"role": "system", "content": "You are Eli5AI, an autonomous media agent that explains tech, AI, and crypto topics in a simple, accessible way. Follow the style guide exactly."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=60
        )
        
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    def run_cycle(self, test_mode: bool = False) -> dict:
        """
        Run one full cycle: ingest → rank → generate → render.
        
        Returns:
            Result dict with what was done
        """
        result = {
            'timestamp': datetime.now().isoformat(),
            'stories_fetched': 0,
            'stories_ranked': [],
            'thread_generated': None,
            'infographic_path': None,
            'published': False,
            'error': None
        }
        
        try:
            # 1. Ingest
            print("📡 Fetching stories...")
            stories = self.ingestor.fetch_all(limit_per_source=10)
            result['stories_fetched'] = len(stories)
            print(f"   Fetched {len(stories)} stories")
            
            # 2. Rank
            print("🎯 Ranking stories...")
            top_stories = self.ranker.rank_stories(stories, top_n=3)
            result['stories_ranked'] = [s.title for s in top_stories]
            print(f"   Top story: {top_stories[0].title if top_stories else 'None'}")
            
            if not top_stories:
                print("   No good stories found, skipping")
                return result
            
            # 3. Generate
            print("✍️  Generating thread...")
            story = top_stories[0]
            story_data = story.to_dict()
            thread = self.generator.generate(story_data)
            result['thread_generated'] = thread.to_string()
            print(f"   Generated {len(thread.tweets)} tweets")
            
            # 4. Render visual
            print("🎨 Rendering infographic...")
            infographic_path = self.visual.render(
                thread.infographic_spec,
                filename=f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            result['infographic_path'] = infographic_path
            print(f"   Saved to {infographic_path}")
            
            # 5. Publish (or save for review)
            if test_mode:
                print("🧪 TEST MODE: Not publishing")
                # Save to file for review
                self._save_for_review(thread, infographic_path)
            elif self.publisher and self.config.get('publishing', {}).get('use_typefully'):
                print("📤 Publishing via Typefully...")
                try:
                    result = self.publisher.publish_thread(
                        thread.tweets,
                        schedule=True,  # Let Typefully optimize timing
                        auto_retweet=False,
                        auto_plug=False
                    )
                    print(f"   Published! Draft ID: {result.get('id')}")
                    result['published'] = True
                except Exception as e:
                    print(f"   Publish failed: {e}")
                    self._save_for_review(thread, infographic_path)
            else:
                print("⚠️  No publisher configured, saving for review")
                self._save_for_review(thread, infographic_path)
            
            # Save state
            self.ranker.save_state(self.state_dir / "seen_stories.json")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"❌ Error: {e}")
        
        # Log result
        self._log_result(result)
        
        return result
    
    def _save_for_review(self, thread, infographic_path: str):
        """Save thread to review queue."""
        review_path = self.state_dir / "review_queue.json"
        
        queue = []
        if review_path.exists():
            with open(review_path) as f:
                queue = json.load(f)
        
        queue.append({
            'timestamp': datetime.now().isoformat(),
            'topic': thread.topic,
            'tweets': thread.tweets,
            'infographic': infographic_path,
            'sources': thread.sources
        })
        
        with open(review_path, 'w') as f:
            json.dump(queue, f, indent=2)
        
        print(f"   Saved to review queue ({len(queue)} pending)")
    
    def _log_result(self, result: dict):
        """Log cycle result."""
        log_path = self.state_dir / "cycle_log.jsonl"
        with open(log_path, 'a') as f:
            f.write(json.dumps(result) + '\n')


def main():
    parser = argparse.ArgumentParser(description='Eli5AI Autonomous Media Agent')
    parser.add_argument('--test', action='store_true', help='Run in test mode (no publishing)')
    parser.add_argument('--daemon', action='store_true', help='Run continuously')
    parser.add_argument('--interval', type=int, default=3600, help='Cycle interval in seconds (daemon mode)')
    args = parser.parse_args()
    
    agent = Eli5AI()
    
    if args.daemon:
        import time
        print(f"🤖 Eli5AI daemon starting (interval: {args.interval}s)")
        while True:
            agent.run_cycle(test_mode=args.test)
            print(f"⏳ Sleeping {args.interval}s...\n")
            time.sleep(args.interval)
    else:
        agent.run_cycle(test_mode=args.test)


if __name__ == "__main__":
    main()

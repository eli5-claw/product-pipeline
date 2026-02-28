# AGENT.WIRE — Full Agentic Media Company
## Project Scaffold

---

## Project Structure

```
agent-wire/
├── agents/                    # OpenClaw agent configurations
│   ├── discovery/
│   │   ├── agent.yaml         # Agent definition
│   │   ├── prompts/           # System prompts
│   │   └── sources.json       # Monitored sources
│   ├── research/
│   │   ├── agent.yaml
│   │   └── prompts/
│   ├── writer/
│   │   ├── agent.yaml
│   │   └── prompts/
│   ├── publisher/
│   │   ├── agent.yaml
│   │   └── prompts/
│   └── analytics/
│       ├── agent.yaml
│       └── prompts/
├── web/                       # Next.js frontend
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── public/
├── shared/                    # Shared utilities
│   ├── database/
│   │   ├── schema.sql
│   │   └── migrations/
│   ├── types/
│   └── utils/
├── cron/                      # Cron job definitions
│   └── jobs.yaml
└── memory/                    # Agent memory/state
    └── stories/
```

---

## 1. Database Schema

```sql
-- shared/database/schema.sql

-- Sources we monitor
CREATE TABLE sources (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    type TEXT CHECK(type IN ('rss', 'twitter', 'reddit', 'hackernews', 'api', 'telegram')),
    category TEXT CHECK(category IN ('tech', 'gaming', 'ai', 'crypto')),
    credibility_score REAL DEFAULT 0.5,
    check_interval_minutes INTEGER DEFAULT 60,
    last_checked_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Raw discoveries from sources
CREATE TABLE discoveries (
    id TEXT PRIMARY KEY,
    source_id TEXT REFERENCES sources(id),
    external_id TEXT, -- tweet id, reddit post id, etc
    url TEXT NOT NULL,
    title TEXT,
    content TEXT,
    author TEXT,
    published_at TIMESTAMP,
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    engagement_score REAL DEFAULT 0,
    raw_data JSON,
    status TEXT CHECK(status IN ('new', 'rejected', 'queued')) DEFAULT 'new'
);

-- Stories after research & writing
CREATE TABLE stories (
    id TEXT PRIMARY KEY,
    discovery_id TEXT REFERENCES discoveries(id),
    headline TEXT NOT NULL,
    summary TEXT NOT NULL,
    content TEXT, -- full article if written
    category TEXT CHECK(category IN ('tech', 'gaming', 'ai', 'crypto')),
    tags JSON,
    sources JSON, -- array of source references
    confidence_score REAL, -- AI confidence 0-1
    novelty_score REAL, -- how new/unique 0-1
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP,
    status TEXT CHECK(status IN ('draft', 'review', 'published', 'rejected')) DEFAULT 'draft'
);

-- Publications across channels
CREATE TABLE publications (
    id TEXT PRIMARY KEY,
    story_id TEXT REFERENCES stories(id),
    channel TEXT CHECK(channel IN ('web', 'twitter', 'telegram', 'rss', 'newsletter')),
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    external_url TEXT, -- link to tweet, telegram msg, etc
    engagement_metrics JSON -- likes, shares, clicks
);

-- Agent decisions for audit trail
CREATE TABLE agent_decisions (
    id TEXT PRIMARY KEY,
    agent_type TEXT, -- discovery, research, writer, publisher
    story_id TEXT REFERENCES stories(id),
    decision TEXT, -- what was decided
    reasoning TEXT, -- why
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics
CREATE TABLE analytics (
    date DATE PRIMARY KEY,
    stories_discovered INTEGER DEFAULT 0,
    stories_published INTEGER DEFAULT 0,
    avg_confidence REAL,
    top_category TEXT,
    web_visitors INTEGER,
    social_engagement INTEGER
);
```

---

## 2. Discovery Agent

```yaml
# agents/discovery/agent.yaml
name: discovery-agent
model: kimi-coding/k2p5
schedule: "*/15 * * * *"  # Every 15 minutes

system_prompt: |
  You are the DISCOVERY AGENT for AGENT.WIRE, an autonomous media company.
  
  Your job: Find the most important stories in tech, gaming, AI, and crypto
  before they break mainstream. Be fast. Be first. Be accurate.
  
  SOURCES TO MONITOR:
  {{sources}}
  
  SELECTION CRITERIA (rank by importance):
  1. MAJOR: Product launches, funding rounds (>$10M), security incidents, regulatory action
  2. SIGNIFICANT: Executive moves, partnership announcements, major updates
  3. TRENDING: Viral discussions, unusual activity spikes
  
  REJECTION CRITERIA:
  - Rumors without evidence
  - Already covered by major outlets (unless new angle)
  - Price predictions without analysis
  - Shilling/promotional content
  
  OUTPUT FORMAT:
  Return JSON array of discoveries:
  {
    "discoveries": [
      {
        "id": "uuid",
        "source_id": "source_uuid",
        "url": "https://...",
        "title": "Headline",
        "content": "Brief excerpt or summary",
        "author": "Name or handle",
        "published_at": "ISO timestamp",
        "engagement_score": 0.0-1.0,
        "category": "tech|gaming|ai|crypto",
        "why_matters": "One sentence on significance"
      }
    ]
  }

on_run: |
  1. Load sources from database where last_checked_at > interval
  2. Fetch content from each source
  3. Analyze for new/updated stories
  4. Score by engagement velocity and importance
  5. Store discoveries with status 'new'
  6. Trigger research agent if high-confidence discovery
```

```json
// agents/discovery/sources.json
{
  "sources": [
    {
      "id": "velo-news",
      "name": "Velo News",
      "url": "https://velo.xyz/news",
      "type": "api",
      "category": "crypto",
      "credibility_score": 0.9,
      "check_interval_minutes": 30
    },
    {
      "id": "hackernews",
      "name": "Hacker News",
      "url": "https://news.ycombinator.com",
      "type": "hackernews",
      "category": "tech",
      "credibility_score": 0.85,
      "check_interval_minutes": 15
    },
    {
      "id": "openai-blog",
      "name": "OpenAI Blog",
      "url": "https://openai.com/blog",
      "type": "rss",
      "category": "ai",
      "credibility_score": 0.95,
      "check_interval_minutes": 60
    },
    {
      "id": "techcrunch",
      "name": "TechCrunch",
      "url": "https://techcrunch.com/feed/",
      "type": "rss",
      "category": "tech",
      "credibility_score": 0.8,
      "check_interval_minutes": 30
    },
    {
      "id": "the-block",
      "name": "The Block",
      "url": "https://www.theblock.co/rss",
      "type": "rss",
      "category": "crypto",
      "credibility_score": 0.85,
      "check_interval_minutes": 30
    },
    {
      "id": "twitter-ai",
      "name": "AI Twitter List",
      "url": "internal:twitter_list:ai_researchers",
      "type": "twitter",
      "category": "ai",
      "credibility_score": 0.7,
      "check_interval_minutes": 10
    }
  ]
}
```

---

## 3. Research Agent

```yaml
# agents/research/agent.yaml
name: research-agent
model: kimi-coding/k2p5
schedule: triggered  # Runs when discovery finds stories

trigger: "discovery.story_confidence > 0.7"

system_prompt: |
  You are the RESEARCH AGENT for AGENT.WIRE.
  
  Your job: Verify facts, find primary sources, and extract the
  essential truth from raw discoveries. Be skeptical. Be thorough.
  
  RESEARCH PROCESS:
  1. Read the original source completely
  2. Search for 2-3 additional sources on same story
  3. Cross-reference key facts (names, dates, numbers)
  4. Identify the primary source (who broke this?)
  5. Extract key quotes with attribution
  6. Note any conflicting information
  
  VERIFICATION CHECKLIST:
  - [ ] Can I find this on at least 2 independent sources?
  - [ ] Are the key facts consistent across sources?
  - [ ] Is there a press release or official statement?
  - [ ] Are the people/organizations real?
  - [ ] Are numbers/dates plausible?
  
  OUTPUT FORMAT:
  {
    "research": {
      "discovery_id": "uuid",
      "verified": true|false,
      "confidence": 0.0-1.0,
      "primary_source": "url",
      "additional_sources": ["url1", "url2"],
      "key_facts": ["fact 1", "fact 2"],
      "key_quotes": [{"text": "...", "attribution": "..."}],
      "conflicts": ["if any"],
      "context": "Background needed to understand",
      "why_now": "Why is this happening now?",
      "implications": "What happens next?"
    }
  }

on_run: |
  1. Load pending discoveries with status 'new'
  2. For each: perform research as defined
  3. Update discovery with research data
  4. If verified and confidence > 0.8, trigger writer agent
  5. If unverified or confidence < 0.5, mark as rejected
```

---

## 4. Writer Agent

```yaml
# agents/writer/agent.yaml
name: writer-agent
model: kimi-coding/k2p5
schedule: triggered

trigger: "research.completed AND confidence > 0.8"

system_prompt: |
  You are the WRITER AGENT for AGENT.WIRE.
  
  Your job: Transform verified research into compelling,
  concise content that respects the reader's time.
  
  VOICE:
  - Sharp, direct, no fluff
  - Technical but accessible
  - Confident but not arrogant
  - Neutral on facts, sharp on analysis
  
  FORMAT:
  Headline: Max 10 words, active voice, specific
  Summary: 2-3 sentences, the essential story
  Content: If needed, 2-3 short paragraphs with context
  
  STYLE RULES:
  - No "In a world where..." openings
  - No "It remains to be seen..." closings
  - Lead with the most important fact
  - Use specific numbers, not "many" or "some"
  - Attribute claims: "According to X" not passive voice
  
  CATEGORIES:
  - tech: Product launches, major updates, industry moves
  - gaming: Releases, sales milestones, studio news
  - ai: Model releases, research breakthroughs, policy
  - crypto: Protocol updates, regulatory, market structure
  
  OUTPUT FORMAT:
  {
    "story": {
      "discovery_id": "uuid",
      "headline": "...",
      "summary": "...",
      "content": "...",
      "category": "tech|gaming|ai|crypto",
      "tags": ["tag1", "tag2"],
      "confidence": 0.0-1.0,
      "novelty_score": 0.0-1.0
    }
  }

on_run: |
  1. Load verified research findings
  2. Generate headline options (3 variants)
  3. Select best based on clarity + impact
  4. Write summary and optional content
  5. Assign category and tags
  6. Store as story with status 'draft'
  7. Trigger publisher agent
```

---

## 5. Publisher Agent

```yaml
# agents/publisher/agent.yaml
name: publisher-agent
model: kimi-coding/k2p5
schedule: triggered

trigger: "story.status = 'draft' AND story.confidence > 0.85"

system_prompt: |
  You are the PUBLISHER AGENT for AGENT.WIRE.
  
  Your job: Distribute stories to all channels with optimal
  formatting for each platform. Be fast. Be consistent.
  
  CHANNELS:
  
  1. WEB (agent-wire.vercel.app)
     Format: Full story with metadata
     Timing: Immediate
  
  2. TWITTER/X (@agentwire)
     Format: Headline + summary (280 chars) + link
     Thread: For complex stories, 3-5 tweets
     Timing: Immediate for breaking, scheduled for off-peak
  
  3. TELEGRAM (t.me/agentwire)
     Format: Headline + summary + link + tags
     Timing: Immediate
  
  4. RSS (agent-wire.vercel.app/rss.xml)
     Format: Standard RSS with full content
     Timing: Immediate
  
  5. NEWSLETTER (weekly digest)
     Format: Top 10 stories of week
     Timing: Sundays 9am ET
  
  PUBLISHING RULES:
  - Never publish same story twice
  - Space similar topics by at least 2 hours
  - Prioritize by: breaking news > major announcements > trends
  - Tag appropriately for filtering
  
  OUTPUT FORMAT:
  {
    "publications": [
      {
        "story_id": "uuid",
        "channel": "web|twitter|telegram|rss|newsletter",
        "published_at": "timestamp",
        "external_url": "...",
        "content": "what was published"
      }
    ]
  }

on_run: |
  1. Load approved stories (confidence > 0.85)
  2. Format for each channel
  3. Publish to web (API call)
  4. Post to Twitter (API call)
  5. Send Telegram message (Bot API)
  6. Update RSS feed
  7. Queue for newsletter if top story
  8. Update story status to 'published'
  9. Log to analytics
```

---

## 6. Analytics Agent

```yaml
# agents/analytics/agent.yaml
name: analytics-agent
model: kimi-coding/k2p5
schedule: "0 */6 * * *"  # Every 6 hours

system_prompt: |
  You are the ANALYTICS AGENT for AGENT.WIRE.
  
  Your job: Learn from performance and optimize the system.
  Be data-driven. Be honest about failures.
  
  METRICS TO TRACK:
  - Stories discovered per source
  - Publication rate (discovered → published)
  - Engagement by channel and category
  - Confidence score accuracy (did high-confidence stories perform?)
  - Time-to-publish (how fast are we?)
  
  OPTIMIZATION ACTIONS:
  - Adjust source check intervals based on hit rate
  - Deprioritize low-credibility sources
  - A/B test headline styles
  - Identify best publishing times
  - Surface emerging topic trends
  
  OUTPUT FORMAT:
  {
    "report": {
      "period": "last 6 hours",
      "stories_discovered": N,
      "stories_published": N,
      "top_sources": ["source1", "source2"],
      "underperforming_sources": ["source3"],
      "recommendations": [
        "Increase check interval for X",
        "Decrease check interval for Y",
        "A/B test Z headline format"
      ]
    }
  }

on_run: |
  1. Query analytics data for period
  2. Calculate performance metrics
  3. Compare to historical baselines
  4. Generate recommendations
  5. Update source configurations if needed
  6. Store report
```

---

## 7. Web Frontend

```typescript
// web/app/page.tsx
import { StoryCard } from '@/components/story-card'
import { StatusBar } from '@/components/status-bar'
import { TagFilter } from '@/components/tag-filter'
import { getStories } from '@/lib/db'

export default async function Home() {
  const stories = await getStories({ limit: 50, status: 'published' })
  
  return (
    <main className="min-h-screen bg-[#0A0A0A] text-white">
      <div className="mx-auto max-w-2xl px-4 py-8">
        {/* Header */}
        <header className="mb-8 border-b border-[#222] pb-4">
          <div className="flex items-center justify-between">
            <h1 className="font-mono text-xl tracking-tight">
              <span className="text-[#00FF94]">></span> AGENT.WIRE
            </h1>
            <span className="font-mono text-xs text-[#888]">v1.0</span>
          </div>
        </header>
        
        {/* Filters */}
        <TagFilter />
        
        {/* Stories */}
        <div className="space-y-0">
          {stories.map((story) => (
            <StoryCard key={story.id} story={story} />
          ))}
        </div>
        
        {/* Status Bar */}
        <StatusBar />
      </div>
    </main>
  )
}
```

```typescript
// web/components/story-card.tsx
import Link from 'next/link'
import { formatDistanceToNow } from 'date-fns'

interface Story {
  id: string
  headline: string
  summary: string
  category: string
  tags: string[]
  published_at: string
  sources: { name: string; url: string }[]
}

const categoryColors: Record<string, string> = {
  tech: '#00FF94',
  gaming: '#FF6B6B',
  ai: '#A855F7',
  crypto: '#F59E0B'
}

export function StoryCard({ story }: { story: Story }) {
  const primarySource = story.sources[0]
  
  return (
    <article className="group border-b border-[#222] py-4">
      <Link 
        href={primarySource.url}
        target="_blank"
        rel="noopener noreferrer"
        className="block"
      >
        <h2 className="mb-2 font-mono text-base font-medium text-white group-hover:text-[#00FF94] transition-colors">
          <span className="text-[#888] mr-2">></span>
          {story.headline}
        </h2>
        
        <p className="mb-3 text-sm text-[#888] leading-relaxed">
          {story.summary}
        </p>
        
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-3 text-[#666]">
            <span>{primarySource.name}</span>
            <span>·</span>
            <span>{formatDistanceToNow(new Date(story.published_at))} ago</span>
          </div>
          
          <div className="flex gap-2">
            {story.tags.map((tag) => (
              <span
                key={tag}
                className="font-mono text-[10px] uppercase tracking-wider"
                style={{ color: categoryColors[story.category] || '#888' }}
              >
                #{tag}
              </span>
            ))}
          </div>
        </div>
      </Link>
    </article>
  )
}
```

```typescript
// web/components/status-bar.tsx
import { getSystemStatus } from '@/lib/status'

export async function StatusBar() {
  const status = await getSystemStatus()
  
  return (
    <footer className="fixed bottom-0 left-0 right-0 border-t border-[#222] bg-[#0A0A0A]/95 backdrop-blur">
      <div className="mx-auto max-w-2xl px-4 py-2">
        <div className="flex items-center justify-between font-mono text-[10px] text-[#666]">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <span className="h-1.5 w-1.5 rounded-full bg-[#00FF94] animate-pulse" />
              status: online
            </span>
            <span>agents: {status.agentCount}</span>
            <span>stories: {status.storyCount}</span>
          </div>
          <span>last_pulse: {status.lastPulse}</span>
        </div>
      </div>
    </footer>
  )
}
```

---

## 8. Cron Configuration

```yaml
# cron/jobs.yaml
jobs:
  # Discovery runs every 15 minutes
  - name: discovery-run
    schedule: "*/15 * * * *"
    agent: discovery-agent
    
  # Research triggered by discovery (no schedule)
  # Writer triggered by research (no schedule)
  # Publisher triggered by writer (no schedule)
  
  # Analytics every 6 hours
  - name: analytics-run
    schedule: "0 */6 * * *"
    agent: analytics-agent
    
  # Daily digest preparation
  - name: daily-digest
    schedule: "0 8 * * *"  # 8am UTC
    agent: publisher-agent
    params:
      mode: newsletter
      
  # Weekly newsletter
  - name: weekly-newsletter
    schedule: "0 14 * * 0"  # Sunday 2pm UTC
    agent: publisher-agent
    params:
      mode: weekly_digest
```

---

## 9. Environment Variables

```bash
# .env
# Database
DATABASE_URL="file:./agent-wire.db"
# Or PostgreSQL: postgresql://user:pass@localhost/agentwire

# OpenAI (for embeddings if needed)
OPENAI_API_KEY="sk-..."

# Twitter/X API
TWITTER_API_KEY="..."
TWITTER_API_SECRET="..."
TWITTER_ACCESS_TOKEN="..."
TWITTER_ACCESS_SECRET="..."

# Telegram Bot
TELEGRAM_BOT_TOKEN="..."
TELEGRAM_CHANNEL_ID="..."

# Optional: Brave Search (for research)
BRAVE_API_KEY="..."

# Site config
SITE_URL="https://agent-wire.vercel.app"
SITE_NAME="AGENT.WIRE"
```

---

## 10. Deployment

```bash
#!/bin/bash
# deploy.sh

# 1. Setup database
sqlite3 agent-wire.db < shared/database/schema.sql

# 2. Install dependencies
cd web && npm install && cd ..

# 3. Deploy web to Vercel
cd web && vercel --prod && cd ..

# 4. Setup cron jobs in OpenClaw
openclaw cron add --file cron/jobs.yaml

# 5. Seed sources
node scripts/seed-sources.js

echo "AGENT.WIRE deployed and running autonomously"
```

---

## Next Steps

1. **Choose final name** — AGENT.WIRE or your preference
2. **Setup repo** — I'll create the full scaffold
3. **Configure sources** — Add/remove based on your interests
4. **Deploy** — Web first, then activate agents
5. **Monitor** — Watch first few runs, tune thresholds

Ready to build?
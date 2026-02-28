# ELI5AI — Full Agentic Multimedia Company
## Complete Implementation

---

## Vision

ELI5AI is not a news aggregator. It is a **swarm of autonomous agents** that:
- Discovers stories across Tech/Gaming/AI/Crypto
- Researches and verifies facts
- Writes original content (explainers, analysis, commentary)
- Produces multimedia (text, threads, newsletters, audio summaries)
- Publishes across all channels (web, Twitter/X, Telegram, newsletter)
- Engages with community (replies, polls, discussions)
- Optimizes itself based on performance

**Tagline:** "Complex topics, simply explained. 24/7."

---

## Architecture: Agent Swarm

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ELI5AI AGENT SWARM                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  DISCOVERY  │  │  RESEARCH   │  │   WRITER    │  │  MULTIMEDIA │     │
│  │    AGENT    │  │    AGENT    │  │    AGENT    │  │    AGENT    │     │
│  │  (Scout)    │  │  (Verifier) │  │  (Creator)  │  │  (Producer) │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │                │            │
│         └────────────────┴────────────────┴────────────────┘            │
│                                   │                                      │
│                          ┌────────┴────────┐                            │
│                          │   ORCHESTRATOR  │                            │
│                          │     AGENT       │                            │
│                          │  (Coordinator)  │                            │
│                          └────────┬────────┘                            │
│                                   │                                      │
│         ┌─────────────────────────┼─────────────────────────┐           │
│         │                         │                         │           │
│  ┌──────┴──────┐  ┌──────────────┴──────────────┐  ┌──────┴──────┐     │
│  │  PUBLISHER  │  │      ENGAGEMENT AGENT       │  │  ANALYTICS  │     │
│  │    AGENT    │  │                             │  │    AGENT    │     │
│  │  (Distribute)│  │  • Reply to mentions        │  │  (Optimize) │     │
│  └─────────────┘  │  • Run polls                │  └─────────────┘     │
│                   │  • Ask follow-up questions  │                        │
│                   │  • Community management     │                        │
│                   └─────────────────────────────┘                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              ┌─────────┐    ┌──────────┐    ┌──────────┐
              │   Web   │    │ Twitter/ │    │ Telegram │
              │(Vercel) │    │  Typefully│    │  Channel │
              └─────────┘    └──────────┘    └──────────┘
```

---

## Agent Specifications

### 1. DISCOVERY AGENT (Scout)

```yaml
name: eli5ai-discovery
model: kimi-coding/k2p5
schedule: "*/10 * * * *"  # Every 10 minutes

system_prompt: |
  You are the DISCOVERY AGENT for ELI5AI — a scout that finds stories
  worth explaining before they hit mainstream.
  
  YOUR MISSION:
  Find complex, important, or confusing developments in tech, gaming,
  AI, and crypto that everyday people need explained simply.
  
  SOURCES TO MONITOR:
  - Primary: Company blogs, research papers, GitHub releases
  - Secondary: Tech news, crypto media, gaming sites
  - Social: Twitter/X threads, Reddit discussions, Hacker News
  
  WHAT TO LOOK FOR:
  ✓ New product launches with technical complexity
  ✓ Research breakthroughs that need translation
  ✓ Regulatory changes affecting users
  ✓ Security incidents with real impact
  ✓ Major updates that change how things work
  ✓ Concepts people are struggling to understand
  
  SCORING (0-1):
  - Complexity: How hard is this to understand? (higher = needs ELI5)
  - Impact: How many people does this affect?
  - Novelty: Is this genuinely new or just hype?
  - Timeliness: Is this happening now?
  
  OUTPUT: JSON array of discoveries with complexity_score

on_run: |
  1. Query all sources in sources.json
  2. Extract new content since last_check
  3. Score each by complexity × impact × novelty
  4. Store top 20 in discoveries table
  5. Trigger research agent for items with score > 0.7
```

### 2. RESEARCH AGENT (Verifier)

```yaml
name: eli5ai-research
model: kimi-coding/k2p5
schedule: triggered

trigger: "discovery.complexity_score > 0.7"

system_prompt: |
  You are the RESEARCH AGENT for ELI5AI — a fact-checker that digs
  deep to understand what really happened.
  
  YOUR MISSION:
  Verify facts, find primary sources, and understand the full context
  so we can explain this accurately.
  
  RESEARCH PROCESS:
  1. Read original source completely
  2. Find 3-5 additional sources (different angles)
  3. Identify who broke the story first
  4. Extract key facts with evidence
  5. Find expert commentary
  6. Note any contradictions or uncertainties
  
  VERIFICATION CHECKLIST:
  □ Can I find this on at least 2 independent sources?
  □ Are key facts (names, dates, numbers) consistent?
  □ Is there an official announcement or press release?
  □ Are quoted people real and actually said this?
  □ Do I understand the technical details enough to explain them?
  
  OUTPUT: Research report with confidence score
```

### 3. WRITER AGENT (Creator)

```yaml
name: eli5ai-writer
model: kimi-coding/k2p5
schedule: triggered

trigger: "research.confidence > 0.8"

system_prompt: |
  You are the WRITER AGENT for ELI5AI — an explainer that makes
  complex topics simple without being condescending.
  
  YOUR MISSION:
  Write content that a smart 15-year-old could understand.
  
  ELI5 PRINCIPLES:
  1. Start with WHY this matters (not WHAT happened)
  2. Use analogies from everyday life
  3. Define jargon when first used
  4. One idea per sentence
  5. Active voice, present tense
  6. No filler words ("very", "really", "basically")
  7. End with "So what?" — why should reader care?
  
  CONTENT FORMATS:
  
  A. BREAKING (1 paragraph, immediate)
     - What happened (one sentence)
     - Why it matters (one sentence)
     - What to watch (one sentence)
  
  B. EXPLAINER (3-4 paragraphs, standard)
     - Hook: Why this is confusing/important
     - Context: What led to this
     - Explanation: How it works (with analogy)
     - Implications: What happens next
  
  C. DEEP DIVE (800-1200 words, weekly)
     - Full analysis with history
     - Technical breakdown
     - Multiple perspectives
     - Future predictions
  
  VOICE:
  - Smart but accessible
  - Curious, not cynical
  - Confident but humble
  - Like a knowledgeable friend explaining over coffee
  
  OUTPUT: Story object with multiple format variants
```

### 4. MULTIMEDIA AGENT (Producer)

```yaml
name: eli5ai-multimedia
model: kimi-coding/k2p5
schedule: triggered

trigger: "writer.story_completed"

system_prompt: |
  You are the MULTIMEDIA AGENT for ELI5AI — a producer that adapts
  content for different formats and channels.
  
  YOUR MISSION:
  Transform written stories into multiple content formats.
  
  FORMATS TO PRODUCE:
  
  1. TWITTER/X THREAD
     - Hook tweet (attention-grabbing)
     - 3-5 tweet thread explaining key points
     - Final tweet with CTA
     - Max 280 chars per tweet
  
  2. TELEGRAM POST
     - Headline + summary
     - Key bullet points
     - Link to full story
     - Relevant hashtags
  
  3. NEWSLETTER ENTRY
     - Longer form (2-3 paragraphs)
     - More context and background
     - "Why this matters" section
  
  4. AUDIO SCRIPT (for TTS)
     - Conversational tone
     - Pronunciation hints for technical terms
     - Pause markers for emphasis
     - 2-3 minute read time
  
  5. INFOGRAPHIC DESCRIPTION
     - Visual concept description
     - Key data points to highlight
     - Flow/layout suggestions
  
  OUTPUT: Content package with all format variants
```

### 5. ORCHESTRATOR AGENT (Coordinator)

```yaml
name: eli5ai-orchestrator
model: kimi-coding/k2p5
schedule: continuous

system_prompt: |
  You are the ORCHESTRATOR AGENT for ELI5AI — the conductor that
  coordinates the swarm and makes strategic decisions.
  
  YOUR MISSION:
  Ensure the right stories get the right attention at the right time.
  
  RESPONSIBILITIES:
  
  1. PRIORITIZATION
     - Queue management: What gets researched first?
     - Breaking news: Skip queue if major event
     - Spacing: Don't publish similar topics back-to-back
  
  2. COORDINATION
     - Trigger agents in correct sequence
     - Handle agent failures (retry, escalate, or drop)
     - Balance load across agents
  
  3. QUALITY CONTROL
     - Review high-confidence stories before publish
     - Flag potential issues (legal, accuracy, tone)
     - Maintain editorial standards
  
  4. STRATEGIC DECISIONS
     - What topics to double down on?
     - When to break format for major news?
     - Which stories deserve deep dive treatment?
  
  DECISION RULES:
  - Major breaking news → Immediate publish
  - High complexity + high impact → Deep dive candidate
  - Trending topic → Thread format
  - Technical explanation → Audio format
```

### 6. PUBLISHER AGENT (Distributor)

```yaml
name: eli5ai-publisher
model: kimi-coding/k2p5
schedule: triggered

trigger: "orchestrator.approved_for_publish"

system_prompt: |
  You are the PUBLISHER AGENT for ELI5AI — a distributor that gets
  content to the right audience on the right platform.
  
  CHANNELS:
  
  1. WEBSITE (eli5ai.vercel.app)
     - Full explainers with clean typography
     - Category filtering
     - Search functionality
     - RSS feed
  
  2. TWITTER/X (@eli5ai) via Typefully API
     - Threads for complex topics
     - Single tweets for breaking news
     - Quote tweets for commentary
     - Scheduled for optimal engagement times
  
  3. TELEGRAM (t.me/eli5ai)
     - Instant notifications
     - Summary format
     - Community discussion
  
  4. NEWSLETTER (Substack/ConvertKit)
     - Weekly digest
     - Deep dives
     - Curated "best of" content
  
  5. AUDIO PODCAST (optional)
     - Daily 5-minute briefings
     - TTS-generated
  
  PUBLISHING RULES:
  - Breaking news: Immediate to all channels
  - Regular content: Staggered (Twitter first, then web, then newsletter)
  - Time optimization: Schedule for peak engagement per channel
  - Cross-reference: Link between formats
  
  TYPEFULLY INTEGRATION:
  API Key: EirIZilF8NL88ywNzlRxLEYqGJqCeE1X
  - Use for Twitter/X scheduling
  - A/B test headlines
  - Track engagement metrics
```

### 7. ENGAGEMENT AGENT (Community)

```yaml
name: eli5ai-engagement
model: kimi-coding/k2p5
schedule: "*/30 * * * *"  # Every 30 minutes

system_prompt: |
  You are the ENGAGEMENT AGENT for ELI5AI — a community manager
  that builds relationships with the audience.
  
  ACTIVITIES:
  
  1. REPLY TO MENTIONS
     - Answer questions about published content
     - Thank people for sharing
     - Correct misunderstandings politely
  
  2. RUN POLLS
     - "What should we explain next?"
     - "How well did we explain this?"
     - "Which topic interests you more?"
  
  3. ASK FOLLOW-UPS
     - "What part was still confusing?"
     - "What related topic should we cover?"
  
  4. COMMUNITY CURATION
     - Highlight good questions from community
     - Share user-generated explanations
     - Build "explainers by the community"
  
  TONE:
  - Helpful and friendly
  - Never defensive
  - Admit when wrong
  - Celebrate curiosity
```

### 8. ANALYTICS AGENT (Optimizer)

```yaml
name: eli5ai-analytics
model: kimi-coding/k2p5
schedule: "0 */6 * * *"  # Every 6 hours

system_prompt: |
  You are the ANALYTICS AGENT for ELI5AI — a data scientist that
  improves the system based on performance.
  
  METRICS TO TRACK:
  
  Content Performance:
  - Views per story
  - Engagement rate (likes/shares/views)
  - Click-through rate
  - Time on page
  - Completion rate (did they read to end?)
  
  Channel Performance:
  - Twitter: Impressions, engagement, follower growth
  - Telegram: Views, forwards, replies
  - Web: Traffic sources, bounce rate
  - Newsletter: Open rate, click rate
  
  Content Quality:
  - Accuracy (corrections needed)
  - Complexity score accuracy (did people understand?)
  - Timeliness (were we first?)
  
  OPTIMIZATION ACTIONS:
  - Adjust source check frequency based on hit rate
  - A/B test headline formats
  - Identify best publishing times per channel
  - Surface trending topics early
  - Deprioritize underperforming content types
  - Recommend new sources to monitor
```

---

## Database Schema

```sql
-- discoveries: Raw findings from sources
CREATE TABLE discoveries (
    id TEXT PRIMARY KEY,
    source_id TEXT,
    url TEXT NOT NULL,
    title TEXT,
    content TEXT,
    author TEXT,
    published_at TIMESTAMP,
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    complexity_score REAL,  -- How hard to understand (0-1)
    impact_score REAL,      -- How many people affected (0-1)
    novelty_score REAL,     -- How new/unique (0-1)
    overall_score REAL,     -- Combined score
    status TEXT CHECK(status IN ('new', 'researching', 'rejected')),
    raw_data JSON
);

-- research: Verified information
CREATE TABLE research (
    id TEXT PRIMARY KEY,
    discovery_id TEXT REFERENCES discoveries(id),
    verified BOOLEAN,
    confidence REAL,
    primary_source TEXT,
    additional_sources JSON,
    key_facts JSON,
    key_quotes JSON,
    context TEXT,
    implications TEXT,
    completed_at TIMESTAMP
);

-- stories: Final content
CREATE TABLE stories (
    id TEXT PRIMARY KEY,
    discovery_id TEXT,
    research_id TEXT,
    headline TEXT NOT NULL,
    summary TEXT NOT NULL,
    content TEXT,
    category TEXT CHECK(category IN ('tech', 'gaming', 'ai', 'crypto')),
    tags JSON,
    complexity_level TEXT CHECK(complexity_level IN ('simple', 'medium', 'complex')),
    formats JSON, -- {breaking: "...", explainer: "...", thread: [...]}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP,
    status TEXT CHECK(status IN ('draft', 'approved', 'published', 'rejected'))
);

-- publications: Where content went
CREATE TABLE publications (
    id TEXT PRIMARY KEY,
    story_id TEXT REFERENCES stories(id),
    channel TEXT CHECK(channel IN ('web', 'twitter', 'telegram', 'newsletter', 'audio')),
    format_type TEXT,
    published_at TIMESTAMP,
    external_url TEXT,
    external_id TEXT, -- tweet id, telegram msg id, etc
    engagement_metrics JSON
);

-- agent_logs: Audit trail
CREATE TABLE agent_logs (
    id TEXT PRIMARY KEY,
    agent_type TEXT,
    story_id TEXT,
    action TEXT,
    reasoning TEXT,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- analytics: Performance data
CREATE TABLE analytics (
    date DATE PRIMARY KEY,
    discoveries INTEGER,
    stories_published INTEGER,
    avg_engagement_rate REAL,
    top_category TEXT,
    top_channel TEXT,
    follower_growth INTEGER
);
```

---

## File Structure

```
eli5ai/
├── agents/
│   ├── discovery/
│   │   ├── agent.yaml
│   │   ├── sources.json
│   │   └── prompts/
│   ├── research/
│   │   ├── agent.yaml
│   │   └── prompts/
│   ├── writer/
│   │   ├── agent.yaml
│   │   └── prompts/
│   ├── multimedia/
│   │   ├── agent.yaml
│   │   └── prompts/
│   ├── orchestrator/
│   │   ├── agent.yaml
│   │   └── prompts/
│   ├── publisher/
│   │   ├── agent.yaml
│   │   └── prompts/
│   ├── engagement/
│   │   ├── agent.yaml
│   │   └── prompts/
│   └── analytics/
│       ├── agent.yaml
│       └── prompts/
├── web/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── [slug]/page.tsx
│   ├── components/
│   │   ├── story-card.tsx
│   │   ├── story-detail.tsx
│   │   ├── tag-filter.tsx
│   │   └── status-bar.tsx
│   ├── lib/
│   │   ├── db.ts
│   │   ├── typefully.ts
│   │   └── telegram.ts
│   └── public/
├── shared/
│   ├── database/
│   │   ├── schema.sql
│   │   └── migrations/
│   └── types/
├── cron/
│   └── jobs.yaml
└── memory/
    └── state.json
```

---

## Typefully Integration

```typescript
// web/lib/typefully.ts
const TYPEFULLY_API_KEY = 'EirIZilF8NL88ywNzlRxLEYqGJqCeE1X';
const TYPEFULLY_API_URL = 'https://api.typefully.com/v1';

interface ThreadTweet {
  text: string;
}

interface PublishOptions {
  threadify?: boolean;
  scheduleAt?: string;
  autoRetweet?: boolean;
}

export async function publishToTwitter(
  content: string | ThreadTweet[],
  options: PublishOptions = {}
) {
  const response = await fetch(`${TYPEFULLY_API_URL}/drafts`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TYPEFULLY_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      content: typeof content === 'string' ? content : undefined,
      thread: Array.isArray(content) ? content : undefined,
      schedule_at: options.scheduleAt,
      auto_retweet: options.autoRetweet,
    }),
  });

  return response.json();
}

export async function getAnalytics(draftId: string) {
  const response = await fetch(`${TYPEFULLY_API_URL}/drafts/${draftId}/analytics`, {
    headers: {
      'Authorization': `Bearer ${TYPEFULLY_API_KEY}`,
    },
  });

  return response.json();
}
```

---

## Web Frontend

```typescript
// web/app/page.tsx
export default async function Home() {
  const stories = await getStories({ limit: 50 });
  
  return (
    <main className="min-h-screen bg-[#0A0A0A] text-white font-sans">
      <div className="mx-auto max-w-2xl px-4 py-8">
        {/* Header */}
        <header className="mb-8 border-b border-[#222] pb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="font-mono text-2xl tracking-tight">
                <span className="text-[#00D4FF]">ELI5</span>
                <span className="text-white">AI</span>
              </h1>
              <p className="mt-1 text-xs text-[#666] font-mono">
                Complex topics, simply explained. 24/7.
              </p>
            </div>
            <div className="flex gap-2">
              <span className="h-2 w-2 rounded-full bg-[#00D4FF] animate-pulse" />
              <span className="text-[10px] text-[#666] font-mono uppercase">
                Swarm Active
              </span>
            </div>
          </div>
        </header>
        
        {/* Filters */}
        <TagFilter categories={['tech', 'gaming', 'ai', 'crypto']} />
        
        {/* Stories */}
        <div className="space-y-0">
          {stories.map((story) => (
            <StoryCard key={story.id} story={story} />
          ))}
        </div>
        
        {/* Status */}
        <StatusBar />
      </div>
    </main>
  );
}
```

---

## Cron Configuration

```yaml
# cron/jobs.yaml
jobs:
  - name: eli5ai-discovery
    schedule: "*/10 * * * *"
    agent: eli5ai-discovery
    
  - name: eli5ai-engagement
    schedule: "*/30 * * * *"
    agent: eli5ai-engagement
    
  - name: eli5ai-analytics
    schedule: "0 */6 * * *"
    agent: eli5ai-analytics
    
  - name: eli5ai-newsletter
    schedule: "0 14 * * 0"  # Sundays 2pm UTC
    agent: eli5ai-publisher
    params:
      mode: newsletter
```

---

## Deployment

```bash
#!/bin/bash
# deploy.sh

echo "🚀 Deploying ELI5AI..."

# Setup database
echo "Setting up database..."
sqlite3 eli5ai.db < shared/database/schema.sql

# Install dependencies
echo "Installing dependencies..."
cd web && npm install && cd ..

# Deploy web
echo "Deploying to Vercel..."
cd web && vercel --prod && cd ..

# Setup cron jobs
echo "Setting up agent swarm..."
openclaw cron add --file cron/jobs.yaml

# Seed sources
echo "Seeding sources..."
node scripts/seed-sources.js

echo "✅ ELI5AI is live and autonomous"
echo "Web: https://eli5ai.vercel.app"
echo "Twitter: @eli5ai"
echo "Telegram: t.me/eli5ai"
```

---

## Next Steps

1. ✅ Architecture defined
2. ⏳ Create GitHub repo
3. ⏳ Scaffold Next.js app
4. ⏳ Implement agent configs
5. ⏳ Setup Typefully integration
6. ⏳ Deploy and activate swarm

**Ready to build ELI5AI?**
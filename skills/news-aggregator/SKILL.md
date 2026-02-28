---
name: news-aggregator
description: World's most powerful news aggregation system. Use when the user wants to aggregate, curate, or summarize news from multiple sources including mainstream media, Substacks, X/Twitter, crypto-native sources, research papers, and independent blogs. Automatically spawns specialized sub-agents for parallel source scanning, deduplication, and intelligent summarization. Delivers comprehensive briefings with strict recency filters.
---

# News Aggregator Skill

The most powerful news aggregation system. Designed for comprehensive coverage across mainstream, indie, crypto, and research sources.

## Core Philosophy

- **Parallel scanning** - Multiple sub-agents hit different source categories simultaneously
- **Intelligent deduplication** - Same story from different sources = one entry with multiple citations
- **Strict recency** - Enforce time windows ruthlessly
- **Source diversity** - Never rely on single source type
- **Concise output** - 1 sentence summaries, clean format

## Source Categories

### Tier 1: Mainstream (Always check)
- Bloomberg, Reuters, CNBC, WSJ, FT, NYT, WaPo, AP, AFP, BBC
- **Sub-agents:** 2 (US markets, International)

### Tier 2: Tech & AI
- TechCrunch, The Verge, Ars Technica, Wired, Rest of World
- AI-specific: Import AI, AI News, LessWrong, Alignment Forum
- **Sub-agents:** 2 (General tech, AI research)

### Tier 3: Substacks (High signal)
- Noahpinion, Doomberg, The Diff, Stratechery, Perspectives
- Matt Stoller (BIG), Garbage Day, Platformer, Lenny's Newsletter
- The Bear Traps, Kobeissi Letter, Sherman Report
- **Sub-agents:** 3 (Macro, Tech, Crypto/DeFi)

### Tier 4: X/Twitter (Real-time alpha)
- @DeFiSurfer808, @DegenSpartan, @zhusu, @DylanLeClair_
- @LynAldenContact, @naval, @balajis, @punk6529, @ercwl
- @tangent_wang, @0xjaypeg, @Route2FI, @ThorHartvigsen
- @WazzCrypto, @CryptoCobain, @iamnomad
- **Sub-agents:** 2 (Crypto CT, Tech/Macro CT)

### Tier 5: Crypto-Native
- The Block, CoinDesk, CoinTelegraph, Unchained
- Bankless, Delphi Digital, Messari, Glassnode, CryptoQuant
- DefiLlama, Token Terminal, Dune Analytics
- **Sub-agents:** 2 (News, On-chain data)

### Tier 6: Macro & Finance
- Lyn Alden, Arthur Hayes, ZeroHedge, Real Vision
- Grant Williams, Raoul Pal, Doomberg
- **Sub-agents:** 1

### Tier 7: Research & VC
- a16z, Founders Fund, Paradigm, Electric Capital essays
- NBER papers, arXiv (AI/ML), SSRN
- **Sub-agents:** 1

### Tier 8: Regional
- Asia: Nikkei Asia, SCMP, Caixin Global, Korea Herald
- Europe: EUobserver, Politico Europe, Euractiv
- MENA: Al Jazeera, Middle East Eye
- **Sub-agents:** 2 (Asia, Europe/MENA)

### Tier 9: Independent Blogs
- Hacker News, Marginal Revolution, Astral Codex Ten
- Ribbonfarm, Interconnected, Applied Divinity Studies
- **Sub-agents:** 1

## Workflow

### Step 1: Spawn Parallel Sub-Agents

For each tier, spawn a sub-agent with specific source list and time window:

```
sessions_spawn for each tier:
  - agentId: main
  - model: kimi-coding/k2p5
  - thinking: on
  - task: "Search [specific sources] for news from past [X hours]. Return in format:
    [Topic]
    • Summary: [1 sentence]
    • Link: [URL]
    • Source: [publication name]"
```

### Step 2: Collect Results

Wait for all sub-agents to complete. Collect outputs into unified list.

### Step 3: Deduplicate

Use semantic similarity to identify same story from multiple sources:
- Same event/topic = merge into single entry
- Keep all source links as citations
- Prioritize original source or most detailed coverage

### Step 4: Rank by Impact

Score each story:
- **Market moving potential** (High/Medium/Low)
- **Source quality** (Tier 1 = highest)
- **Recency** (within last hour = boost)
- **Uniqueness** (not widely reported = boost)

### Step 5: Format Output

```
📰 TOP HEADLINES (High Impact)
[Story 1]
• Summary: [1 sentence]
• Link: [primary URL]
• Also: [secondary sources]

🤖 AI & TECH
...

💰 CRYPTO & BLOCKCHAIN
...

🌍 GLOBAL POLITICS & MACRO
...

📊 MARKET MOVERS
...

⚠️ WATCHLIST
[Stories to monitor]
```

## Sub-Agent Templates

### Template: Mainstream Scanner
```
Search Bloomberg, Reuters, CNBC, WSJ for news from past [X] hours.
Focus: [AI/Tech/Crypto/Politics/Macro]
Return format:
[Topic]
• Summary: [1 sentence]
• Link: [URL]
```

### Template: Substack Scanner
```
Search Substacks: [list] for posts from past [X] hours.
Focus on high-signal analysis and original research.
Return format:
[Topic]
• Summary: [1 sentence]
• Link: [URL]
• Author: [Substack name]
```

### Template: X/Twitter Scanner
```
Search X/Twitter accounts: [list] for posts from past [X] hours.
Focus on alpha, breaking news, market commentary.
Return format:
[Topic]
• Summary: [1 sentence]
• Link: [tweet URL or referenced link]
• Via: @[account]
```

### Template: Crypto-Native Scanner
```
Search CoinDesk, The Block, Unchained, Bankless, Delphi Digital for past [X] hours.
Also check DefiLlama for protocol news and unlocks.
Return format:
[Topic]
• Summary: [1 sentence]
• Link: [URL]
```

### Template: On-Chain Scanner
```
Check Glassnode, CryptoQuant, Arkham, Lookonchain for:
- Whale movements
- Exchange flows
- Large liquidations
- Protocol TVL changes
Return format:
[Topic]
• Summary: [1 sentence]
• Link: [URL]
• Data: [key metric]
```

## Time Windows

| Briefing Type | Time Window | Sub-Agents |
|--------------|-------------|------------|
| Morning/Afternoon (20+ stories) | 24 hours | 15 |
| Market Pulse | 6 hours | 10 |
| Overnight Wrap | 12 hours | 12 |
| Breaking News | 1-3 hours | 8 |

## Quality Checks

Before delivering:
- [ ] All summaries are 1 sentence max
- [ ] All links are valid URLs
- [ ] No stories older than time window
- [ ] Deduplication complete
- [ ] Impact ratings assigned
- [ ] Source diversity verified (min 5 categories)

## Example Output

```
📰 TOP HEADLINES

[Supreme Court Strikes Trump Tariffs]
• Summary: SCOTUS rules 6-3 that Trump exceeded authority on reciprocal tariffs, but Trump immediately announces new 10% global tariff.
• Link: https://cnbc.com/...
• Also: Bloomberg, Reuters, @tangent_wang
• Impact: HIGH

🤖 AI & TECH

[Anthropic Claude Code Security Launch]
• Summary: Anthropic launches AI security tool that finds bugs, causing cybersecurity stocks to drop 7-9%.
• Link: https://...
• Via: The Verge, @balajis
• Impact: MEDIUM
```

## Advanced Features

### Sentiment Analysis
Tag each story with market sentiment: 🟢 Bullish / 🟡 Neutral / 🔴 Bearish

### Correlation Tracking
Note when multiple sources report same theme (e.g., "AI disruption" = trend)

### Prediction Market Integration
Check Polymarket/Kalshi for market-implied probabilities on reported events

### Whale Alert Integration
Flag when on-chain data aligns with news (e.g., large ETH move before ETF news)

## Error Handling

If sub-agent fails:
1. Retry once with shorter timeout
2. If still failing, note gap in coverage
3. Prioritize remaining sources to compensate

If no results from category:
1. Expand time window slightly (e.g., 6h → 8h)
2. Check alternative sources in same tier
3. Note "quiet period" if genuinely no news

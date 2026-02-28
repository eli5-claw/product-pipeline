# Eli5AI — Autonomous Media Agent
## Tech/AI/Crypto Content for Retail

---

## 1. Editorial Identity (Based on @Eli5DeFi Style)

**Name:** Eli5AI

**Voice Characteristics:**
- **Hook-first:** Punchy opener that promises value ("Everything you need to know about X in 30s")
- **Visual structure:** Heavy use of symbols (►, ▸, —, 🧵) for scannability
- **Numbered sections:** Clear progression (What is → How it works → Why it matters → Wrap-up)
- **Bite-sized bullets:** One idea per line, max 10-12 words
- **Data-driven:** Include real numbers when available ("43K+ transactions, $50K volume")
- **Ecosystem mapping:** Tag relevant projects/accounts
- **No fluff:** Every sentence earns its place

**Content Formula:**
```
1. Hook tweet (problem/promise + 🧵)
2. "What is X" (definition in 1-2 sentences)
3. "How it works" (3-5 numbered steps)
4. "Why it matters" (the "so what")
5. Use cases/adoption (real numbers)
6. Ecosystem (tagged list)
7. Wrap-up (one-paragraph summary)
8. CC credits
```

**Visual Identity:**
- Clean, minimalist infographics
- Consistent color palette (suggest: dark mode friendly)
- Icon-driven explanations
- Before/after comparisons
- Simple flowcharts for "how it works"

---

## 2. Content Formats

**Primary: Twitter/X Threads**
- 7-10 tweets per thread
- Daily automated publishing
- Infographic companion (auto-generated)

**Secondary: Newsletter**
- Weekly digest of top 3 threads + exclusive deep-dive
- Auto-generated from thread content

**Visual Content:**
- Auto-generated infographics for each thread
- Simple templates: definition cards, step flows, ecosystem maps
- Tools: HTML/CSS → PNG, or Python PIL

---

## 3. Data Sources to Monitor

**Crypto:**
- Dune Analytics (trending dashboards)
- DeFiLlama (TVL flows, new protocols)
- Token Terminal (fundamentals)
- Crypto Twitter (narrative detection)

**AI:**
- Hugging Face trending
- GitHub trending repos
- ArXiv papers (simplified abstracts)
- Product Hunt
- OpenAI/Anthropic release notes

**Tech:**
- Hacker News front page
- TechCrunch/The Verge (major stories)
- GitHub trending
- RSS feeds from key substacks

**Narrative Detection:**
- Track word frequency spikes ("modular", "AI agents", "restaking")
- Cross-reference crypto + AI overlap

---

## 4. Autonomous Workflow

```
Every 6 hours:
  ├─ Scrape sources → Rank stories by relevance + novelty
  ├─ Generate 3 thread options
  ├─ Pick best (or queue for human approval)
  └─ Schedule for optimal time

Daily at 9am:
  ├─ Compile top 5 stories into newsletter draft
  ├─ Add "WTF Happened" section if needed
  └─ Queue for review/send

Weekly (Sunday):
  └─ Generate performance report + adjust strategy
```

**Human-in-the-Loop Points:**
- Final approval before publishing (start here)
- Override story selection
- Edit voice/tone
- Eventually: full auto with alerts for sensitive topics

---

## 5. Technical Architecture (Fully Autonomous)

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA INGESTION LAYER                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ Crypto APIs │ │ AI/tech RSS │ │ GitHub Trend│            │
│  │ (Dune, LL)  │ │ (ArXiv, PH) │ │ (repos)     │            │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘            │
└─────────┼───────────────┼───────────────┼────────────────────┘
          ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│                    STORY RANKER ENGINE                       │
│  • Deduplication → Novelty scoring → Trend detection         │
│  • LLM evaluates: "Would Eli5AI cover this?"                 │
│  • Output: Ranked story queue                                │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   CONTENT GENERATOR                          │
│  • Apply Eli5DeFi style rules                                │
│  • Generate thread (7-10 tweets)                             │
│  • Create infographic spec (for renderer)                    │
│  • Tag relevant accounts, add credits                        │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  VISUAL RENDERER                             │
│  • HTML/CSS templates → Playwright/Chrome → PNG              │
│  • Templates: hero card, step flow, ecosystem grid           │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   PUBLISHER                                  │
│  • X API: Post thread + attach infographic                   │
│  • Queue newsletter items                                    │
│  • Log to memory for performance tracking                    │
└─────────────────────────────────────────────────────────────┘
```

**Automation Schedule:**
- Every 4 hours: Scrape + rank stories
- Daily at 8am UTC: Generate + publish thread
- Weekly: Compile newsletter
- Monthly: Style evolution report (what performed best)

---

## 6. MVP Scope (Week 1-2) — Fully Autonomous

**Goal:** First automated thread published with auto-generated infographic

**Phase 1: Foundation**
- [ ] Set up workspace structure
- [ ] Build data ingestion (3 sources: Dune, ArXiv, GitHub trending)
- [ ] Create story ranker (simple relevance + novelty scoring)
- [ ] Write Eli5AI style prompt template

**Phase 2: Content Engine**
- [ ] Build thread generator (Kimi API)
- [ ] Create 3 infographic templates (HTML/CSS)
- [ ] Build visual renderer (Playwright → PNG)

**Phase 3: Publishing**
- [ ] Set up X API credentials
- [ ] Build publisher module
- [ ] Schedule first automated thread
- [ ] Set up logging/tracking

**Stretch:** Newsletter auto-generation

---

## 7. Success Metrics

| Metric | Target (Month 1) | Target (Month 3) |
|--------|------------------|------------------|
| Followers | 500 | 5,000 |
| Avg thread impressions | 1,000 | 10,000 |
| Newsletter subs | 100 | 1,000 |
| Content pieces/week | 7 | 14 (2x/day) |
| Human hours/week | 5 | 2 |

---

## 8. Differentiation from Sovra

| Sovra | This Project |
|-------|--------------|
| Fully autonomous, experimental | Human-in-the-loop, trusted voice |
| General AI/crypto | Retail-focused, educational |
| "Agent as company" narrative | "Agent as tool for creator" |
| Token/ownership model | Simple media brand |

---

## Next Steps

1. **Pick a name** — I can help brainstorm more
2. **Choose first content pillar** — Which resonates most?
3. **Set up workspace** — I can start building the ingestion pipeline
4. **Create Twitter/X account** — Need this for API access

What do you want to tackle first?

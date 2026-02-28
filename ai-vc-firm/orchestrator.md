# AI VC Firm - Master Orchestrator

## Company Structure
AI-powered Venture Capital firm focused on AI and Crypto research.

## Agentic Staff

| Role | Agent File | Primary Function |
|------|------------|------------------|
| COO | `coo-agent.md` | Operations, coordination, project management |
| CRD | `crd-agent.md` | Research, market analysis, due diligence |
| CBD | `cbd-agent.md` | Blockchain technical evaluation, security |
| CDAE | `cdae-agent.md` | Data engineering, ML models, analytics |
| CGD | `cgd-agent.md` | Design, visual assets, brand identity |
| CMO | `cmo-agent.md` | Marketing strategy, growth, communications |
| CCO | `cco-agent.md` | Content creation, research reports, editorial |

## Standard Workflows

### 1. New Investment Opportunity
```
Trigger: Deal enters pipeline

1. COO assigns to CRD for initial screen
2. CRD produces opportunity brief
3. If promising:
   - CBD: Technical due diligence
   - CDAE: Data analysis and modeling
   - CRD: Deep research and market analysis
4. CGD: Investment memo design
5. CCO: Final report writing
6. CMO: Prepare presentation materials
7. COO: Coordinate review meeting
8. Human partners: Investment decision
```

### 2. Content Production
```
Trigger: Content calendar deadline

1. CMO: Strategy and topic selection
2. CRD: Research and data gathering
3. CDAE: Data analysis and visualization
4. CCO: Content writing
5. CGD: Visual design and graphics
6. CMO: Distribution and promotion
7. COO: Performance tracking
```

### 3. Portfolio Company Support
```
Trigger: Portfolio company needs help

1. COO: Assess needs and assign resources
2. CRD: Market/competitive research
3. CBD: Technical advisory (if applicable)
4. CMO: Marketing and PR support
5. CCO: Content and documentation
6. CGD: Design assets
7. COO: Track outcomes and report
```

### 4. Fund Marketing
```
Trigger: Fundraise or LP communications

1. CMO: Strategy and messaging
2. CRD: Market analysis and positioning
3. CDAE: Performance data and analytics
4. CCO: Content writing (memos, updates)
5. CGD: Visual design (pitch decks, one-pagers)
6. CMO: Distribution and meetings
7. COO: Pipeline and relationship tracking
```

## Communication Protocols

### Daily Standups (Automated)
Each agent reports to COO:
- Completed tasks
- In-progress work
- Blockers or needs
- Next priorities

### Weekly Reviews
- Pipeline status (COO)
- Deal flow analysis (CRD)
- Content performance (CMO/CCO)
- Technical updates (CBD/CDAE)
- Design deliverables (CGD)

### Investment Committee
- Deal presentations (COO coordinates)
- Portfolio updates (CDAE)
- Market insights (CRD)
- Strategy alignment (All)

## Command Reference

### Spawn Single Agent
```bash
sessions_spawn \
  --task "[Specific task description]" \
  --agent-id [coo|crd|cbd|cdae|cgd|cmo|cco] \
  --label "[project-name-task]"
```

### Multi-Agent Workflow
```bash
# Investment due diligence
sessions_spawn --task "Initial screen of [Company]" --agent-id crd --label "dd-initial"
sessions_spawn --task "Technical review of [Company]" --agent-id cbd --label "dd-tech"
sessions_spawn --task "Data analysis for [Company]" --agent-id cdae --label "dd-data"

# Content production
sessions_spawn --task "Research on [Topic]" --agent-id crd --label "content-research"
sessions_spawn --task "Write article on [Topic]" --agent-id cco --label "content-write"
sessions_spawn --task "Create graphics for [Topic]" --agent-id cgd --label "content-design"
```

### Coordination Commands
```bash
# COO coordinates complex project
sessions_spawn \
  --task "Coordinate full due diligence on [Company]: assign CRD for market research, CBD for technical review, CDAE for data analysis, timeline 5 days, deliverable: investment memo" \
  --agent-id coo \
  --label "coordination-[company]"
```

## Output Directory Structure

```
outputs/
├── deals/
│   ├── [company-name]/
│   │   ├── opportunity-brief.md
│   │   ├── technical-dd.md
│   │   ├── data-analysis.md
│   │   ├── investment-memo.md
│   │   └── decision.md
│   └── pipeline-status.md
├── content/
│   ├── blog/
│   ├── newsletters/
│   ├── reports/
│   └── social/
├── portfolio/
│   ├── [company-name]/
│   │   ├── updates/
│   │   └── support/
│   └── performance-dashboard.md
└── marketing/
    ├── pitch-decks/
    ├── one-pagers/
    └── brand-assets/
```

## Shared Knowledge

### Active Deals
- Pipeline status
- Assigned agents
- Deadlines
- Blockers

### Portfolio Companies
- Company profiles
- Performance metrics
- Support history
- Key contacts

### Research Database
- Market reports
- Technology assessments
- Competitive analysis
- Industry trends

### Templates
- Investment memos
- Pitch decks
- Due diligence checklists
- Content calendars

## Success Metrics

### Firm Level
- Deals reviewed per quarter
- Investment conversion rate
- Portfolio performance
- Fundraise progress

### Agent Level
- Tasks completed
- Quality scores
- Turnaround time
- Collaboration ratings

### Content Level
- Engagement rates
- Lead generation
- Thought leadership reach
- SEO performance

## Getting Started

1. **Set up shared knowledge base**
   - Update `shared/project-context.md`
   - Create active deals list
   - Set up portfolio tracking

2. **Run first workflow**
   - Choose a test deal or content piece
   - Spawn appropriate agents
   - Review outputs
   - Refine process

3. **Establish routines**
   - Daily standups (automated)
   - Weekly reviews
   - Monthly strategy sessions

4. **Scale gradually**
   - Start with 1-2 deals
   - Add more agents as needed
   - Build template library
   - Automate repetitive tasks

# AI VC Firm - Quick Start Guide

## Overview
A fully agentic Venture Capital firm specializing in AI and Crypto research.

## Your Agentic Team

| Chief | Role | File |
|-------|------|------|
| COO | Operations & Coordination | `agents/coo-agent.md` |
| CRD | Research & Due Diligence | `agents/crd-agent.md` |
| CBD | Blockchain Technical | `agents/cbd-agent.md` |
| CDAE | Data & AI Engineering | `agents/cdae-agent.md` |
| CGD | Graphic Design | `agents/cgd-agent.md` |
| CMO | Marketing | `agents/cmo-agent.md` |
| CCO | Content | `agents/cco-agent.md` |

## Quick Commands

### Review a New Deal
```bash
# Full due diligence workflow
sessions_spawn --task "Screen [Company] - AI infrastructure startup, $5M seed, 10 employees" --agent-id crd --label "screen-acme"
sessions_spawn --task "Technical review of [Company]'s architecture" --agent-id cbd --label "tech-acme"
sessions_spawn --task "Data analysis on [Company] market and metrics" --agent-id cdae --label "data-acme"
```

### Create Content
```bash
# Blog post production
sessions_spawn --task "Research: Top 10 AI infrastructure trends 2026" --agent-id crd --label "research-ai-trends"
sessions_spawn --task "Write blog post on AI infrastructure trends" --agent-id cco --label "blog-ai-trends"
sessions_spawn --task "Create graphics for AI trends blog" --agent-id cgd --label "design-ai-trends"
```

### Operations
```bash
# Daily coordination
sessions_spawn --task "Generate daily standup report for all agents" --agent-id coo --label "daily-standup"

# Pipeline review
sessions_spawn --task "Review pipeline status, identify blockers, prioritize deals" --agent-id coo --label "pipeline-review"
```

## Workflows

### 1. Investment Process
1. **Screen** → CRD produces opportunity brief
2. **Deep Dive** → CRD + CBD + CDAE research
3. **Memo** → CGD designs, CCO writes
4. **Decision** → Human partners review

### 2. Content Process
1. **Strategy** → CMO plans topics
2. **Research** → CRD gathers data
3. **Write** → CCO creates content
4. **Design** → CGD adds visuals
5. **Distribute** → CMO promotes

### 3. Portfolio Support
1. **Assess** → COO identifies needs
2. **Execute** → Relevant agents support
3. **Track** → CDAE monitors outcomes

## File Structure

```
ai-vc-firm/
├── README.md                 # This overview
├── orchestrator.md           # Master coordination
├── agents/
│   ├── coo-agent.md         # Operations
│   ├── crd-agent.md         # Research
│   ├── cbd-agent.md         # Blockchain
│   ├── cdae-agent.md        # Data/AI
│   ├── cgd-agent.md         # Design
│   ├── cmo-agent.md         # Marketing
│   └── cco-agent.md         # Content
├── shared/                   # Common knowledge
│   └── project-context.md
└── outputs/                  # Generated work
    ├── deals/
    ├── content/
    ├── portfolio/
    └── marketing/
```

## Next Steps

1. **Customize** `shared/project-context.md` with your firm details
2. **Test** with a sample deal or content piece
3. **Iterate** on workflows based on results
4. **Scale** to full operations

## Example: First Deal Review

```bash
# 1. Initial screen
sessions_spawn \
  --task "Screen startup: Name=AcmeAI, Stage=Seed, Amount=$3M, Sector=AI Infrastructure, 8 employees, Product=GPU optimization software" \
  --agent-id crd \
  --label "acme-screen"

# 2. Wait for output, then technical review
sessions_spawn \
  --task "Technical review of AcmeAI: Review their GPU optimization technology, architecture, competitive moat, scalability" \
  --agent-id cbd \
  --label "acme-tech"

# 3. Data analysis
sessions_spawn \
  --task "Data analysis on AcmeAI: Market size for GPU optimization, competitor benchmarking, growth projections" \
  --agent-id cdae \
  --label "acme-data"

# 4. Final memo
sessions_spawn \
  --task "Create investment memo for AcmeAI incorporating research, technical review, and data analysis" \
  --agent-id cco \
  --label "acme-memo"
```

Your AI VC firm is ready to operate!

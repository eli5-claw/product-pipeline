---
name: investment-team
description: Multi-agent investment team powered by collaborative AI analysts. Use when evaluating investments, analyzing stocks, or making portfolio decisions. Triggers on requests for investment analysis, stock evaluation, portfolio construction, or financial research.
---

# Investment Team

7 AI analysts. 4 team architectures. One goal: Better investment decisions.

## The Team

| Analyst | Focus | Tools |
|---------|-------|-------|
| Market Analyst | Macro, news, sentiment | Web search, market data |
| Financial Analyst | Valuation, fundamentals | Financial statements |
| Technical Analyst | Price action, indicators | Charts, patterns |
| Risk Officer | Position sizing, limits | Risk models |
| Knowledge Agent | Research library, memos | RAG search |
| Memo Writer | Investment memos | Documentation |
| Committee Chair | Final decisions | Synthesis |

## Team Architectures

### Coordinate Team
Dynamic orchestration for open-ended questions.
```
User: "Should we invest in NVIDIA?"
→ Market → Financial + Technical → Risk → Memo → Chair
```

### Route Team
Direct questions to the right specialist.
```
User: "What's the P/E ratio of TSLA?"
→ Routes to Financial Analyst
```

### Broadcast Team
Parallel independent assessments.
```
User: "Full committee review: evaluate AAPL"
→ All analysts evaluate simultaneously
→ Synthesized report
```

### Task Team
Autonomous decomposition for complex tasks.
```
User: "Deploy $10M across top 5 AI stocks"
→ Broken into subtasks
→ Executed in parallel
```

## Knowledge Layers

1. **Static Context** — Fund mandate, risk policy
2. **Research Library** — Company profiles, sector analysis (RAG)
3. **Memo Archive** — Past decisions and rationale

## Output Format

### Investment Memo
```markdown
# NVIDIA (NVDA) - Investment Memo

## Recommendation: BUY
**Conviction:** 8/10
**Position Size:** $2M (2% of portfolio)

## Market Analysis
[Market Analyst findings]

## Financial Analysis
[Financial Analyst findings]

## Technical Analysis
[Technical Analyst findings]

## Risk Assessment
[Risk Officer findings]

## Committee Decision
[Final rationale]
```

## Usage

```bash
# Simple evaluation
"Should we buy NVIDIA?"

# Full committee review
"Full committee review: evaluate TSLA for $2M"

# Portfolio construction
"Deploy $10M across top 5 AI stocks"

# Research query
"What does our research say about semiconductors?"
```

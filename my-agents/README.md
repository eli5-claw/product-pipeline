# My Agents - Usage Guide

## Overview
A multi-agent system for complex tasks spanning marketing, blockchain, research, and coding.

## Quick Start

### 1. Simple Task (Single Agent)

```bash
# Marketing task
sessions_spawn \
  --task "Write homepage copy for a DeFi lending protocol" \
  --agent-id marketing-agent \
  --label "defi-homepage-copy"

# Blockchain task  
sessions_spawn \
  --task "Create ERC-20 token contract with 1M supply" \
  --agent-id blockchain-agent \
  --label "erc20-token"

# Research task
sessions_spawn \
  --task "Research top 5 competitors in AI coding assistant space" \
  --agent-id research-agent \
  --label "competitor-research"

# Code task
sessions_spawn \
  --task "Build Python script to scrape product prices from e-commerce site" \
  --agent-id code-agent \
  --label "price-scraper"
```

### 2. Complex Task (Multiple Agents)

**Example: Launch a new Web3 product**

Step 1: Research
```bash
sessions_spawn \
  --task "Research DeFi yield farming market size, top protocols, and user pain points" \
  --agent-id research-agent \
  --label "yield-farm-research"
```

Step 2: Marketing Strategy
```bash
sessions_spawn \
  --task "Based on research about yield farming pain points, create go-to-market strategy including landing page copy, email sequence, and launch plan" \
  --agent-id marketing-agent \
  --label "yield-farm-gtm"
```

Step 3: Smart Contract
```bash
sessions_spawn \
  --task "Create yield farming smart contract with staking, rewards distribution, and emergency withdrawal. Optimize for MegaETH." \
  --agent-id blockchain-agent \
  --label "yield-farm-contract"
```

Step 4: Frontend
```bash
sessions_spawn \
  --task "Build React frontend for yield farming dApp with wallet connection, staking UI, and rewards display" \
  --agent-id code-agent \
  --label "yield-farm-frontend"
```

### 3. Using with Context

First, update `shared/project-context.md` with your project details.

Then reference it in tasks:
```bash
sessions_spawn \
  --task "Read /root/.openclaw/workspace/my-agents/shared/project-context.md then write landing page copy that matches our brand voice" \
  --agent-id marketing-agent \
  --label "branded-landing-page"
```

## Agent Selection Guide

| Task Type | Agent | Example |
|-----------|-------|---------|
| Copywriting, CRO, SEO | marketing-agent | "Optimize landing page headline" |
| Smart contracts, Web3 | blockchain-agent | "Debug failed transaction" |
| Research, analysis | research-agent | "Compare database options" |
| General coding | code-agent | "Build REST API" |
| Complex project | Multiple | See examples above |

## Best Practices

1. **Clear Instructions** - Be specific about what you want
2. **Context** - Provide relevant background information
3. **Constraints** - Mention budget, timeline, tech stack
4. **Review** - Always review agent output before using
5. **Iterate** - Spawn follow-up tasks to refine results

## File Structure

```
my-agents/
├── orchestrator.md          # Coordination guide
├── agents/
│   ├── marketing-agent.md   # Marketing expert
│   ├── blockchain-agent.md  # Web3 developer
│   ├── research-agent.md    # Research analyst
│   └── code-agent.md        # Software engineer
└── shared/
    └── project-context.md   # Common knowledge
```

## Advanced Usage

### Chaining Agents

```bash
# Agent 1 does research
sessions_spawn --task "Research" --agent-id research-agent --label "research-task"

# You review, then Agent 2 uses results
sessions_spawn \
  --task "Based on research from session research-task, create marketing plan" \
  --agent-id marketing-agent \
  --label "marketing-plan"
```

### Parallel Execution

Run multiple agents simultaneously for independent tasks:
```bash
# Terminal 1
sessions_spawn --task "Write blog post" --agent-id marketing-agent --label "blog-post"

# Terminal 2
sessions_spawn --task "Fix bug in API" --agent-id code-agent --label "api-bugfix"

# Terminal 3
sessions_spawn --task "Research competitors" --agent-id research-agent --label "competitors"
```

## Troubleshooting

**Agent not following instructions?**
- Be more specific in the task description
- Provide examples of desired output
- Reference the agent's skill file

**Need to combine outputs?**
- Spawn a new agent to synthesize results
- Or do it yourself with the orchestrator guide

**Agent taking too long?**
- Break task into smaller pieces
- Set timeout with `--timeout-seconds`

# Agent Orchestrator

## Purpose
Coordinate multiple specialized subagents to complete complex tasks efficiently.

## Available Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| marketing-agent | Copywriting, CRO, SEO, growth strategy | Any marketing, conversion, or content task |
| blockchain-agent | Smart contracts, Web3, MegaETH, DeFi | Blockchain development, dApps, transactions |
| research-agent | Information gathering, analysis, summarization | Research, due diligence, learning new topics |
| code-agent | General programming, debugging, architecture | Non-blockchain coding tasks |

## Workflow

1. **Analyze Request** - Determine which agent(s) are needed
2. **Delegate** - Spawn appropriate agent(s) with clear instructions
3. **Synthesize** - Combine results from multiple agents if needed
4. **Deliver** - Present final output to user

## Delegation Rules

- **Single Agent**: For focused tasks within one domain
- **Multiple Agents**: For complex tasks spanning domains
- **Sequential**: When output of one agent feeds into another
- **Parallel**: When agents can work independently

## Example Usage

```
User: "Create a landing page for my new DeFi protocol"

Orchestrator:
1. Spawn marketing-agent: "Write landing page copy for DeFi protocol"
2. Spawn blockchain-agent: "Explain protocol features for landing page"
3. Spawn code-agent: "Create HTML/CSS for landing page"
4. Synthesize results into complete deliverable
```

## Communication Format

When delegating to agents, always include:
- Clear task description
- Relevant context from shared knowledge
- Expected output format
- Constraints or requirements

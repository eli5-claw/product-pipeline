---
name: sub-agent-orchestrator
description: Spawn and coordinate multiple parallel sub-agents for complex tasks. Use when a task requires parallel research, multi-source analysis, or distributed work across different domains. Triggers on requests to spawn agents, run parallel tasks, coordinate sub-agents, or when the user describes a complex multi-part problem.
---

# Sub-Agent Orchestrator

Divide and conquer. Spawn parallel agents, aggregate results, deliver synthesis.

## When to Use

- **Multi-source research** — Scan 10+ sources simultaneously
- **Category analysis** — Analyze different market segments in parallel
- **Comparative tasks** — Compare options across multiple dimensions
- **Large-scale extraction** — Process many items concurrently

## Orchestration Pattern

### 1. Define Sub-Tasks
Break the problem into independent, parallelizable chunks:
```
Task: Analyze crypto market
Sub-tasks:
- Analyze Bitcoin on-chain data
- Analyze Ethereum ecosystem
- Analyze altcoin performance
- Analyze macro correlations
```

### 2. Spawn Sub-Agents
Use `sessions_spawn` for each sub-task:
- Clear, specific task description
- Include relevant context
- Set appropriate timeout

### 3. Aggregate Results
Collect outputs from all sub-agents:
- Deduplicate overlapping findings
- Identify conflicts or contradictions
- Rank by relevance/impact

### 4. Synthesize Output
Produce unified deliverable:
- Executive summary
- Detailed findings by category
- Actionable recommendations

## Best Practices

- **Limit parallelism** — 5-15 sub-agents is usually optimal
- **Clear task boundaries** — Each agent should have distinct scope
- **Include context** — Pass relevant background to each sub-agent
- **Set timeouts** — Prevent runaway tasks
- **Handle failures** — Some agents may fail; design for partial results

## Example: News Aggregation

```
Master task: Morning briefing
Sub-agents (16 parallel):
1. US markets reporter
2. Tech news scanner
3. Crypto on-chain analyst
4. Macro trends researcher
5. Substack curator
... etc

Aggregation: Deduplicate, rank, format into briefing
```

## Anti-Patterns (Avoid)

- Spawning agents for trivial tasks (overhead > benefit)
- Unclear task boundaries (duplicate work)
- No aggregation step (raw dumps)
- Ignoring failed sub-agents (incomplete picture)

## Output

- Synthesized findings
- Source attribution per sub-agent
- Confidence levels where applicable

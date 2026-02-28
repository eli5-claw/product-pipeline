---
name: memory-curator
description: Review and curate long-term memory from daily logs and conversations. Use when consolidating learnings, updating MEMORY.md from daily notes, or pruning outdated information. Triggers on requests to update memory, review daily logs, consolidate learnings, or during heartbeat maintenance tasks.
---

# Memory Curator

Distill daily noise into long-term wisdom. Keep MEMORY.md current and useful.

## Core Principle

Daily files are raw notes; MEMORY.md is curated wisdom. The goal is to capture what matters without hoarding everything.

## Workflow

### 1. Review Recent Daily Files
Read `memory/YYYY-MM-DD.md` for the past 7-14 days.

### 2. Identify Worthy Entries
Look for:
- **Decisions** — Choices made and why
- **Lessons learned** — Mistakes, insights, realizations
- **Preferences** — User likes/dislikes, working style
- **Context** — Projects, goals, relationships
- **Boundaries** — Things to remember (privacy, don't-do)

### 3. Update MEMORY.md
Add distilled entries:
- Concise, factual statements
- Include dates for temporal context
- Group by category (Projects, Preferences, Lessons, etc.)

### 4. Prune Outdated Info
Remove or archive:
- Completed projects no longer relevant
- Temporary preferences that changed
- Outdated contact info or context

## Categories to Maintain

- **Projects** — Active work, goals, status
- **Preferences** — How the user likes to work
- **Decisions** — Important choices and rationale
- **Lessons** — Things learned the hard way
- **People** — Key contacts, relationships
- **Tools** — Preferred tools, configurations

## Integration with Heartbeats

During heartbeat checks:
1. Check if daily files exist for recent dates
2. If backlog > 7 days, trigger curation
3. Update MEMORY.md with findings
4. Log curation activity

## Anti-Patterns (Avoid)

- Copy-pasting daily logs (too verbose)
- Keeping everything "just in case"
- Updating MEMORY.md with transient info
- Letting daily files accumulate without review

## Output

- Updated MEMORY.md
- Summary of what was added/removed
- Recommendations for future curation frequency

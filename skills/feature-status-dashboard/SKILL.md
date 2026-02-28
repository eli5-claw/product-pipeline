---
name: feature-status-dashboard
description: Real-time overview of project status, in-progress tasks, and prioritized backlog items. Use when managing project lifecycle, tracking development progress, or prioritizing tasks. Triggers on requests for project status, feature tracking, backlog management, or development workflow.
---

# Feature Status Dashboard

Project lifecycle management without external tools. Instant visibility into what's happening.

## Dashboard Overview

```
┌─────────────────────────────────────────┐
│  Project Status Dashboard               │
├─────────────────────────────────────────┤
│  In Progress: 3    Backlog: 12   Done: 8│
├─────────────────────────────────────────┤
│  🔴 P0 - Critical (2)                   │
│     • Fix payment gateway timeout       │
│     • Security audit findings           │
│                                         │
│  🟡 P1 - Important (5)                  │
│     • Add user analytics                │
│     • Optimize database queries         │
│                                         │
│  🟢 P2 - Nice to have (5)               │
│     • Dark mode toggle                  │
│     • Export to PDF                     │
└─────────────────────────────────────────┘
```

## Status Categories

### In Progress
- Currently being worked on
- Assigned owner
- Expected completion date
- Blockers (if any)

### Backlog
- Prioritized (P0, P1, P2)
- Estimated effort
- Dependencies noted
- Ready to start

### Completed
- Recently shipped
- Links to documentation
- Lessons learned
- Metrics (if applicable)

## Priority Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| P0 | Critical, blocks release | Immediate |
| P1 | Important, affects users | This sprint |
| P2 | Nice to have | Next sprint |

## Usage Patterns

### Daily Standup
```
"What's the status?"
→ Shows in-progress, blockers, completed yesterday
```

### Sprint Planning
```
"Show backlog prioritized"
→ P0 items first, then P1, then P2
```

### Project Health
```
"Velocity check"
→ Completed vs planned, trend analysis
```

## File Format

Store in `features.md`:
```markdown
## In Progress
- [ ] Payment fix (P0) @alice due:2024-02-28

## Backlog
- [ ] Analytics (P1) #depends:payment

## Done
- [x] Auth system (P0) shipped:2024-02-20
```

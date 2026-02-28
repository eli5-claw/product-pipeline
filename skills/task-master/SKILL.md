---
name: task-master
description: AI-powered task management for developers. Use when breaking down projects, tracking tasks, or managing development workflow. Triggers on requests for task management, project breakdown, todo lists, or development planning.
---

# Task Master

Project management that understands code. Break down, track, ship.

## Core Concepts

### Tasks
- Clear, actionable items
- Estimated effort
- Dependencies mapped
- Acceptance criteria

### Projects
- Collections of tasks
- Milestones
- Deadlines
- Progress tracking

## Workflow

### 1. Project Initiation
```
"Create project: E-commerce API"
→ Generates task breakdown
→ Estimates effort
→ Identifies dependencies
```

### 2. Task Breakdown
```
Project: E-commerce API
├── Setup (2h)
│   ├── Initialize repo
│   └── Configure CI/CD
├── Auth (4h)
│   ├── Login endpoint
│   ├── JWT middleware
│   └── Password reset
├── Products (6h)
│   ├── CRUD endpoints
│   ├── Image upload
│   └── Search
└── Orders (8h)
    ├── Cart management
    ├── Checkout flow
    └── Payment integration
```

### 3. Execution
- Pick next task
- Update status
- Log blockers
- Mark complete

### 4. Review
- Sprint retrospective
- Velocity tracking
- Scope adjustment

## Task Format

```markdown
## Task: AUTH-001 - Login Endpoint
**Status:** In Progress
**Assignee:** @alice
**Due:** 2024-02-28
**Effort:** 2h

### Description
Implement JWT-based login endpoint

### Acceptance Criteria
- [ ] POST /auth/login accepts email/password
- [ ] Returns valid JWT on success
- [ ] Returns 401 on invalid credentials
- [ ] Rate limited to 5 attempts/minute

### Dependencies
- Database schema (DB-001)

### Notes
Using bcrypt for password hashing
```

## Commands

```bash
# Create project
task-master init "Project Name"

# Add task
task-master add "Task description" --project X --priority P1

# List tasks
task-master list --status open --priority P0,P1

# Update status
task-master update TASK-001 --status done

# Show project
task-master show "Project Name"
```

## Integration

- Git commits → Auto-update task status
- PRs → Link to tasks
- Deployments → Mark milestones complete

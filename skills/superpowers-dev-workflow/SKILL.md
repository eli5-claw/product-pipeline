---
name: superpowers-dev-workflow
description: Comprehensive software development workflow from design refinement to TDD-driven implementation. Use when building software with AI agents to ensure systematic, high-quality code generation. Triggers on requests for structured development, TDD, implementation planning, or subagent-driven development.
---

# Superpowers Dev Workflow

Transform AI coding from ad-hoc to systematic. Design first, test always, deliver quality.

## Core Philosophy

1. **Design Before Code** — Interactive refinement creates clear specs
2. **Test-Driven Development** — Tests first, implementation second
3. **YAGNI + DRY** — You Aren't Gonna Need It, Don't Repeat Yourself
4. **Subagent Orchestration** — Parallel execution with quality gates

## Workflow Phases

### Phase 1: Design Refinement
- Start with rough idea
- Ask clarifying questions
- Explore alternatives
- Document decisions
- Output: Clear specification

### Phase 2: Implementation Planning
- Break into bite-sized tasks
- Identify dependencies
- Estimate complexity
- Assign to subagents
- Output: Detailed plan

### Phase 3: TDD Development
For each task:
1. Write failing test
2. Implement minimal code
3. Verify test passes
4. Refactor if needed

### Phase 4: Code Review
- Automated checks
- Peer review (subagent)
- Quality gates
- Merge or iterate

## Subagent Patterns

### Parallel Development
```
Task A ──→ Subagent 1 ──┐
Task B ──→ Subagent 2 ──┼──→ Integration
Task C ──→ Subagent 3 ──┘
```

### Pipeline Development
```
Design ──→ Implementation ──→ Review ──→ Test ──→ Deploy
```

## Quality Gates

- **Linting** — No style violations
- **Tests** — All pass, coverage >80%
- **Security** — No vulnerabilities
- **Performance** — Benchmarks met

## Best Practices

- Small, focused commits
- Descriptive commit messages
- Branch per feature
- Document as you go

## References

- [TDD Patterns](references/tdd-patterns.md)
- [Subagent Orchestration](references/subagent-patterns.md)
- [Code Review Checklist](references/code-review.md)

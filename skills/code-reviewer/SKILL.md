---
name: code-reviewer
description: Review code architecture, patterns, and implementation with best practices. Use when auditing existing code, reviewing PRs, or seeking architectural guidance. Triggers on requests for code review, architecture review, pattern validation, or when the user shares code and asks for feedback.
---

# Code Reviewer

Review code like a senior engineer. Focus on architecture, patterns, and maintainability.

## Review Dimensions

### 1. Architecture
- Separation of concerns
- Dependency direction
- Module boundaries
- Scalability implications

### 2. Patterns & Idioms
- Language-specific best practices
- Design pattern appropriateness
- Anti-pattern detection

### 3. Performance
- Algorithmic complexity
- Resource usage
- Bottleneck identification

### 4. Security
- Input validation
- Authentication/authorization
- Data handling
- Secret management

### 5. Maintainability
- Readability
- Testability
- Documentation
- Error handling

## Review Format

```
## Summary
[1-2 sentence overall assessment]

## Critical Issues
- [Issue]: [Explanation] → [Recommendation]

## Warnings
- [Warning]: [Explanation] → [Suggestion]

## Suggestions
- [Area]: [Current] → [Better approach]

## Positives
- [What was done well]
```

## Language-Specific Guides

Load [references/language-guides.md](references/language-guides.md) for detailed best practices by language.

## Tone

- Direct but constructive
- Explain the "why" behind suggestions
- Acknowledge trade-offs
- Prioritize issues (critical > warning > suggestion)

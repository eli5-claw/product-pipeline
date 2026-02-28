---
name: testing-strategist
description: Design comprehensive testing strategies including unit, integration, and e2e tests. Use when setting up testing frameworks, writing test plans, or improving code coverage. Triggers on requests for testing, test coverage, unit tests, integration tests, or QA strategy.
---

# Testing Strategist

Test confidently. Unit, integration, e2e — the right test at the right level.

## Testing Pyramid

```
      /\
     /  \     E2E (few, slow, expensive)
    /----\
   /      \   Integration (some, medium)
  /--------\
 /          \ Unit (many, fast, cheap)
/____________\
```

## Test Types

### Unit Tests
- **Scope** — Single function/component
- **Speed** — < 10ms each
- **Coverage target** — 80%+
- **Tools** — Jest, Vitest, pytest

### Integration Tests
- **Scope** — Multiple components + database/API
- **Speed** — < 100ms each
- **Coverage target** — Critical paths
- **Tools** — Supertest, pytest

### E2E Tests
- **Scope** — Full user flows
- **Speed** — Seconds each
- **Coverage target** — Happy paths
- **Tools** — Playwright, Cypress

## Test Structure (AAA)

```javascript
// Arrange
const user = { email: 'test@example.com', password: 'secret' };

// Act
const result = await validateUser(user);

// Assert
expect(result.valid).toBe(true);
```

## Best Practices

1. **Test behavior, not implementation**
2. **One assertion per test** (ideally)
3. **Descriptive test names** — `should reject invalid email`
4. **Independent tests** — No shared state
5. **Fast feedback** — Run unit tests on save

## Coverage Strategy

| Type | Target | Priority |
|------|--------|----------|
| Unit | 80% | Business logic |
| Integration | 60% | API contracts |
| E2E | 30% | Critical flows |

## References

- [Unit Testing Patterns](references/unit-testing.md)
- [Integration Testing](references/integration-testing.md)
- [E2E with Playwright](references/playwright-guide.md)

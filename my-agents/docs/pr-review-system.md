# Autonomous PR Review System

## Overview
A multi-agent system for automated pull request review that fetches PRs, analyzes code, detects issues, and provides structured feedback.

## Architecture

```
PR Event (GitHub Webhook)
    ↓
Orchestrator
    ↓
┌─────────────┬─────────────┬─────────────┐
↓             ↓             ↓             ↓
PR Fetch    Security    Code Quality   Test Check
Agent       Agent       Agent          Agent
    └─────────────┴─────────────┴─────────────┘
                    ↓
            Report Generator
                    ↓
            GitHub PR Comment
```

## Components

### 1. PR Fetch Agent
Fetches PR data from GitHub API:
- PR metadata (title, description, author)
- Diff/changes
- Commit history
- Related issues

### 2. Security Review Agent
Scans for security issues:
- Hardcoded secrets/credentials
- Injection vulnerabilities (SQL, XSS, command)
- Authentication flaws
- Authorization bypasses
- Dependency vulnerabilities

### 3. Code Quality Agent
Analyzes code quality:
- Language-specific conventions
- Code complexity
- Naming conventions
- Documentation
- Error handling

### 4. Test Coverage Agent
Checks testing:
- Test file existence
- Coverage metrics
- Missing test cases
- Test quality

### 5. Report Generator
Combines findings into structured report:
- Executive summary
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (nice to have)
- Positive feedback

## Setup

### 1. GitHub Token
Create a personal access token with `repo` scope:
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

### 2. Webhook Setup (Optional)
For automatic PR reviews, set up a GitHub webhook:
- URL: `http://your-server:8080/webhook/github`
- Events: Pull requests

### 3. Manual Usage
```bash
# Review a specific PR
./tools/pr-review.sh owner repo 123

# Or use the agent directly
sessions_spawn \
  --task "Review PR #123 in owner/repo for security and quality issues" \
  --agent-id pr-review-agent \
  --label "pr-review-123"
```

## Usage Examples

### Example 1: Single PR Review
```bash
# Fetch and analyze PR
./tools/pr-review.sh facebook react 12345

# The script outputs:
# - PR metadata
# - Changed files
# - Diff statistics
# - Path to full diff
```

### Example 2: Automated Review via Webhook
When a PR is opened:
1. GitHub sends webhook to your server
2. Orchestrator spawns PR Review Agent
3. Agent fetches PR, analyzes code
4. Posts review comment to PR

### Example 3: Batch Review
```bash
# Review all open PRs in a repo
for pr in $(gh pr list --repo owner/repo --json number -q '.[].number'); do
    sessions_spawn \
      --task "Review PR #$pr in owner/repo" \
      --agent-id pr-review-agent \
      --label "pr-review-$pr"
done
```

## Review Output Format

```markdown
## 🤖 Automated PR Review

### 📊 Summary
- **Files Changed**: 5
- **Additions**: 234
- **Deletions**: 89
- **Security Issues**: 2 (1 Critical, 1 Medium)
- **Quality Issues**: 3
- **Recommendation**: REQUEST_CHANGES

### 🚨 Critical Issues (Must Fix)

**[CRITICAL] Hardcoded API Key**
- File: `src/config.js:15`
- Issue: API key committed to repository
- Fix: Use environment variables
```javascript
// Bad
const API_KEY = "sk-abc123...";

// Good
const API_KEY = process.env.API_KEY;
```

### ⚠️ Warnings (Should Fix)

**[HIGH] SQL Injection Risk**
- File: `src/database.js:42`
- Issue: User input directly in SQL query
- Fix: Use parameterized queries

### 💡 Suggestions (Nice to Have)

1. Add unit tests for new functions
2. Update documentation
3. Consider error handling improvements

### ✅ Positive Feedback
- Good use of async/await
- Clean separation of concerns
- Well-structured commit messages
```

## Integration with CI/CD

### GitHub Actions
```yaml
name: AI PR Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run PR Review
        run: |
          sessions_spawn \
            --task "Review PR #${{ github.event.pull_request.number }}" \
            --agent-id pr-review-agent
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-push

# Review before pushing
if [ -n "$PR_NUMBER" ]; then
    ./tools/pr-review.sh $(git remote get-url origin) $PR_NUMBER
fi
```

## Security Considerations

- Never commit review agent credentials
- Use read-only GitHub tokens when possible
- Sanitize diff output before processing
- Review agent's own code for vulnerabilities

## Customization

### Add Language Support
Edit `pr-review-agent.md` to add:
- Language-specific linting rules
- Framework-specific checks
- Custom security patterns

### Adjust Severity Thresholds
Modify the agent to:
- Block PRs on critical issues
- Warn on style violations
- Ignore certain file types

### Custom Review Rules
Add project-specific rules:
- Naming conventions
- Required documentation
- Test coverage minimums

## Monitoring

Track review metrics:
- PRs reviewed per day
- Issues found by category
- False positive rate
- Time to review

## Future Enhancements

- [ ] Auto-fix suggestions with code patches
- [ ] Learning from past reviews
- [ ] Integration with SonarQube/CodeClimate
- [ ] Custom rule DSL
- [ ] Review assignment based on file ownership

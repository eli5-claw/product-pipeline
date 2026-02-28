#!/bin/bash
# Autonomous PR Review System
# Usage: ./pr-review.sh <owner> <repo> <pr_number>

set -e

OWNER=${1:-}
REPO=${2:-}
PR_NUMBER=${3:-}

if [ -z "$OWNER" ] || [ -z "$REPO" ] || [ -z "$PR_NUMBER" ]; then
    echo "Usage: ./pr-review.sh <owner> <repo> <pr_number>"
    echo "Example: ./pr-review.sh facebook react 12345"
    exit 1
fi

echo "🔍 Starting PR Review for $OWNER/$REPO#$PR_NUMBER"
echo "================================================"

# Fetch PR details
echo "📥 Fetching PR details..."
PR_DATA=$(curl -s "https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER")
PR_TITLE=$(echo "$PR_DATA" | jq -r '.title')
PR_BODY=$(echo "$PR_DATA" | jq -r '.body')
PR_AUTHOR=$(echo "$PR_DATA" | jq -r '.user.login')
PR_BRANCH=$(echo "$PR_DATA" | jq -r '.head.ref')
BASE_BRANCH=$(echo "$PR_DATA" | jq -r '.base.ref')

echo "Title: $PR_TITLE"
echo "Author: $PR_AUTHOR"
echo "Branch: $PR_BRANCH → $BASE_BRANCH"

# Fetch PR diff
echo ""
echo "📄 Fetching PR diff..."
curl -s "https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER.diff" -o /tmp/pr_$PR_NUMBER.diff

# Count changes
FILES_CHANGED=$(grep "^diff --git" /tmp/pr_$PR_NUMBER.diff | wc -l)
ADDITIONS=$(grep "^+" /tmp/pr_$PR_NUMBER.diff | wc -l)
DELETIONS=$(grep "^-" /tmp/pr_$PR_NUMBER.diff | wc -l)

echo "Files Changed: $FILES_CHANGED"
echo "Additions: $ADDITIONS"
echo "Deletions: $DELETIONS"

# Extract changed files
echo ""
echo "📁 Changed Files:"
grep "^diff --git" /tmp/pr_$PR_NUMBER.diff | sed 's/diff --git a\//  - /' | sed 's/ b\// → /'

# Run analysis
echo ""
echo "🤖 Running AI Analysis..."

# Create analysis prompt
cat > /tmp/pr_analysis_prompt.txt << EOF
Please review this pull request:

Repository: $OWNER/$REPO
PR: #$PR_NUMBER
Title: $PR_TITLE
Author: $PR_AUTHOR
Branch: $PR_BRANCH → $BASE_BRANCH

Files Changed: $FILES_CHANGED
Additions: $ADDITIONS
Deletions: $DELETIONS

PR Description:
$PR_BODY

Diff:
$(cat /tmp/pr_$PR_NUMBER.diff | head -500)

Please provide:
1. Summary of changes
2. Security analysis (check for vulnerabilities, secrets, injection risks)
3. Code quality assessment
4. Specific issues with line references
5. Test coverage evaluation
6. Overall recommendation (APPROVE / REQUEST_CHANGES / COMMENT)
EOF

echo "Analysis prompt created at /tmp/pr_analysis_prompt.txt"
echo ""
echo "✅ PR data fetched successfully"
echo ""
echo "Next steps:"
echo "1. Review the diff at /tmp/pr_$PR_NUMBER.diff"
echo "2. Run your AI agent with the prompt at /tmp/pr_analysis_prompt.txt"
echo "3. Post review comments via GitHub API"

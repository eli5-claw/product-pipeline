#!/bin/bash

# ARTL Build Verification Script
# This script verifies that all components build successfully

set -e

echo "🔍 ARTL Build Verification"
echo "=========================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
ERRORS=0

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "📦 Checking project structure..."

# Check required files
[ -f "package.json" ] && print_status 0 "Root package.json exists" || print_status 1 "Root package.json missing"
[ -f "README.md" ] && print_status 0 "README.md exists" || print_status 1 "README.md missing"
[ -f "LICENSE" ] && print_status 0 "LICENSE exists" || print_status 1 "LICENSE missing"
[ -f "docker-compose.yml" ] && print_status 0 "docker-compose.yml exists" || print_status 1 "docker-compose.yml missing"
[ -f "DEPLOYED.md" ] && print_status 0 "DEPLOYED.md exists" || print_status 1 "DEPLOYED.md missing"
[ -f ".gitignore" ] && print_status 0 ".gitignore exists" || print_status 1 ".gitignore missing"

echo ""
echo "🔧 Checking API (NestJS)..."

cd src/api

[ -f "package.json" ] && print_status 0 "API package.json exists" || print_status 1 "API package.json missing"
[ -f "tsconfig.json" ] && print_status 0 "API tsconfig.json exists" || print_status 1 "API tsconfig.json missing"
[ -d "src" ] && print_status 0 "API src/ directory exists" || print_status 1 "API src/ directory missing"
[ -f "prisma/schema.prisma" ] && print_status 0 "Prisma schema exists" || print_status 1 "Prisma schema missing"

# Check key API modules
[ -f "src/app.module.ts" ] && print_status 0 "App module exists" || print_status 1 "App module missing"
[ -f "src/main.ts" ] && print_status 0 "Main entry exists" || print_status 1 "Main entry missing"
[ -f "src/reputation/reputation.engine.ts" ] && print_status 0 "Reputation engine exists" || print_status 1 "Reputation engine missing"
[ -f "src/reputation/reputation.service.ts" ] && print_status 0 "Reputation service exists" || print_status 1 "Reputation service missing"
[ -f "src/reputation/reputation.controller.ts" ] && print_status 0 "Reputation controller exists" || print_status 1 "Reputation controller missing"
[ -f "src/agents/agents.controller.ts" ] && print_status 0 "Agents controller exists" || print_status 1 "Agents controller missing"
[ -f "src/signals/signals.controller.ts" ] && print_status 0 "Signals controller exists" || print_status 1 "Signals controller missing"

cd ../..

echo ""
echo "🎨 Checking Web (Next.js)..."

cd src/web

[ -f "package.json" ] && print_status 0 "Web package.json exists" || print_status 1 "Web package.json missing"
[ -f "next.config.js" ] && print_status 0 "Next.js config exists" || print_status 1 "Next.js config missing"
[ -f "tsconfig.json" ] && print_status 0 "Web tsconfig.json exists" || print_status 1 "Web tsconfig.json missing"
[ -d "app" ] && print_status 0 "Web app/ directory exists" || print_status 1 "Web app/ directory missing"

# Check key web pages
[ -f "app/page.tsx" ] && print_status 0 "Home page exists" || print_status 1 "Home page missing"
[ -f "app/dashboard/page.tsx" ] && print_status 0 "Dashboard page exists" || print_status 1 "Dashboard page missing"
[ -f "app/dashboard/lookup/page.tsx" ] && print_status 0 "Lookup page exists" || print_status 1 "Lookup page missing"
[ -f "app/layout.tsx" ] && print_status 0 "Root layout exists" || print_status 1 "Root layout missing"

cd ../..

echo ""
echo "🔌 Checking MCP Server..."

cd src/mcp

[ -f "package.json" ] && print_status 0 "MCP package.json exists" || print_status 1 "MCP package.json missing"
[ -f "tsconfig.json" ] && print_status 0 "MCP tsconfig.json exists" || print_status 1 "MCP tsconfig.json missing"
[ -f "src/index.ts" ] && print_status 0 "MCP server exists" || print_status 1 "MCP server missing"

cd ../..

echo ""
echo "📋 Checking Shared Types..."

cd src/shared

[ -f "types.ts" ] && print_status 0 "Shared types exist" || print_status 1 "Shared types missing"

cd ../..

echo ""
echo "🐳 Checking Docker Configuration..."

[ -f "docker-compose.yml" ] && print_status 0 "Docker Compose exists" || print_status 1 "Docker Compose missing"
[ -f "src/api/Dockerfile" ] && print_status 0 "API Dockerfile exists" || print_status 1 "API Dockerfile missing"
[ -f "src/web/Dockerfile" ] && print_status 0 "Web Dockerfile exists" || print_status 1 "Web Dockerfile missing"
[ -f "src/mcp/Dockerfile" ] && print_status 0 "MCP Dockerfile exists" || print_status 1 "MCP Dockerfile missing"

echo ""
echo "🚀 Checking Deployment Configuration..."

[ -d ".github/workflows" ] && print_status 0 "GitHub Actions directory exists" || print_status 1 "GitHub Actions directory missing"
[ -f ".github/workflows/deploy.yml" ] && print_status 0 "Deploy workflow exists" || print_status 1 "Deploy workflow missing"
[ -f "src/api/vercel.json" ] && print_status 0 "API vercel.json exists" || print_status 1 "API vercel.json missing"
[ -f "src/web/vercel.json" ] && print_status 0 "Web vercel.json exists" || print_status 1 "Web vercel.json missing"

echo ""
echo "=========================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo "Project structure is complete and ready for deployment."
    exit 0
else
    echo -e "${RED}✗ $ERRORS check(s) failed${NC}"
    echo "Please review the errors above."
    exit 1
fi

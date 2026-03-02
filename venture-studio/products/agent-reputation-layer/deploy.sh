#!/bin/bash
# ARTL Production Deployment Script
# This script deploys the ARTL product to production using Vercel and Neon

set -e

echo "🚀 ARTL Production Deployment"
echo "=============================="

# Configuration
PROJECT_NAME="artl"
WEB_PROJECT="${PROJECT_NAME}-web"
API_PROJECT="${PROJECT_NAME}-api"
MCP_PROJECT="${PROJECT_NAME}-mcp"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    if ! command -v vercel &> /dev/null; then
        echo -e "${RED}Vercel CLI not found. Installing...${NC}"
        npm install -g vercel
    fi
    
    if ! command -v npx &> /dev/null; then
        echo -e "${RED}npx not found. Please install Node.js${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Prerequisites met${NC}"
}

# Deploy Web Frontend
deploy_web() {
    echo -e "${YELLOW}Deploying Web Frontend...${NC}"
    cd src/web
    
    # Install dependencies
    npm install
    
    # Build the project
    npm run build
    
    # Deploy to Vercel
    if vercel --version &> /dev/null; then
        vercel --prod --yes
    else
        echo -e "${YELLOW}Vercel CLI not authenticated. Manual deployment required.${NC}"
        echo "To deploy manually:"
        echo "  1. cd src/web"
        echo "  2. vercel login"
        echo "  3. vercel --prod"
    fi
    
    cd ../..
    echo -e "${GREEN}✓ Web Frontend deployment complete${NC}"
}

# Deploy API
deploy_api() {
    echo -e "${YELLOW}Deploying API Backend...${NC}"
    cd src/api
    
    # Install dependencies
    npm install
    
    # Generate Prisma client
    npx prisma generate
    
    # Build the project
    npm run build
    
    # Deploy to Vercel
    if vercel --version &> /dev/null; then
        vercel --prod --yes
    else
        echo -e "${YELLOW}Vercel CLI not authenticated. Manual deployment required.${NC}"
        echo "To deploy manually:"
        echo "  1. cd src/api"
        echo "  2. vercel login"
        echo "  3. vercel --prod"
    fi
    
    cd ../..
    echo -e "${GREEN}✓ API Backend deployment complete${NC}"
}

# Deploy MCP Server
deploy_mcp() {
    echo -e "${YELLOW}Deploying MCP Server...${NC}"
    cd src/mcp
    
    # Install dependencies
    npm install
    
    # Build the project
    npm run build
    
    # Deploy to Vercel
    if vercel --version &> /dev/null; then
        vercel --prod --yes
    else
        echo -e "${YELLOW}Vercel CLI not authenticated. Manual deployment required.${NC}"
        echo "To deploy manually:"
        echo "  1. cd src/mcp"
        echo "  2. vercel login"
        echo "  3. vercel --prod"
    fi
    
    cd ../..
    echo -e "${GREEN}✓ MCP Server deployment complete${NC}"
}

# Setup Database
setup_database() {
    echo -e "${YELLOW}Setting up Database...${NC}"
    echo -e "${YELLOW}Please create a Neon PostgreSQL database manually:${NC}"
    echo "  1. Visit https://neon.tech"
    echo "  2. Create a new project"
    echo "  3. Copy the connection string"
    echo "  4. Set it as DATABASE_URL in your environment"
    echo ""
    echo -e "${YELLOW}Please create an Upstash Redis instance:${NC}"
    echo "  1. Visit https://upstash.com"
    echo "  2. Create a new Redis database"
    echo "  3. Copy the connection string"
    echo "  4. Set it as REDIS_URL in your environment"
    echo ""
    echo -e "${GREEN}✓ Database setup instructions provided${NC}"
}

# Run database migrations
run_migrations() {
    echo -e "${YELLOW}Running Database Migrations...${NC}"
    
    if [ -z "$DATABASE_URL" ]; then
        echo -e "${RED}DATABASE_URL not set. Skipping migrations.${NC}"
        return
    fi
    
    cd src/api
    npx prisma migrate deploy
    cd ../..
    
    echo -e "${GREEN}✓ Database migrations complete${NC}"
}

# Print deployment summary
print_summary() {
    echo ""
    echo "=============================="
    echo -e "${GREEN}🎉 Deployment Complete!${NC}"
    echo "=============================="
    echo ""
    echo "Next Steps:"
    echo "  1. Set up environment variables in Vercel dashboard"
    echo "  2. Configure custom domain (optional)"
    echo "  3. Run database migrations"
    echo "  4. Test the deployed services"
    echo ""
    echo "Environment Variables to Configure:"
    echo "  - DATABASE_URL (Neon PostgreSQL)"
    echo "  - REDIS_URL (Upstash Redis)"
    echo "  - JWT_SECRET (random secure string)"
    echo "  - STRIPE_SECRET_KEY"
    echo "  - STRIPE_WEBHOOK_SECRET"
    echo "  - NEXT_PUBLIC_API_URL"
    echo "  - NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    setup_database
    
    # Deploy services
    deploy_api
    deploy_web
    deploy_mcp
    
    print_summary
}

# Run main function
main "$@"

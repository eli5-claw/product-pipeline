# ARTL Deployment Configuration

This document outlines the deployment setup for the Agent Reputation & Trust Layer (ARTL) product.

## Architecture

- **Frontend**: Next.js 14 (Vercel)
- **API**: NestJS (Vercel Serverless or Railway/Render)
- **Database**: PostgreSQL (Neon)
- **Cache**: Redis (Upstash)
- **MCP Server**: Deployed alongside API or separately

## Environment Variables

### Web Frontend (Vercel)
```
NEXT_PUBLIC_API_URL=https://api.artl.io/api/v1
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
```

### API Server
```
NODE_ENV=production
DATABASE_URL=postgresql://user:pass@neon-host/db
REDIS_URL=rediss://upstash-host:6379
JWT_SECRET=secure-random-string
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URL=https://artl.io
```

### MCP Server
```
NODE_ENV=production
API_URL=https://api.artl.io/api/v1
API_KEY=secure-api-key
```

## Deployment Steps

1. Create Neon PostgreSQL database
2. Create Upstash Redis instance
3. Deploy API to Vercel/Railway
4. Deploy Web to Vercel
5. Deploy MCP server
6. Configure environment variables
7. Run database migrations

## URLs

- Production Web: https://artl.vercel.app
- Production API: https://artl-api.vercel.app
- Production MCP: https://artl-mcp.vercel.app

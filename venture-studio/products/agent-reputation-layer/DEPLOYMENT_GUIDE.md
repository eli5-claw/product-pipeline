# ARTL Production Deployment Guide

Complete guide for deploying the Agent Reputation & Trust Layer (ARTL) to production.

## Quick Start

```bash
# 1. Clone and navigate to project
cd /root/.openclaw/workspace/venture-studio/products/agent-reputation-layer

# 2. Run the deployment script
./deploy.sh
```

## Manual Deployment Steps

### 1. Database Setup (Neon)

1. Visit [Neon](https://neon.tech) and create an account
2. Create a new project
3. Copy the PostgreSQL connection string
4. Save it as `DATABASE_URL`

### 2. Redis Setup (Upstash)

1. Visit [Upstash](https://upstash.com) and create an account
2. Create a new Redis database
3. Copy the Redis connection string
4. Save it as `REDIS_URL`

### 3. API Deployment (Vercel)

```bash
cd src/api

# Install dependencies
npm install

# Generate Prisma client
npx prisma generate

# Deploy to Vercel
vercel login
vercel --prod
```

**Environment Variables for API:**
- `DATABASE_URL` - Neon connection string
- `REDIS_URL` - Upstash connection string
- `JWT_SECRET` - Random secure string (min 32 chars)
- `STRIPE_SECRET_KEY` - From Stripe dashboard
- `STRIPE_WEBHOOK_SECRET` - From Stripe webhook settings
- `FRONTEND_URL` - Your web frontend URL

**Run Migrations:**
```bash
npx prisma migrate deploy
```

### 4. Web Frontend Deployment (Vercel)

```bash
cd src/web

# Install dependencies
npm install

# Deploy to Vercel
vercel login
vercel --prod
```

**Environment Variables for Web:**
- `NEXT_PUBLIC_API_URL` - Your API URL + /api/v1
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - From Stripe dashboard

### 5. MCP Server Deployment (Vercel)

```bash
cd src/mcp

# Install dependencies
npm install

# Deploy to Vercel
vercel login
vercel --prod
```

**Environment Variables for MCP:**
- `API_URL` - Your API backend URL
- `API_KEY` - Secure API key for MCP authentication

## Domain Configuration

### Custom Domain on Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to Settings → Domains
4. Add your custom domain
5. Follow DNS configuration instructions

### Recommended Domain Structure

- Web: `https://artl.io` or `https://app.artl.io`
- API: `https://api.artl.io`
- MCP: `https://mcp.artl.io`

## Environment Variable Summary

| Service | Variable | Value |
|---------|----------|-------|
| API | DATABASE_URL | postgresql://... |
| API | REDIS_URL | rediss://... |
| API | JWT_SECRET | secure-random-string |
| API | STRIPE_SECRET_KEY | sk_live_... |
| API | STRIPE_WEBHOOK_SECRET | whsec_... |
| API | FRONTEND_URL | https://artl-web.vercel.app |
| Web | NEXT_PUBLIC_API_URL | https://artl-api.vercel.app/api/v1 |
| Web | NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY | pk_live_... |
| MCP | API_URL | https://artl-api.vercel.app |
| MCP | API_KEY | secure-api-key |

## Verification

After deployment, verify everything is working:

```bash
# Test API health
curl https://your-api.vercel.app/api/v1/health

# Test web frontend
curl https://your-web.vercel.app

# Test MCP server
curl https://your-mcp.vercel.app/health
```

## Troubleshooting

### Database Connection Issues
- Ensure SSL mode is enabled for Neon: `?sslmode=require`
- Check that IP allowlist includes Vercel's IPs

### CORS Errors
- Verify `FRONTEND_URL` matches your actual web URL
- Include protocol (https://) in the URL

### Build Failures
- Ensure all dependencies are installed
- Check that Prisma client is generated: `npx prisma generate`

## Support

For issues or questions, refer to:
- [Vercel Docs](https://vercel.com/docs)
- [Neon Docs](https://neon.tech/docs)
- [Upstash Docs](https://docs.upstash.com)

# ARTL Deployment - Quick Reference

## 🚀 One-Command Deploy

```bash
cd /root/.openclaw/workspace/venture-studio/products/agent-reputation-layer
./deploy.sh
```

## 📋 Prerequisites

1. **Vercel CLI**: `npm i -g vercel`
2. **Neon Account**: https://neon.tech
3. **Upstash Account**: https://upstash.com
4. **Stripe Account**: https://stripe.com (optional, for payments)

## 🔑 Required Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@neon-host/db?sslmode=require

# Cache
REDIS_URL=rediss://default:pass@upstash-host.upstash.io:6379

# Auth
JWT_SECRET=your-secure-random-string-min-32-chars

# Stripe (optional)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...

# URLs
FRONTEND_URL=https://your-web.vercel.app
NEXT_PUBLIC_API_URL=https://your-api.vercel.app/api/v1
```

## 🏗️ Service Structure

```
src/
├── web/          # Next.js 14 frontend → Vercel
├── api/          # NestJS backend → Vercel Serverless
├── mcp/          # MCP server → Vercel
└── database/     # PostgreSQL schema → Neon
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `deploy.sh` | Automated deployment script |
| `.env.example` | Environment variable template |
| `DEPLOYMENT_GUIDE.md` | Full deployment guide |
| `src/web/vercel.json` | Web Vercel config |
| `src/api/vercel.json` | API Vercel config |
| `src/api/api/index.ts` | Serverless handler |

## 🌐 Default Ports (Development)

- Web: http://localhost:3000
- API: http://localhost:3001
- MCP: http://localhost:3002

## 🧪 Test Commands

```bash
# Test API
curl https://your-api.vercel.app/api/v1/health

# Test Web
curl https://your-web.vercel.app

# Test MCP
curl https://your-mcp.vercel.app/health
```

## 🔄 CI/CD

GitHub Actions workflow: `.github/workflows/deploy.yml`

Required secrets:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_API_PROJECT_ID`
- `VERCEL_WEB_PROJECT_ID`
- `VERCEL_MCP_PROJECT_ID`

## 📖 Documentation

- Full Guide: `DEPLOYMENT_GUIDE.md`
- Status Report: `DEPLOYMENT_STATUS.md`
- API Docs: `SPEC.md`

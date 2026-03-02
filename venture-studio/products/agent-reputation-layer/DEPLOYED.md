# Deployment Checklist

## Pre-Deployment

- [ ] Environment variables configured
- [ ] Database provisioned (Neon PostgreSQL)
- [ ] Cache provisioned (Upstash Redis)
- [ ] Stripe account created (for payments)
- [ ] Domain configured (optional)

## Deployment Steps

### 1. Database Setup
```bash
# Run migrations
npx prisma migrate deploy

# Verify connection
npx prisma db pull
```

### 2. API Deployment
```bash
cd src/api
npm ci
npx prisma generate
vercel --prod
```

### 3. Web Deployment
```bash
cd src/web
npm ci
vercel --prod
```

### 4. MCP Deployment
```bash
cd src/mcp
npm ci
npm run build
vercel --prod
```

## Post-Deployment Verification

- [ ] Health check endpoint responds
- [ ] Database connections working
- [ ] Redis cache responding
- [ ] API authentication working
- [ ] Stripe webhooks configured
- [ ] CORS configured correctly

## Environment Variables

### Required
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET` - JWT signing secret (min 32 chars)

### Optional (for payments)
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`

## Rollback Plan

1. Keep previous deployment URL active
2. Database migrations are backward-compatible
3. Vercel allows instant rollback to previous deployment

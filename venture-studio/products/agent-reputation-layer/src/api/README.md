# ARTL API - Vercel Configuration

This API is configured for deployment on Vercel as a serverless function.

## Deployment Steps

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel --prod
   ```

## Environment Variables

Configure these in the Vercel dashboard:

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Neon PostgreSQL connection string | Yes |
| `REDIS_URL` | Upstash Redis connection string | Yes |
| `JWT_SECRET` | Secret for JWT signing | Yes |
| `STRIPE_SECRET_KEY` | Stripe API key | Yes |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook secret | Yes |
| `FRONTEND_URL` | CORS allowed origin | Yes |

## Database Setup

1. Create a Neon project: https://neon.tech
2. Get the connection string
3. Run migrations:
   ```bash
   npx prisma migrate deploy
   ```

## API Endpoints

- `GET /api/v1/agents` - List agents
- `GET /api/v1/agents/:id` - Get agent details
- `POST /api/v1/agents` - Create agent
- `GET /api/v1/agents/:id/reputation` - Get reputation score
- `POST /api/v1/signals` - Submit trust signal
- `POST /api/v1/auth/login` - Authenticate
- `POST /api/v1/auth/register` - Register user

## Health Check

```bash
curl https://your-api.vercel.app/api/v1/health
```

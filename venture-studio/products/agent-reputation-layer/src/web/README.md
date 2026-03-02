# ARTL Web - Vercel Configuration

This Next.js 14 frontend is configured for deployment on Vercel.

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
| `NEXT_PUBLIC_API_URL` | API backend URL | Yes |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | Yes |

## Features

- Landing page with product overview
- Dashboard for managing agents
- Reputation explorer
- Payment/subscription management
- Agent verification workflows

## Build Configuration

The `next.config.js` is set to `output: 'standalone'` for optimal Vercel deployment.

## Custom Domain

To use a custom domain:
1. Go to Vercel dashboard
2. Select your project
3. Go to Settings > Domains
4. Add your domain

# SKILL.md — Monetization Agent

## Purpose
Specialized agent for designing and implementing business models and payment systems.

## Capabilities
- Design pricing tiers and value propositions
- Implement Stripe Checkout and Billing
- Configure subscription logic
- Set up usage-based billing
- Create affiliate/referral systems

## Pricing Models

### SaaS Tiers
| Tier | Price | Target |
|------|-------|--------|
| Free | $0 | Acquisition |
| Starter | $9-29/mo | Individual users |
| Pro | $49-99/mo | Power users |
| Enterprise | Custom | Teams |

### One-Time Purchase
- Early bird: $29 (first 100 customers)
- Launch price: $49
- Regular: $79

### Usage-Based
- Free tier: 100 requests/mo
- Pay-as-you-go: $0.01 per request
- Unlimited: $99/mo

## Stripe Integration Pattern
```tsx
// Checkout session creation
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: `${BASE_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${BASE_URL}/pricing`,
});
```

## Revenue Optimization
- Annual discounts (2 months free)
- Limited-time offers
- Upsell prompts at usage limits
- Referral credits

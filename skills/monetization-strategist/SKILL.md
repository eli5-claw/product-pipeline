# SKILL.md — Monetization Strategist

## Description
Designs comprehensive business models, pricing strategies, and revenue optimization for digital products. Specializes in SaaS pricing, token economics, and self-sustaining business models.

## When to Use
- Launching a new product and need pricing
- Optimizing existing pricing for conversion
- Designing token economics for Bankr/self-sustaining models
- Planning revenue diversification

## Input
```json
{
  "product": "saas|token|marketplace|info-product",
  "targetAudience": "indie-makers|enterprise|consumers|developers",
  "competitors": ["competitor1", "competitor2"],
  "costs": {
    "monthly": 0,
    "perUser": 0
  },
  "goals": {
    "mrrTarget": 0,
    "timeline": "6-months"
  }
}
```

## Process

### 1. Competitor Analysis
Research and document:
- Pricing models (tiered, usage-based, freemium)
- Price points and value metrics
- Strengths and weaknesses
- Market positioning

### 2. Value Metric Identification
What do users pay for?
- Users/seats
- Usage volume (events, API calls, storage)
- Features (good/better/best)
- Outcomes (ROI-based)

### 3. Pricing Tier Design
```json
{
  "tiers": [
    {
      "name": "Free",
      "price": 0,
      "limits": {},
      "features": [],
      "conversionStrategy": ""
    },
    {
      "name": "Pro",
      "price": 29,
      "limits": {},
      "features": [],
      "valueProposition": ""
    }
  ]
}
```

### 4. Token Economics (if applicable)
For Bankr/self-sustaining models:
- Token utility design
- Fee structure
- Buyback/burn mechanisms
- Revenue share model

### 5. Revenue Projections
```json
{
  "assumptions": {
    "conversionRate": 0.05,
    "churnRate": 0.05,
    "arpu": 25
  },
  "projections": {
    "month6": {},
    "month12": {}
  }
}
```

## Output Format

```markdown
# Monetization Strategy — [Product]

## Competitor Analysis
| Competitor | Price | Model | Strengths | Weaknesses |

## Pricing Model
### Free Tier
- Price: $0
- Limits: ...
- Conversion strategy: ...

### Paid Tiers
...

## Token Economics (if applicable)
- Token: $XXX
- Utility: ...
- Fee structure: ...

## Revenue Projections
| Month | Users | MRR | ARR |

## Implementation Checklist
- [ ] Stripe products created
- [ ] Pricing page built
- [ ] Trial flow configured
```

## Tools
- `web_search` — Competitor research
- `kimi_search` — Market analysis
- `write` — Save strategy document

## Example Usage
```
Design monetization for VibeAnalytics analytics dashboard.
Target: Indie makers, solopreneurs
Competitors: Plausible, PostHog, Simple Analytics
Goal: $10K MRR by month 12
```

## Specializations
- SaaS pricing optimization
- Bankr token integration
- Usage-based billing
- Freemium conversion
- Enterprise expansion

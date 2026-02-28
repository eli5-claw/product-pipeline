# Security Model

## Key Isolation

Private keys never leave Coinbase infrastructure:
- Keys generated in secure enclaves
- Agent authenticates via email OTP
- No direct key access

## Spending Guardrails

### Per-Session Limits
Set maximum spend per session:
```bash
npx awal config set sessionLimit 100  # $100 max per session
```

### Per-Transaction Limits
Set maximum per single transaction:
```bash
npx awal config set txLimit 50  # $50 max per tx
```

### Require Confirmation
Force manual confirmation for large transactions:
```bash
npx awal config set confirmThreshold 25  # Confirm if >$25
```

## KYT Screening

Know Your Transaction screening:
- Blocks high-risk addresses
- Flags suspicious patterns
- Compliance with regulations

## Best Practices

1. **Start with low limits** — Increase as needed
2. **Monitor transactions** — Regular review of activity
3. **Use dedicated email** — Separate from personal
4. **Enable confirmations** — For significant amounts

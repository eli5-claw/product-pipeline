# Polymarket Bot - Code Review Checklist

Use this checklist before deploying or committing changes.

## Security

- [ ] **No hardcoded secrets** - All credentials in `.env` only
- [ ] **Private key handling** - Uses environment variable, never logged
- [ ] **Input validation** - All external inputs sanitized
- [ ] **No eval/exec** - No dynamic code execution
- [ ] **Safe defaults** - Simulation mode default for new setups

## Error Handling

- [ ] **API call retries** - All Polymarket API calls wrapped in try/except
- [ ] **Balance checks** - Verifies sufficient balance before orders
- [ ] **Order validation** - Checks order response before assuming success
- [ ] **WebSocket reconnection** - Handles disconnects gracefully
- [ ] **Graceful degradation** - Bot continues if non-critical features fail

## Risk Management

- [ ] **Stop-loss enabled** - `ENABLE_STOP_LOSS=true` in production
- [ ] **Daily loss limit** - Set appropriate to your risk tolerance
- [ ] **Position sizing** - Mode appropriate for account size
- [ ] **Max concurrent markets** - Prevents over-exposure
- [ ] **Bail-out logic** - Sells one-sided fills before resolution

## Testing

- [ ] **Simulation mode passes** - Run full cycle without real orders
- [ ] **Stop-loss triggers correctly** - Test at various price levels
- [ ] **Position sizing math** - Verify calculations match expected
- [ ] **Redemption flow** - Test position redemption (if possible)
- [ ] **Error scenarios** - Test API failures, low balance, etc.

## Logging & Monitoring

- [ ] **All trades logged** - Entry, exit, P&L recorded
- [ ] **Errors logged** - Full stack traces for debugging
- [ ] **Performance metrics** - Fill rates, win rates tracked
- [ ] **Log rotation** - `bot.log` doesn't grow indefinitely
- [ ] **Alerts configured** - Telegram notifications if enabled

## Configuration

- [ ] **Entry price realistic** - 0.45 may not fill in current market
- [ ] **Position size appropriate** - Max 10-20% of account per trade
- [ ] **Order expiry reasonable** - 60 minutes default is fine
- [ ] **Check interval** - 10 seconds is aggressive, consider 30s
- [ ] **Auto-redeem enabled** - If builder credentials available

## Pre-Deployment

- [ ] **Read README.md** - Understand all configuration options
- [ ] **Test with small amount** - $50-100 first
- [ ] **Monitor first 24h** - Watch logs, verify behavior
- [ ] **Have exit plan** - Know how to stop bot and withdraw
- [ ] **Document changes** - Update this checklist if behavior changes

## Known Limitations

- [ ] **Fill rate uncertainty** - 45¢ fills not guaranteed
- [ ] **One-sided fill risk** - Can lose entire position
- [ ] **API rate limits** - Aggressive checking may hit limits
- [ ] **Gas costs** - Even "gasless" redeems have costs
- [ ] **Market liquidity** - Large positions move the market

## Sign-off

| Check | Date | Result |
|-------|------|--------|
| Security review | | |
| Simulation test | | |
| Small live test | | |
| Full deployment | | |

Reviewer: _________________

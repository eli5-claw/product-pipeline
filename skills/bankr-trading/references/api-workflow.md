# API Workflow

## Direct REST API Usage

No CLI required. Use any HTTP client.

### Authentication

Header: `X-API-Key: bk_YOUR_KEY`

### Submit a Prompt

```bash
curl -X POST "https://api.bankr.bot/agent/prompt" \
  -H "X-API-Key: bk_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is my ETH balance?"
  }'
```

Response:
```json
{
  "jobId": "job_abc123",
  "threadId": "thr_xyz789",
  "status": "pending"
}
```

### Poll for Results

```bash
curl "https://api.bankr.bot/agent/job/job_abc123" \
  -H "X-API-Key: bk_YOUR_KEY"
```

Response (completed):
```json
{
  "jobId": "job_abc123",
  "status": "completed",
  "response": "Your ETH balance is 2.5 ETH ($6,250)"
}
```

### Continue Conversation

Pass `threadId` to maintain context:

```bash
curl -X POST "https://api.bankr.bot/agent/prompt" \
  -H "X-API-Key: bk_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "And my SOL balance?",
    "threadId": "thr_xyz789"
  }'
```

### Sign/Submit Raw Transactions

```bash
# Sign a message
curl -X POST "https://api.bankr.bot/agent/sign" \
  -H "X-API-Key: bk_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello world"
  }'

# Submit raw transaction
curl -X POST "https://api.bankr.bot/agent/submit" \
  -H "X-API-Key: bk_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "base",
    "tx": "0x..."
  }'
```

## Job States

- `pending` — Submitted, waiting to process
- `processing` — Currently executing
- `completed` — Success, response available
- `failed` — Error occurred
- `cancelled` — User or system cancelled

## Error Handling

```bash
# Check for errors
if [ "$STATUS" = "failed" ]; then
  echo "$RESULT" | jq -r '.error'
fi
```

# LLM Gateway

## Multi-Model API Access

Bankr provides a unified API for multiple LLM models, funded by your Bankr wallet.

## Endpoint

```
https://llm.bankr.bot
```

## Authentication

Same API key as trading: `X-API-Key: bk_YOUR_KEY`

## Available Models

| Model | Provider | Best For |
|-------|----------|----------|
| gpt-4o | OpenAI | General purpose |
| claude-3-opus | Anthropic | Complex reasoning |
| gemini-pro | Google | Multimodal |
| llama-3 | Meta | Open source |

## Usage

```bash
curl -X POST "https://llm.bankr.bot/v1/chat/completions" \
  -H "X-API-Key: bk_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "Analyze this trade"}
    ]
  }'
```

## Pricing

Deducted from Bankr wallet automatically:
- Input tokens: $0.01 per 1K tokens
- Output tokens: $0.03 per 1K tokens

## Enable LLM Gateway

During login:
```bash
bankr login email user@example.com --code 123456 --llm
```

Or separately:
```bash
bankr config set llmKey bk_YOUR_LLM_KEY
```

## Use Cases

- **Trade analysis** — LLM interprets market data
- **Strategy generation** — AI creates trading strategies
- **Risk assessment** — LLM evaluates portfolio risk
- **Natural language queries** — "Should I buy ETH now?"

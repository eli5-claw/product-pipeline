# ARTL MCP Server - Vercel Configuration

MCP (Model Context Protocol) server for agent-native reputation queries.

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

| Variable | Description | Required |
|----------|-------------|----------|
| `API_URL` | ARTL API backend URL | Yes |
| `API_KEY` | API key for authentication | Yes |

## MCP Endpoints

- `POST /mcp/query` - Query agent reputation
- `GET /mcp/agents/:did` - Get agent by DID
- `POST /mcp/verify` - Verify agent identity

## Integration

Use with any MCP-compatible client:

```json
{
  "mcpServers": {
    "artl": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-artl"],
      "env": {
        "ARTL_API_URL": "https://your-mcp-server.vercel.app"
      }
    }
  }
}
```

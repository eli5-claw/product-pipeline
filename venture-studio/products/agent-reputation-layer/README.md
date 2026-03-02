# Agent Reputation & Trust Layer (ARTL) v1.0

> Universal reputation system for AI agents across MCP, A2A, and blockchain protocols.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/eli5/artl)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue.svg)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![NestJS](https://img.shields.io/badge/NestJS-10-red.svg)](https://nestjs.com/)

## 🎯 Overview

ARTL provides a decentralized reputation oracle that:
1. **Ingests** trust signals from multiple sources (A2A, MCP, on-chain, manual attestations)
2. **Aggregates** signals into a unified reputation score (0-1000)
3. **Exposes** scores via API and MCP/A2A protocols for agent consumption
4. **Enables** reputation-weighted transactions and dispute resolution

### Key Features

- **🔐 DID-Based Identity**: Decentralized identifiers for cross-platform agent recognition
- **📊 0-1000 Reputation Score**: Granular trust scoring with confidence metrics
- **🔄 Multi-Protocol Support**: Native MCP and A2A protocol integration
- **⚡ Real-time API**: RESTful API for reputation queries and signal submission
- **🎨 Interactive Dashboard**: Web interface for reputation exploration
- **🛡️ Dispute Resolution**: Built-in arbitration system for trust violations
- **✅ Verification Workflows**: Email, domain, and enterprise verification

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Web Frontend  │────▶│   API Backend   │────▶│   PostgreSQL    │
│   (Next.js 16)  │     │   (NestJS)      │     │   (Database)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   MCP Server    │     │     Redis       │     │   A2A Gateway   │
│   (Reputation   │     │   (Cache)       │     │   (Protocol)    │
│    Tools)       │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Components

| Component | Technology | Description |
|-----------|------------|-------------|
| **Web** | Next.js 16 + TypeScript | Dashboard, landing page, reputation explorer |
| **API** | NestJS + Prisma | Core reputation engine, REST API |
| **MCP** | TypeScript MCP SDK | Protocol-native reputation tools |
| **Database** | PostgreSQL 16 | Agent data, trust signals, reputation history |
| **Cache** | Redis 7 | Hot scores, rate limiting, sessions |

## 🚀 Quick Start

### Prerequisites

- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 16 (or use Docker)
- Redis 7 (or use Docker)

### Installation

```bash
# Clone the repository
git clone https://github.com/eli5/artl.git
cd artl

# Start infrastructure services
docker-compose up -d postgres redis

# Install API dependencies
cd src/api
npm install
npx prisma migrate dev
npx prisma generate
npm run start:dev

# In a new terminal, install Web dependencies
cd src/web
npm install
npm run dev

# In a new terminal, install MCP dependencies
cd src/mcp
npm install
npm run dev
```

### Access Services

- **Web Dashboard**: http://localhost:3000
- **API**: http://localhost:3001/api/v1
- **API Documentation**: http://localhost:3001/api/docs

## 📖 API Reference

### Authentication

```bash
# Register an agent
POST /api/v1/agents
Authorization: Bearer {jwt_token}
{
  "name": "My Research Agent",
  "description": "Autonomous research assistant",
  "type": "autonomous"
}

# Response includes API key for subsequent requests
{
  "agent": { ... },
  "apiKey": "artl_live_xxxxxxxxxxxx"
}
```

### Reputation Queries

```bash
# Get agent reputation
GET /api/v1/agents/{did}/reputation

# Query multiple agents
POST /api/v1/reputation/query
{
  "agents": ["did:artl:uuid1", "did:artl:uuid2"]
}
```

### Submit Trust Signals

```bash
POST /api/v1/signals
Authorization: Bearer {api_key}
{
  "agentId": "did:artl:uuid",
  "type": "transaction",
  "subtype": "successful_payment",
  "value": 0.8,
  "confidence": 0.95,
  "metadata": {
    "transactionId": "txn_123",
    "amount": 100.00,
    "currency": "USD"
  }
}
```

## 🔌 MCP Integration

ARTL exposes reputation tools as an MCP server:

```json
{
  "mcpServers": {
    "artl": {
      "command": "npx",
      "args": ["@eli5/artl-mcp"],
      "env": {
        "ARTL_API_KEY": "your_api_key"
      }
    }
  }
}
```

### Available Tools

- `get_reputation_score` - Get reputation score by DID
- `verify_agent` - Verify agent meets minimum requirements
- `compare_agents` - Compare multiple agents
- `submit_transaction_signal` - Submit post-transaction feedback

## 🧮 Reputation Scoring

### Score Breakdown (0-1000)

| Category | Weight | Description |
|----------|--------|-------------|
| Transaction History | 0-250 | Payment and commercial transaction history |
| Protocol Compliance | 0-250 | MCP/A2A protocol adherence, uptime |
| Community Trust | 0-250 | Reviews, attestations, endorsements |
| Verification Level | 0-250 | Email, domain, enterprise, KYC verification |

### Time Decay

Signals lose relevance over time using exponential decay:
```
weight = original_weight × exp(-age / 365_days)
```

### Confidence Score

Confidence (0-1) is calculated based on:
- Signal volume and diversity
- Source verification status
- Signal age distribution

## 🛠️ Development

### Project Structure

```
artl/
├── src/
│   ├── api/           # NestJS API backend
│   │   ├── src/
│   │   │   ├── agents/        # Agent management
│   │   │   ├── reputation/    # Scoring engine
│   │   │   ├── signals/       # Trust signal ingestion
│   │   │   ├── auth/          # Authentication
│   │   │   └── prisma/        # Database service
│   │   └── prisma/
│   │       └── schema.prisma  # Database schema
│   ├── web/           # Next.js frontend
│   │   └── app/
│   │       ├── sections/      # Landing page sections
│   │       └── dashboard/     # Reputation dashboard
│   ├── mcp/           # MCP server
│   │   └── src/
│   │       └── index.ts       # MCP tools implementation
│   └── shared/        # Shared types and schemas
│       ├── types.ts
│       └── schemas.ts
├── docker-compose.yml
└── README.md
```

### Database Schema

The system uses PostgreSQL with the following core entities:

- **agents** - Agent profiles with DID-based identity
- **trust_signals** - Individual trust signals from various sources
- **attestations** - Manual verifications and endorsements
- **disputes** - Dispute records and resolutions
- **reputation_history** - Time-series reputation snapshots

See `src/api/prisma/schema.prisma` for complete schema.

### Running Tests

```bash
# API tests
cd src/api
npm test

# Web tests
cd src/web
npm test

# MCP tests
cd src/mcp
npm test
```

## 🚀 Deployment

### Docker Compose (Recommended for Self-Hosting)

```bash
docker-compose up -d
```

### Vercel (Serverless)

```bash
# Deploy API
cd src/api
vercel --prod

# Deploy Web
cd src/web
vercel --prod

# Deploy MCP
cd src/mcp
vercel --prod
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📊 Monitoring

### Health Checks

- API: `GET /health`
- Database: Prisma connection check
- Redis: Ping check

### Metrics

- Reputation calculation latency
- API request rate and latency
- Signal ingestion rate
- Score distribution

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Documentation](https://docs.artl.io)
- [API Reference](https://api.artl.io/docs)
- [MCP Specification](https://modelcontextprotocol.io)
- [A2A Protocol](https://google.github.io/A2A/)

## 💡 Roadmap

- [x] Core reputation scoring engine
- [x] MCP protocol integration
- [x] REST API
- [x] Web dashboard
- [ ] A2A protocol gateway
- [ ] On-chain score anchoring
- [ ] Decentralized attestation network
- [ ] Mobile SDK
- [ ] Enterprise SSO integration

---

Built with ❤️ by [Eli5 Venture Studio](https://eli5.io)

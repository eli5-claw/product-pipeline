# SPEC.md - Agent Reputation & Trust Layer (ARTL)

**Product:** Agent Reputation & Trust Layer  
**Code Name:** trustlayer / ARTL  
**Status:** Specification Complete  
**Date:** March 2, 2026  
**Architect:** Eli5 Venture Studio Architect Agent  
**Opportunity Score:** 73/100 (Highest from Scout Findings)

---

## 1. Executive Summary

### The Problem
As multi-agent systems proliferate (A2A protocol launched by Google in April 2025, MCP gaining traction), agents need to verify each other's trustworthiness before executing transactions or sharing sensitive data. Current solutions are fragmented — Visa, Cloudflare, and ERC-8004 each have proprietary scoring, but there's no universal, cross-protocol reputation layer.

### The Solution
ARTL (Agent Reputation & Trust Layer) is a universal, cross-protocol reputation system that aggregates trust signals from MCP, A2A, and on-chain activity to provide a standardized reputation score for any agent in the ecosystem.

### Dual-Market Value Proposition

**Human:** "Verify AI vendors and freelancers with a standardized trust score — like a credit score for agents"

**Agent:** "Query reputation programmatically to assess risk before transacting with other agents"

---

## 2. Problem Statement

### 2.1 Current Pain Points

**For Humans:**
- Enterprises struggle to vet AI vendors using standardized trust metrics
- Freelancers/agencies cannot prove reliability to clients via verifiable reputation
- No way to compare agent service providers objectively
- Fragmented trust signals across different platforms and protocols

**For Agents:**
- Cannot safely transact without trust verification — blocking adoption
- No standardized way to assess risk before collaboration
- Each protocol (A2A, MCP) has isolated trust mechanisms
- Reputation doesn't travel across platforms

### 2.2 Market Context
- Google A2A Protocol has 50+ enterprise partners (Atlassian, Salesforce, SAP, Workday)
- PayOS and AP2 protocol emerging for agent payments
- Reddit threads show developers struggling with "how do agents trust each other"
- No dominant player in cross-protocol agent reputation

---

## 3. Solution Overview

### 3.1 Core Concept
ARTL provides a decentralized reputation oracle that:
1. **Ingests** trust signals from multiple sources (A2A, MCP, on-chain, manual attestations)
2. **Aggregates** signals into a unified reputation score (0-1000)
3. **Exposes** scores via API and MCP/A2A protocols for agent consumption
4. **Enables** reputation-weighted transactions and dispute resolution

### 3.2 Key Features

**For Humans:**
- Reputation dashboard for agent vendors
- Verification badges and trust certificates
- Dispute filing and resolution
- Enterprise compliance reporting

**For Agents:**
- Real-time reputation queries via API
- Reputation-weighted payment escrow
- Automated risk assessment
- Cross-platform reputation portability

### 3.3 Personas

**Human Persona 1: Enterprise Procurement Manager (Sarah)**
- Role: Evaluating AI vendors for customer service automation
- Pain: No standardized way to compare vendor trustworthiness
- Goal: Vet vendors using objective, third-party reputation scores
- Tech savvy: Medium (uses dashboards, not APIs)

**Human Persona 2: AI Freelancer (Marcus)**
- Role: Builds custom agents for clients
- Pain: Hard to prove reliability to new clients
- Goal: Display verified reputation score to win more business
- Tech savvy: High (developer)

**Agent Persona: Autonomous Procurement Agent**
- Workflow: Needs to purchase services from other agents
- Pain: Must assess risk before each transaction
- Goal: Query reputation, set risk thresholds, auto-approve low-risk transactions

---

## 4. System Architecture

### 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                       │
├─────────────────────────────┬───────────────────────────────────────────────┤
│   Human Web Interface       │   Agent API Clients                           │
│   (Next.js Dashboard)       │   (MCP / A2A / REST)                          │
└──────────────┬──────────────┴───────────────────────┬───────────────────────┘
               │                                      │
               ▼                                      ▼
┌─────────────────────────────┐         ┌─────────────────────────────────────┐
│   Web Gateway (Next.js)     │         │   Protocol Gateways                 │
│   - SSR for SEO             │         │   ┌─────────────────────────────┐   │
│   - Auth & sessions         │         │   │   MCP Gateway               │   │
│   - Dashboard UI            │         │   │   - tools/reputation        │   │
└──────────────┬──────────────┘         │   └─────────────────────────────┘   │
               │                        │   ┌─────────────────────────────┐   │
               │                        │   │   A2A Gateway               │   │
               │                        │   │   - AgentCard integration   │   │
               │                        │   └─────────────────────────────┘   │
               │                        └──────────────┬──────────────────────┘
               │                                       │
               └───────────────────┬───────────────────┘
                                   ▼
                    ┌─────────────────────────────┐
                    │      API Gateway            │
                    │   - Rate limiting           │
                    │   - Auth (JWT/API keys)     │
                    │   - Request routing         │
                    └──────────────┬──────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│  Reputation     │    │  Signal Ingestion   │    │  Attestation        │
│  Engine         │    │  Service            │    │  Service            │
│  - Score calc   │    │  - A2A monitors     │    │  - Manual reviews   │
│  - Decay model  │    │  - MCP monitors     │    │  - Enterprise       │
│  - Weighting    │    │  - On-chain sync    │    │    verification     │
└────────┬────────┘    └──────────┬──────────┘    └──────────┬──────────┘
         │                        │                          │
         └────────────────────────┼──────────────────────────┘
                                  ▼
                    ┌─────────────────────────────┐
                    │      Core Services          │
                    │  ┌───────────────────────┐  │
                    │  │   Identity Registry   │  │
                    │  │   - Agent DID         │  │
                    │  │   - Cross-platform    │  │
                    │  │     identity          │  │
                    │  └───────────────────────┘  │
                    │  ┌───────────────────────┐  │
                    │  │   Dispute Resolution  │  │
                    │  │   - Escrow management │  │
                    │  │   - Arbitration       │  │
                    │  └───────────────────────┘  │
                    │  ┌───────────────────────┐  │
                    │  │   Analytics & Scoring │  │
                    │  │   - Trend analysis    │  │
                    │  │   - Fraud detection   │  │
                    │  └───────────────────────┘  │
                    └──────────────┬──────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│  PostgreSQL     │    │  Redis              │    │  Blockchain         │
│  (Primary DB)   │    │  (Cache/Sessions)   │    │  Anchor (Optional)  │
│  - Agents       │    │  - Hot scores       │    │  - Score anchoring  │
│  - Reputation   │    │  - Rate limits      │    │  - Dispute log      │
│  - Transactions │    │  - Pub/sub          │    │  - Attestations     │
└─────────────────┘    └─────────────────────┘    └─────────────────────┘
```

### 4.2 Component Descriptions

#### 4.2.1 Web Gateway
- **Purpose:** Human-facing interface for reputation management
- **Technology:** Next.js 14 with App Router
- **Features:**
  - Agent reputation dashboards
  - Verification workflows
  - Dispute filing and tracking
  - Enterprise compliance reporting

#### 4.2.2 MCP Gateway
- **Purpose:** MCP-native reputation queries
- **Technology:** TypeScript MCP SDK
- **Features:**
  - `get_reputation_score` tool
  - `verify_agent` tool
  - `submit_attestation` tool
  - Streaming reputation updates

#### 4.2.3 A2A Gateway
- **Purpose:** A2A protocol integration
- **Technology:** Node.js / A2A SDK
- **Features:**
  - AgentCard reputation extension
  - Task-level reputation requirements
  - Reputation-weighted task routing

#### 4.2.4 Reputation Engine
- **Purpose:** Core scoring algorithm
- **Technology:** Python / FastAPI
- **Features:**
  - Multi-factor reputation calculation
  - Time-decay for old signals
  - Confidence scoring
  - Anomaly detection

#### 4.2.5 Signal Ingestion Service
- **Purpose:** Collect trust signals from external sources
- **Technology:** Node.js / BullMQ workers
- **Features:**
  - A2A protocol monitors
  - MCP server interaction tracking
  - On-chain transaction indexing
  - Third-party API integrations

#### 4.2.6 Attestation Service
- **Purpose:** Manual verification and enterprise validation
- **Technology:** Node.js / NestJS
- **Features:**
  - Enterprise verification workflows
  - KYC/AML integration hooks
  - Manual review queue
  - Compliance reporting

---

## 5. Core Data Models

### 5.1 Agent Entity

```typescript
interface Agent {
  // Identity
  id: string;                    // UUID v4
  did: string;                   // Decentralized Identifier
  
  // Basic Info
  name: string;
  description: string;
  type: 'individual' | 'enterprise' | 'service' | 'autonomous';
  
  // Platform Identities (cross-platform linking)
  identities: {
    a2a?: A2AIdentity;
    mcp?: MCPIdentity;
    blockchain?: BlockchainIdentity[];
    web?: WebIdentity[];
  };
  
  // Reputation
  reputation: ReputationScore;
  reputationHistory: ReputationSnapshot[];
  
  // Verification
  verificationStatus: VerificationStatus;
  attestations: Attestation[];
  
  // Ownership
  ownerId?: string;              // For human-owned agents
  organizationId?: string;       // For enterprise agents
  
  // Metadata
  createdAt: Date;
  updatedAt: Date;
  lastActiveAt: Date;
}

interface A2AIdentity {
  agentId: string;
  endpoint: string;
  agentCardUrl: string;
  verified: boolean;
}

interface MCPIdentity {
  serverName: string;
  registryUrl?: string;
  verified: boolean;
}

interface BlockchainIdentity {
  chain: string;
  address: string;
  verified: boolean;
}

interface WebIdentity {
  domain: string;
  verified: boolean;             // DNS TXT record verification
}

interface ReputationScore {
  overall: number;               // 0-1000
  confidence: number;            // 0-1
  breakdown: {
    transactionHistory: number;  // 0-250
    protocolCompliance: number;  // 0-250
    communityTrust: number;      // 0-250
    verificationLevel: number;   // 0-250
  };
  lastCalculatedAt: Date;
  nextRecalculationAt: Date;
}

interface ReputationSnapshot {
  timestamp: Date;
  score: number;
  confidence: number;
  signalsCount: number;
}

interface VerificationStatus {
  level: 'none' | 'email' | 'domain' | 'enterprise' | 'kyc';
  verifiedAt?: Date;
  expiresAt?: Date;
  method: string;
}
```

### 5.2 Trust Signal Entity

```typescript
interface TrustSignal {
  id: string;
  agentId: string;
  
  // Signal Source
  source: SignalSource;
  sourceId: string;
  
  // Signal Type
  type: SignalType;
  subtype: string;
  
  // Signal Value
  value: number;                 // -1 to +1 (negative to positive)
  weight: number;                // Signal importance (0-1)
  confidence: number;            // Confidence in signal (0-1)
  
  // Context
  metadata: {
    transactionId?: string;
    counterpartyId?: string;
    amount?: number;
    currency?: string;
    description?: string;
    evidenceUrl?: string;
    [key: string]: any;
  };
  
  // Timestamps
  occurredAt: Date;
  recordedAt: Date;
  expiresAt?: Date;              // For time-decay
  
  // Verification
  verified: boolean;
  verificationMethod?: string;
}

interface SignalSource {
  type: 'a2a' | 'mcp' | 'blockchain' | 'manual' | 'api' | 'enterprise';
  name: string;
  url?: string;
  verified: boolean;
}

type SignalType = 
  | 'transaction'           // Payment/commercial transaction
  | 'task_completion'       // A2A task completion
  | 'protocol_compliance'   // MCP/A2A protocol adherence
  | 'dispute'              // Dispute filed or resolved
  | 'attestation'          // Manual verification/endorsement
  | 'security_incident'    // Security breach or vulnerability
  | 'review'               // User/agent review
  | 'uptime'               // Service availability
  | 'response_time';       // Performance metric
```

### 5.3 Attestation Entity

```typescript
interface Attestation {
  id: string;
  agentId: string;
  
  // Attester
  attesterType: 'individual' | 'enterprise' | 'protocol';
  attesterId: string;
  attesterReputation: number;    // Attester's reputation at time of attestation
  
  // Attestation Content
  type: AttestationType;
  claim: string;
  evidenceUrls: string[];
  
  // Impact
  weight: number;                // Calculated based on attester reputation
  status: 'pending' | 'verified' | 'rejected' | 'revoked';
  
  // Timestamps
  createdAt: Date;
  verifiedAt?: Date;
  expiresAt?: Date;
}

type AttestationType =
  | 'identity_verification'
  | 'security_audit'
  | 'performance_test'
  | 'compliance_certification'
  | 'business_verification'
  | 'skill_endorsement';
```

### 5.4 Dispute Entity

```typescript
interface Dispute {
  id: string;
  
  // Parties
  initiatorId: string;
  respondentId: string;
  
  // Dispute Details
  type: DisputeType;
  description: string;
  evidence: DisputeEvidence[];
  amount?: number;
  currency?: string;
  
  // Escrow
  escrowId?: string;
  escrowStatus: 'none' | 'held' | 'released_to_initiator' | 'released_to_respondent' | 'split';
  
  // Resolution
  status: 'open' | 'under_review' | 'resolved' | 'escalated';
  resolution?: DisputeResolution;
  
  // Impact
  initiatorImpact: number;       // Reputation impact on initiator
  respondentImpact: number;      // Reputation impact on respondent
  
  // Timestamps
  createdAt: Date;
  resolvedAt?: Date;
}

interface DisputeEvidence {
  type: 'transaction_log' | 'communication' | 'contract' | 'expert_opinion' | 'other';
  url: string;
  submittedBy: string;
  submittedAt: Date;
}

interface DisputeResolution {
  outcome: 'initiator_wins' | 'respondent_wins' | 'split' | 'dismissed';
  reason: string;
  resolvedBy: 'automated' | 'mediator' | 'arbitrator';
  mediatorId?: string;
}
```

### 5.5 Database Schema (PostgreSQL)

```sql
-- Core tables
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    did VARCHAR(255) UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL CHECK (type IN ('individual', 'enterprise', 'service', 'autonomous')),
    
    -- JSONB for flexible identity storage
    identities JSONB NOT NULL DEFAULT '{}',
    
    -- Reputation stored as JSONB for flexibility
    reputation JSONB NOT NULL DEFAULT '{
        "overall": 500,
        "confidence": 0,
        "breakdown": {
            "transactionHistory": 0,
            "protocolCompliance": 0,
            "communityTrust": 0,
            "verificationLevel": 0
        }
    }',
    
    verification_status JSONB NOT NULL DEFAULT '{"level": "none"}',
    
    owner_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_active_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Full-text search
    search_vector tsvector
);

-- Trust signals
CREATE TABLE trust_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    
    source_type VARCHAR(50) NOT NULL,
    source_name VARCHAR(255) NOT NULL,
    source_url TEXT,
    source_verified BOOLEAN DEFAULT FALSE,
    
    signal_type VARCHAR(50) NOT NULL,
    signal_subtype VARCHAR(100),
    
    value DECIMAL(4,3) NOT NULL CHECK (value >= -1 AND value <= 1),
    weight DECIMAL(3,2) NOT NULL CHECK (weight >= 0 AND weight <= 1),
    confidence DECIMAL(3,2) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    
    metadata JSONB DEFAULT '{}',
    
    occurred_at TIMESTAMPTZ NOT NULL,
    recorded_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    
    verified BOOLEAN DEFAULT FALSE,
    verification_method VARCHAR(100),
    
    -- Index for time-decay calculations
    CONSTRAINT valid_signal CHECK (value >= -1 AND value <= 1)
);

-- Attestations
CREATE TABLE attestations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    
    attester_type VARCHAR(50) NOT NULL,
    attester_id VARCHAR(255) NOT NULL,
    attester_reputation INTEGER,
    
    attestation_type VARCHAR(100) NOT NULL,
    claim TEXT NOT NULL,
    evidence_urls TEXT[],
    
    weight DECIMAL(3,2),
    status VARCHAR(50) DEFAULT 'pending',
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    verified_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ
);

-- Disputes
CREATE TABLE disputes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    initiator_id UUID NOT NULL REFERENCES agents(id),
    respondent_id UUID NOT NULL REFERENCES agents(id),
    
    dispute_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    evidence JSONB DEFAULT '[]',
    
    amount DECIMAL(18, 8),
    currency VARCHAR(10),
    
    escrow_id VARCHAR(255),
    escrow_status VARCHAR(50) DEFAULT 'none',
    
    status VARCHAR(50) DEFAULT 'open',
    resolution JSONB,
    
    initiator_impact DECIMAL(4,3) DEFAULT 0,
    respondent_impact DECIMAL(4,3) DEFAULT 0,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

-- Reputation history (time-series)
CREATE TABLE reputation_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    overall_score INTEGER NOT NULL CHECK (overall_score >= 0 AND overall_score <= 1000),
    confidence DECIMAL(3,2) NOT NULL,
    signals_count INTEGER NOT NULL,
    breakdown JSONB NOT NULL
);

-- Organizations
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    domain_verified BOOLEAN DEFAULT FALSE,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Users (human accounts)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- API Keys for agent authentication
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    key_hash VARCHAR(255) NOT NULL UNIQUE,
    key_prefix VARCHAR(8) NOT NULL,
    name VARCHAR(255),
    scopes TEXT[],
    last_used_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    revoked_at TIMESTAMPTZ
);

-- Indexes
CREATE INDEX idx_agents_did ON agents(did);
CREATE INDEX idx_agents_type ON agents(type);
CREATE INDEX idx_agents_owner ON agents(owner_id);
CREATE INDEX idx_agents_org ON agents(organization_id);
CREATE INDEX idx_agents_search ON agents USING GIN(search_vector);
CREATE INDEX idx_agents_reputation ON agents((reputation->>'overall'));

CREATE INDEX idx_signals_agent ON trust_signals(agent_id);
CREATE INDEX idx_signals_type ON trust_signals(signal_type);
CREATE INDEX idx_signals_occurred ON trust_signals(occurred_at);
CREATE INDEX idx_signals_expires ON trust_signals(expires_at);

CREATE INDEX idx_attestations_agent ON attestations(agent_id);
CREATE INDEX idx_attestations_status ON attestations(status);

CREATE INDEX idx_disputes_initiator ON disputes(initiator_id);
CREATE INDEX idx_disputes_respondent ON disputes(respondent_id);
CREATE INDEX idx_disputes_status ON disputes(status);

CREATE INDEX idx_reputation_history_agent ON reputation_history(agent_id);
CREATE INDEX idx_reputation_history_time ON reputation_history(timestamp);

-- Full-text search update trigger
CREATE OR REPLACE FUNCTION update_agent_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.did, '')), 'A');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER agent_search_update
    BEFORE INSERT OR UPDATE ON agents
    FOR EACH ROW
    EXECUTE FUNCTION update_agent_search_vector();

-- Partition reputation_history by month for performance
CREATE TABLE reputation_history_partitioned (
    LIKE reputation_history INCLUDING ALL
) PARTITION BY RANGE (timestamp);

-- Create initial partitions
CREATE TABLE reputation_history_2026_01 PARTITION OF reputation_history_partitioned
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE reputation_history_2026_02 PARTITION OF reputation_history_partitioned
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE reputation_history_2026_03 PARTITION OF reputation_history_partitioned
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
```

---

## 6. API Specification

### 6.1 REST API

#### Authentication
```http
POST /api/v1/auth/token
Content-Type: application/json

{
  "grant_type": "client_credentials",
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "scope": "read:reputation write:signals"
}
```

#### Agents

**Register Agent**
```http
POST /api/v1/agents
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "My Research Agent",
  "description": "Autonomous research assistant",
  "type": "autonomous",
  "identities": {
    "a2a": {
      "agentId": "research-agent-123",
      "endpoint": "https://agent.example.com/a2a"
    }
  }
}

Response 201:
{
  "id": "uuid",
  "did": "did:artl:uuid",
  "name": "My Research Agent",
  "reputation": {
    "overall": 500,
    "confidence": 0,
    "breakdown": {
      "transactionHistory": 0,
      "protocolCompliance": 0,
      "communityTrust": 0,
      "verificationLevel": 0
    }
  },
  "apiKey": "artl_live_xxxxxxxxxxxx"  // Only shown once
}
```

**Get Agent Reputation**
```http
GET /api/v1/agents/{did}/reputation
Authorization: Bearer {token}

Response 200:
{
  "agentId": "uuid",
  "did": "did:artl:uuid",
  "reputation": {
    "overall": 847,
    "confidence": 0.87,
    "breakdown": {
      "transactionHistory": 210,
      "protocolCompliance": 245,
      "communityTrust": 198,
      "verificationLevel": 194
    },
    "lastCalculatedAt": "2026-03-02T10:30:00Z"
  },
  "verificationStatus": {
    "level": "enterprise",
    "verifiedAt": "2026-02-15T08:00:00Z"
  },
  "signalCounts": {
    "total": 156,
    "positive": 142,
    "negative": 8,
    "neutral": 6
  }
}
```

**Query Reputation (Bulk)**
```http
POST /api/v1/reputation/query
Authorization: Bearer {token}
Content-Type: application/json

{
  "agents": ["did:artl:uuid1", "did:artl:uuid2"],
  "includeHistory": false,
  "includeSignals": false
}

Response 200:
{
  "results": [
    {
      "did": "did:artl:uuid1",
      "reputation": { ... },
      "found": true
    },
    {
      "did": "did:artl:uuid2",
      "found": false,
      "message": "Agent not found"
    }
  ]
}
```

#### Trust Signals

**Submit Signal**
```http
POST /api/v1/signals
Authorization: Bearer {token}
Content-Type: application/json

{
  "agentId": "did:artl:uuid",
  "type": "transaction",
  "subtype": "successful_payment",
  "value": 0.8,
  "confidence": 0.95,
  "metadata": {
    "transactionId": "txn_123",
    "counterpartyId": "did:artl:other",
    "amount": 100.00,
    "currency": "USD",
    "description": "API service payment"
  },
  "occurredAt": "2026-03-01T14:30:00Z"
}

Response 201:
{
  "id": "uuid",
  "status": "recorded",
  "estimatedImpact": 2.5,
  "recalculationScheduled": true
}
```

**List Agent Signals**
```http
GET /api/v1/agents/{did}/signals?type=transaction&limit=50
Authorization: Bearer {token}

Response 200:
{
  "data": [
    {
      "id": "uuid",
      "type": "transaction",
      "value": 0.8,
      "confidence": 0.95,
      "metadata": { ... },
      "occurredAt": "2026-03-01T14:30:00Z",
      "verified": true
    }
  ],
  "pagination": {
    "page": 1,
    "perPage": 50,
    "total": 156
  }
}
```

#### Attestations

**Submit Attestation**
```http
POST /api/v1/attestations
Authorization: Bearer {token}
Content-Type: application/json

{
  "agentId": "did:artl:uuid",
  "type": "security_audit",
  "claim": "Passed SOC 2 Type II audit",
  "evidenceUrls": ["https://example.com/audit.pdf"],
  "expiresAt": "2027-03-01T00:00:00Z"
}

Response 201:
{
  "id": "uuid",
  "status": "pending",
  "estimatedWeight": 0.15
}
```

#### Disputes

**File Dispute**
```http
POST /api/v1/disputes
Authorization: Bearer {token}
Content-Type: application/json

{
  "respondentId": "did:artl:uuid",
  "type": "non_delivery",
  "description": "Service was not delivered as agreed",
  "amount": 500.00,
  "currency": "USD",
  "evidence": [
    {
      "type": "communication",
      "url": "https://example.com/evidence1.pdf"
    }
  ],
  "requestEscrow": true
}

Response 201:
{
  "id": "uuid",
  "status": "open",
  "escrowId": "esc_123",
  "estimatedResolution": "5-7 days"
}
```

### 6.2 Reputation Score Calculation

```typescript
// Reputation Score Formula
function calculateReputationScore(agent: Agent): ReputationScore {
  const signals = getActiveSignals(agent.id);
  
  // 1. Transaction History (0-250 points)
  const transactionScore = calculateTransactionScore(
    signals.filter(s => s.type === 'transaction')
  );
  
  // 2. Protocol Compliance (0-250 points)
  const complianceScore = calculateComplianceScore(
    signals.filter(s => s.type === 'protocol_compliance' || s.type === 'uptime')
  );
  
  // 3. Community Trust (0-250 points)
  const communityScore = calculateCommunityScore(
    signals.filter(s => s.type === 'review' || s.type === 'attestation'),
    agent.attestations
  );
  
  // 4. Verification Level (0-250 points)
  const verificationScore = calculateVerificationScore(
    agent.verificationStatus,
    agent.attestations
  );
  
  // Calculate confidence based on signal volume and diversity
  const confidence = calculateConfidence(signals);
  
  // Apply time-decay to old signals
  const decayedSignals = applyTimeDecay(signals);
  
  // Calculate overall score
  const overall = Math.round(
    transactionScore + 
    complianceScore + 
    communityScore + 
    verificationScore
  );
  
  return {
    overall: Math.min(1000, Math.max(0, overall)),
    confidence,
    breakdown: {
      transactionHistory: transactionScore,
      protocolCompliance: complianceScore,
      communityTrust: communityScore,
      verificationLevel: verificationScore
    },
    lastCalculatedAt: new Date(),
    nextRecalculationAt: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours
  };
}

// Time-decay function (signals lose relevance over time)
function applyTimeDecay(signals: TrustSignal[]): TrustSignal[] {
  const now = Date.now();
  const ONE_YEAR = 365 * 24 * 60 * 60 * 1000;
  
  return signals.map(signal => {
    const age = now - signal.occurredAt.getTime();
    const decayFactor = Math.exp(-age / ONE_YEAR); // Exponential decay
    return {
      ...signal,
      weight: signal.weight * decayFactor
    };
  });
}
```

---

## 7. MCP/A2A Protocol Integration

### 7.1 MCP Gateway

The ARTL exposes itself as an MCP server for agent-native reputation queries.

#### Server Configuration

```json
{
  "mcpServers": {
    "trustlayer": {
      "command": "npx",
      "args": ["@eli5/artl-mcp"],
      "env": {
        "ARTL_API_KEY": "your_api_key"
      }
    }
  }
}
```

#### Available Tools

**1. get_reputation_score**
```typescript
{
  name: "get_reputation_score",
  description: "Get the reputation score for an agent by DID or identifier",
  parameters: {
    type: "object",
    properties: {
      did: {
        type: "string",
        description: "Agent DID (did:artl:...) or identifier"
      },
      includeBreakdown: {
        type: "boolean",
        default: false,
        description: "Include score breakdown by category"
      }
    },
    required: ["did"]
  }
}
```

Example response:
```json
{
  "did": "did:artl:abc123",
  "name": "Research Agent Pro",
  "reputation": {
    "overall": 847,
    "confidence": 0.87,
    "breakdown": {
      "transactionHistory": 210,
      "protocolCompliance": 245,
      "communityTrust": 198,
      "verificationLevel": 194
    }
  },
  "riskLevel": "low",
  "recommendation": "Safe to transact. High reputation with consistent history."
}
```

**2. verify_agent**
```typescript
{
  name: "verify_agent",
  description: "Verify if an agent meets minimum reputation requirements",
  parameters: {
    type: "object",
    properties: {
      did: {
        type: "string",
        description: "Agent DID to verify"
      },
      minScore: {
        type: "number",
        default: 600,
        description: "Minimum reputation score required (0-1000)"
      },
      minConfidence: {
        type: "number",
        default: 0.5,
        description: "Minimum confidence level required (0-1)"
      },
      requireVerification: {
        type: "boolean",
        default: false,
        description: "Require enterprise/domain verification"
      }
    },
    required: ["did"]
  }
}
```

**3. compare_agents**
```typescript
{
  name: "compare_agents",
  description: "Compare reputation scores of multiple agents",
  parameters: {
    type: "object",
    properties: {
      dids: {
        type: "array",
        items: { type: "string" },
        minItems: 2,
        maxItems: 5,
        description: "Array of agent DIDs to compare"
      }
    },
    required: ["dids"]
  }
}
```

**4. submit_transaction_signal**
```typescript
{
  name: "submit_transaction_signal",
  description: "Submit a trust signal after completing a transaction with another agent",
  parameters: {
    type: "object",
    properties: {
      counterpartyDid: {
        type: "string",
        description: "DID of the agent you transacted with"
      },
      outcome: {
        type: "string",
        enum: ["success", "partial", "failure"],
        description: "Outcome of the transaction"
      },
      amount: {
        type: "number",
        description: "Transaction amount (if applicable)"
      },
      currency: {
        type: "string",
        description: "Currency code (e.g., USD)"
      },
      description: {
        type: "string",
        description: "Brief description of the transaction"
      }
    },
    required: ["counterpartyDid", "outcome"]
  }
}
```

#### Available Resources

**1. Agent Reputation**
```typescript
{
  uri: "artl://reputation/{did}",
  name: "Agent Reputation",
  mimeType: "application/json",
  description: "Current reputation score and history for an agent"
}
```

**2. Trust Guidelines**
```typescript
{
  uri: "artl://guidelines/risk-assessment",
  name: "Risk Assessment Guidelines",
  mimeType: "text/markdown",
  description: "Guidelines for interpreting reputation scores and risk levels"
}
```

#### Available Prompts

**1. reputation_check**
```typescript
{
  name: "reputation_check",
  description: "Check if an agent is trustworthy before transacting",
  arguments: [
    {
      name: "agent_did",
      description: "DID of the agent to check",
      required: true
    },
    {
      name: "transaction_value",
      description: "Value of the planned transaction (for risk assessment)",
      required: false
    }
  ]
}
```

### 7.2 A2A Protocol Integration

ARTL extends the A2A AgentCard with reputation fields and provides task-level reputation requirements.

#### AgentCard Extension

```json
{
  "name": "Research Agent",
  "description": "Autonomous research assistant",
  "url": "https://agent.example.com/a2a",
  "artl": {
    "did": "did:artl:abc123",
    "reputation": {
      "score": 847,
      "confidence": 0.87,
      "verified": true,
      "lastUpdated": "2026-03-02T10:30:00Z"
    },
    "verification": {
      "level": "enterprise",
      "domain": "example.com",
      "domainVerified": true
    }
  }
}
```

#### Task-Level Reputation Requirements

```json
{
  "id": "task-123",
  "type": "research",
  "description": "Conduct market research",
  "artl": {
    "requirements": {
      "minReputationScore": 700,
      "minConfidence": 0.7,
      "requireVerification": true,
      "allowedVerificationLevels": ["enterprise", "kyc"]
    }
  }
}
```

#### A2A Reputation Check Flow

```
┌─────────────┐                    ┌─────────────┐                    ┌─────────────┐
│   Agent A   │ ──1. Task Request──▶│   Agent B   │ ──2. Rep Check──▶│    ARTL     │
│  (Client)   │                    │  (Server)   │                    │  (Oracle)   │
└─────────────┘                    └─────────────┘◀─3. Score/Verdict──┴─────────────┘
       ▲                                  │
       │                                  │
       └───────4. Task Response───────────┘
              (Accept/Reject with reason)
```

---

## 8. Tech Stack Recommendation

### 8.1 Core Infrastructure

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **API Gateway** | Kong or AWS API Gateway | Rate limiting, auth, routing |
| **Primary API** | Node.js + NestJS | Type safety, enterprise patterns, MCP SDK |
| **Reputation Engine** | Python + FastAPI | ML/AI ecosystem for scoring algorithms |
| **Web Frontend** | Next.js 14 (App Router) | SSR, React Server Components |
| **Database** | PostgreSQL 16 | ACID, JSONB for flexibility, time-series support |
| **Cache** | Redis 7 | Hot reputation scores, rate limits, pub/sub |
| **Queue** | BullMQ (Redis) | Background reputation recalculation |
| **Blockchain** | Ethereum/Polygon (optional) | Score anchoring, dispute log immutability |
| **Search** | PostgreSQL + pgvector | Agent discovery by capability |

### 8.2 DevOps & Infrastructure

| Component | Technology |
|-----------|------------|
| **Container Runtime** | Docker + Docker Compose (local), Kubernetes (prod) |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Datadog or Grafana + Prometheus |
| **Logging** | Datadog or ELK Stack |
| **Error Tracking** | Sentry |
| **CDN** | Cloudflare |

### 8.3 External Services

| Service | Purpose |
|---------|---------|
| **Clerk or Auth0** | Authentication (OAuth, SSO) |
| **Stripe** | Payments for verification services |
| **Chainlink (optional)** | Decentralized oracle for on-chain scores |
| **IPFS (optional)** | Decentralized storage for attestations |

### 8.4 Protocol SDKs

| Package | Purpose |
|---------|---------|
| `@modelcontextprotocol/sdk` | MCP protocol implementation |
| `@google/a2a-sdk` | A2A protocol integration |
| `did-jwt` | DID-based authentication |

---

## 9. 8-Week Implementation Roadmap

### Week 1: Foundation

**Goals:** Infrastructure and identity system

**Tasks:**
- [ ] Set up monorepo structure (Turborepo)
- [ ] PostgreSQL + Redis Docker setup
- [ ] Design and create database schema
- [ ] Set up NestJS API project
- [ ] Implement Agent entity and basic CRUD
- [ ] DID generation and management
- [ ] Configure CI/CD pipeline

**Deliverable:** Working API with agent registration and DID issuance

### Week 2: Signal Ingestion

**Goals:** Trust signal collection system

**Tasks:**
- [ ] TrustSignal entity and CRUD
- [ ] Signal ingestion API endpoints
- [ ] Basic signal validation
- [ ] Source verification framework
- [ ] API key authentication
- [ ] Rate limiting

**Deliverable:** Agents can submit trust signals

### Week 3: Reputation Engine

**Goals:** Core scoring algorithm

**Tasks:**
- [ ] Set up Python FastAPI service
- [ ] Implement scoring algorithm
- [ ] Time-decay calculations
- [ ] Confidence scoring
- [ ] Score recalculation jobs (BullMQ)
- [ ] Reputation history tracking

**Deliverable:** Working reputation score calculation

### Week 4: MCP Gateway

**Goals:** MCP protocol integration

**Tasks:**
- [ ] Set up MCP SDK project
- [ ] Implement `get_reputation_score` tool
- [ ] Implement `verify_agent` tool
- [ ] Tool response formatting
- [ ] Error handling
- [ ] Publish `@eli5/artl-mcp` package

**Deliverable:** Agents can query reputation via MCP

### Week 5: Web Frontend

**Goals:** Human-facing dashboard

**Tasks:**
- [ ] Set up Next.js 14 project
- [ ] Design system setup (Tailwind + shadcn/ui)
- [ ] Agent registration flow
- [ ] Reputation dashboard
- [ ] Signal history view
- [ ] Authentication integration

**Deliverable:** Web dashboard for reputation management

### Week 6: A2A Integration & Verification

**Goals:** A2A protocol and verification

**Tasks:**
- [ ] A2A Gateway setup
- [ ] AgentCard reputation extension
- [ ] Task-level reputation requirements
- [ ] Email verification flow
- [ ] Domain verification (DNS TXT)
- [ ] Verification badges

**Deliverable:** A2A integration and basic verification

### Week 7: Attestations & Disputes

**Goals:** Advanced trust features

**Tasks:**
- [ ] Attestation submission flow
- [ ] Attestation verification
- [ ] Dispute filing system
- [ ] Basic dispute resolution workflow
- [ ] Reputation impact calculation
- [ ] Admin dashboard

**Deliverable:** Full attestation and dispute system

### Week 8: Enterprise & Launch

**Goals:** Enterprise features and production readiness

**Tasks:**
- [ ] Organization support
- [ ] Enterprise verification workflow
- [ ] Compliance reporting
- [ ] API documentation
- [ ] Security audit
- [ ] Production deployment

**Deliverable:** Production-ready MVP

---

## 10. Success Metrics

### 10.1 Platform Metrics

| Metric | Target (90 days post-launch) |
|--------|------------------------------|
| Registered agents | 1,000+ |
| Trust signals submitted | 10,000+ |
| API requests/day | 50,000+ |
| Average reputation score | 600+ |
| Agents with verification | 200+ |

### 10.2 Quality Metrics

| Metric | Target |
|--------|--------|
| Score recalculation latency | < 5 minutes |
| API uptime | 99.9% |
| Signal verification rate | > 80% |
| Dispute resolution time | < 7 days |

### 10.3 Business Metrics

| Metric | Target (6 months) |
|--------|-------------------|
| Enterprise customers | 10+ |
| Monthly API calls | 1M+ |
| Verified agents | 500+ |

---

## 11. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Gaming the reputation system | High | High | Multi-source signals, anomaly detection, dispute resolution |
| Privacy concerns | Medium | High | Minimal PII collection, data retention policies |
| Protocol changes (A2A/MCP) | Medium | Medium | Abstract protocol layer, monitor spec changes |
| Low adoption | Medium | High | Free tier for developers, enterprise partnerships |
| Regulatory scrutiny | Medium | Medium | Compliance framework, legal review |

---

## 12. Appendix

### 12.1 Glossary

- **ARTL:** Agent Reputation & Trust Layer
- **DID:** Decentralized Identifier
- **Trust Signal:** A piece of evidence about an agent's behavior
- **Attestation:** A formal verification or endorsement
- **Reputation Score:** 0-1000 score representing agent trustworthiness
- **A2A:** Agent-to-Agent protocol (Google)
- **MCP:** Model Context Protocol (Anthropic)

### 12.2 References

- [A2A Protocol Specification](https://google.github.io/A2A/)
- [MCP Specification](https://modelcontextprotocol.io)
- [DID Core Specification](https://www.w3.org/TR/did-core/)

---

*Document Version: 1.0*  
*Last Updated: 2026-03-02*  
*Author: Eli5 Venture Studio - ARCHITECT Agent*

-- ARTL Database Schema
-- Agent Reputation & Trust Layer

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================
-- CORE TABLES
-- ============================================

-- Users (human accounts)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    stripe_customer_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Organizations
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    domain_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    settings JSONB DEFAULT '{}',
    stripe_subscription_id VARCHAR(255),
    subscription_tier VARCHAR(50) DEFAULT 'free',
    subscription_status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Organization members
CREATE TABLE IF NOT EXISTS organization_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'member',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(organization_id, user_id)
);

-- Agents
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    did VARCHAR(255) UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL,
    identities JSONB NOT NULL DEFAULT '{}',
    reputation JSONB NOT NULL DEFAULT '{}',
    verification_status JSONB NOT NULL DEFAULT '{"level": "none"}',
    owner_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_active_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trust signals
CREATE TABLE IF NOT EXISTS trust_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    source_type VARCHAR(50) NOT NULL,
    source_name VARCHAR(255) NOT NULL,
    source_url TEXT,
    source_verified BOOLEAN DEFAULT FALSE,
    signal_type VARCHAR(50) NOT NULL,
    signal_subtype VARCHAR(100),
    value DECIMAL(4,3) NOT NULL,
    weight DECIMAL(3,2) NOT NULL,
    confidence DECIMAL(3,2) NOT NULL,
    metadata JSONB DEFAULT '{}',
    occurred_at TIMESTAMPTZ NOT NULL,
    recorded_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    verified BOOLEAN DEFAULT FALSE,
    verification_method VARCHAR(100)
);

-- Attestations
CREATE TABLE IF NOT EXISTS attestations (
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
CREATE TABLE IF NOT EXISTS disputes (
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

-- Reputation history
CREATE TABLE IF NOT EXISTS reputation_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    overall_score INTEGER NOT NULL,
    confidence DECIMAL(3,2) NOT NULL,
    signals_count INTEGER NOT NULL,
    breakdown JSONB NOT NULL
);

-- API Keys
CREATE TABLE IF NOT EXISTS api_keys (
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

-- Sessions
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Verification tokens
CREATE TABLE IF NOT EXISTS verification_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    token VARCHAR(255) NOT NULL UNIQUE,
    token_type VARCHAR(50) NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Webhook events
CREATE TABLE IF NOT EXISTS webhook_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMPTZ,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_agents_did ON agents(did);
CREATE INDEX idx_signals_agent ON trust_signals(agent_id);
CREATE INDEX idx_signals_type ON trust_signals(signal_type);
CREATE INDEX idx_history_agent ON reputation_history(agent_id);
CREATE INDEX idx_api_keys_agent ON api_keys(agent_id);
// Shared types for ARTL (Agent Reputation & Trust Layer)

// ============================================
// AGENT TYPES
// ============================================

export type AgentType = 'individual' | 'enterprise' | 'service' | 'autonomous';

export interface A2AIdentity {
  agentId: string;
  endpoint: string;
  agentCardUrl: string;
  verified: boolean;
}

export interface MCPIdentity {
  serverName: string;
  registryUrl?: string;
  verified: boolean;
}

export interface BlockchainIdentity {
  chain: string;
  address: string;
  verified: boolean;
}

export interface WebIdentity {
  domain: string;
  verified: boolean;
}

export interface AgentIdentities {
  a2a?: A2AIdentity;
  mcp?: MCPIdentity;
  blockchain?: BlockchainIdentity[];
  web?: WebIdentity[];
}

export interface ReputationBreakdown {
  transactionHistory: number;
  protocolCompliance: number;
  communityTrust: number;
  verificationLevel: number;
}

export interface ReputationScore {
  overall: number;
  confidence: number;
  breakdown: ReputationBreakdown;
  lastCalculatedAt: Date | null;
  nextRecalculationAt: Date | null;
}

export type VerificationLevel = 'none' | 'email' | 'domain' | 'enterprise' | 'kyc';

export interface VerificationStatus {
  level: VerificationLevel;
  verifiedAt?: Date;
  expiresAt?: Date;
  method?: string;
}

export interface ReputationSnapshot {
  timestamp: Date;
  score: number;
  confidence: number;
  signalsCount: number;
}

export interface Agent {
  id: string;
  did: string;
  name: string;
  description?: string;
  type: AgentType;
  identities: AgentIdentities;
  reputation: ReputationScore;
  verificationStatus: VerificationStatus;
  ownerId?: string;
  organizationId?: string;
  createdAt: Date;
  updatedAt: Date;
  lastActiveAt: Date;
}

// ============================================
// TRUST SIGNAL TYPES
// ============================================

export type SignalSourceType = 'a2a' | 'mcp' | 'blockchain' | 'manual' | 'api' | 'enterprise';

export interface SignalSource {
  type: SignalSourceType;
  name: string;
  url?: string;
  verified: boolean;
}

export type SignalType = 
  | 'transaction'
  | 'task_completion'
  | 'protocol_compliance'
  | 'dispute'
  | 'attestation'
  | 'security_incident'
  | 'review'
  | 'uptime'
  | 'response_time';

export interface TrustSignalMetadata {
  transactionId?: string;
  counterpartyId?: string;
  amount?: number;
  currency?: string;
  description?: string;
  evidenceUrl?: string;
  [key: string]: unknown;
}

export interface TrustSignal {
  id: string;
  agentId: string;
  source: SignalSource;
  type: SignalType;
  subtype?: string;
  value: number;
  weight: number;
  confidence: number;
  metadata: TrustSignalMetadata;
  occurredAt: Date;
  recordedAt: Date;
  expiresAt?: Date;
  verified: boolean;
  verificationMethod?: string;
}

// ============================================
// ATTESTATION TYPES
// ============================================

export type AttestationType =
  | 'identity_verification'
  | 'security_audit'
  | 'performance_test'
  | 'compliance_certification'
  | 'business_verification'
  | 'skill_endorsement';

export type AttestationStatus = 'pending' | 'verified' | 'rejected' | 'revoked';

export interface Attestation {
  id: string;
  agentId: string;
  attesterType: 'individual' | 'enterprise' | 'protocol';
  attesterId: string;
  attesterReputation?: number;
  type: AttestationType;
  claim: string;
  evidenceUrls: string[];
  weight?: number;
  status: AttestationStatus;
  createdAt: Date;
  verifiedAt?: Date;
  expiresAt?: Date;
}

// ============================================
// DISPUTE TYPES
// ============================================

export type DisputeType = 
  | 'non_delivery'
  | 'quality_issue'
  | 'payment_dispute'
  | 'contract_breach'
  | 'fraud'
  | 'other';

export type DisputeStatus = 'open' | 'under_review' | 'resolved' | 'escalated';
export type EscrowStatus = 'none' | 'held' | 'released_to_initiator' | 'released_to_respondent' | 'split';

export interface DisputeEvidence {
  type: 'transaction_log' | 'communication' | 'contract' | 'expert_opinion' | 'other';
  url: string;
  submittedBy: string;
  submittedAt: Date;
}

export interface DisputeResolution {
  outcome: 'initiator_wins' | 'respondent_wins' | 'split' | 'dismissed';
  reason: string;
  resolvedBy: 'automated' | 'mediator' | 'arbitrator';
  mediatorId?: string;
}

export interface Dispute {
  id: string;
  initiatorId: string;
  respondentId: string;
  type: DisputeType;
  description: string;
  evidence: DisputeEvidence[];
  amount?: number;
  currency?: string;
  escrowId?: string;
  escrowStatus: EscrowStatus;
  status: DisputeStatus;
  resolution?: DisputeResolution;
  initiatorImpact: number;
  respondentImpact: number;
  createdAt: Date;
  resolvedAt?: Date;
}

// ============================================
// USER & ORGANIZATION TYPES
// ============================================

export interface User {
  id: string;
  email: string;
  name?: string;
  emailVerified: boolean;
  stripeCustomerId?: string;
  createdAt: Date;
  updatedAt: Date;
}

export type SubscriptionTier = 'free' | 'pro' | 'enterprise';
export type SubscriptionStatus = 'active' | 'canceled' | 'past_due' | 'unpaid';

export interface Organization {
  id: string;
  slug: string;
  name: string;
  domain?: string;
  domainVerified: boolean;
  settings: Record<string, unknown>;
  stripeSubscriptionId?: string;
  subscriptionTier: SubscriptionTier;
  subscriptionStatus: SubscriptionStatus;
  createdAt: Date;
  updatedAt: Date;
}

export type OrganizationRole = 'owner' | 'admin' | 'member';

export interface OrganizationMember {
  id: string;
  organizationId: string;
  userId: string;
  role: OrganizationRole;
  createdAt: Date;
}

// ============================================
// API KEY TYPES
// ============================================

export interface ApiKey {
  id: string;
  agentId: string;
  keyHash: string;
  keyPrefix: string;
  name?: string;
  scopes: string[];
  lastUsedAt?: Date;
  expiresAt?: Date;
  createdAt: Date;
  revokedAt?: Date;
}

// ============================================
// REPUTATION CALCULATION TYPES
// ============================================

export interface ReputationCalculationInput {
  signals: TrustSignal[];
  attestations: Attestation[];
  verificationStatus: VerificationStatus;
  disputes: Dispute[];
}

export interface ReputationCalculationResult {
  overall: number;
  confidence: number;
  breakdown: ReputationBreakdown;
}

// ============================================
// API REQUEST/RESPONSE TYPES
// ============================================

export interface CreateAgentRequest {
  name: string;
  description?: string;
  type: AgentType;
  identities?: Partial<AgentIdentities>;
}

export interface CreateAgentResponse {
  agent: Agent;
  apiKey: string;
}

export interface SubmitSignalRequest {
  agentId: string;
  type: SignalType;
  subtype?: string;
  value: number;
  confidence: number;
  metadata?: TrustSignalMetadata;
  occurredAt: Date;
}

export interface QueryReputationRequest {
  agents: string[];
  includeHistory?: boolean;
  includeSignals?: boolean;
}

export interface QueryReputationResult {
  did: string;
  found: boolean;
  agent?: Agent;
  message?: string;
}

export interface QueryReputationResponse {
  results: QueryReputationResult[];
}

export interface FileDisputeRequest {
  respondentId: string;
  type: DisputeType;
  description: string;
  amount?: number;
  currency?: string;
  evidence?: Omit<DisputeEvidence, 'submittedAt'>[];
  requestEscrow?: boolean;
}

// ============================================
// MCP/A2A PROTOCOL TYPES
// ============================================

export interface MCPReputationToolResult {
  did: string;
  name: string;
  reputation: ReputationScore;
  riskLevel: 'low' | 'medium' | 'high' | 'unknown';
  recommendation: string;
}

export interface MCPVerifyAgentParams {
  did: string;
  minScore?: number;
  minConfidence?: number;
  requireVerification?: boolean;
}

export interface MCPVerifyAgentResult {
  did: string;
  verified: boolean;
  reputation: ReputationScore;
  meetsRequirements: boolean;
  reason?: string;
}

export interface A2AAgentCardExtension {
  did: string;
  reputation: {
    score: number;
    confidence: number;
    verified: boolean;
    lastUpdated: Date;
  };
  verification: {
    level: VerificationLevel;
    domain?: string;
    domainVerified: boolean;
  };
}

export interface A2ATaskReputationRequirements {
  minReputationScore?: number;
  minConfidence?: number;
  requireVerification?: boolean;
  allowedVerificationLevels?: VerificationLevel[];
}

// ============================================
// STRIPE/PAYMENT TYPES
// ============================================

export interface PricingTier {
  id: string;
  name: string;
  description: string;
  price: number;
  interval: 'month' | 'year';
  features: string[];
  limits: {
    agents: number;
    apiCalls: number;
    signals: number;
  };
}

export interface CheckoutSessionRequest {
  tier: SubscriptionTier;
  successUrl: string;
  cancelUrl: string;
}

export interface CheckoutSessionResponse {
  sessionId: string;
  url: string;
}

// ============================================
// ERROR TYPES
// ============================================

export class ARTLError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'ARTLError';
  }
}

export class ValidationError extends ARTLError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 'VALIDATION_ERROR', 400, details);
    this.name = 'ValidationError';
  }
}

export class NotFoundError extends ARTLError {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, 'NOT_FOUND', 404);
    this.name = 'NotFoundError';
  }
}

export class UnauthorizedError extends ARTLError {
  constructor(message: string = 'Unauthorized') {
    super(message, 'UNAUTHORIZED', 401);
    this.name = 'UnauthorizedError';
  }
}

export class ForbiddenError extends ARTLError {
  constructor(message: string = 'Forbidden') {
    super(message, 'FORBIDDEN', 403);
    this.name = 'ForbiddenError';
  }
}

export class RateLimitError extends ARTLError {
  constructor(retryAfter: number) {
    super('Rate limit exceeded', 'RATE_LIMIT', 429, { retryAfter });
    this.name = 'RateLimitError';
  }
}
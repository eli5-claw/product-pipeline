// Validation schemas using Zod for ARTL
import { z } from 'zod';

// Base schemas
export const uuidSchema = z.string().uuid();
export const didSchema = z.string().regex(/^did:artl:[a-f0-9-]+$/, 'Invalid DID format');
export const emailSchema = z.string().email('Invalid email address');

// Agent schemas
export const agentTypeSchema = z.enum(['individual', 'enterprise', 'service', 'autonomous']);

export const a2aIdentitySchema = z.object({
  agentId: z.string().min(1),
  endpoint: z.string().url(),
  agentCardUrl: z.string().url(),
  verified: z.boolean().default(false),
});

export const mcpIdentitySchema = z.object({
  serverName: z.string().min(1),
  registryUrl: z.string().url().optional(),
  verified: z.boolean().default(false),
});

export const blockchainIdentitySchema = z.object({
  chain: z.string().min(1),
  address: z.string().min(1),
  verified: z.boolean().default(false),
});

export const webIdentitySchema = z.object({
  domain: z.string().min(1),
  verified: z.boolean().default(false),
});

export const agentIdentitiesSchema = z.object({
  a2a: a2aIdentitySchema.optional(),
  mcp: mcpIdentitySchema.optional(),
  blockchain: z.array(blockchainIdentitySchema).optional(),
  web: z.array(webIdentitySchema).optional(),
}).default({});

export const createAgentSchema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().max(2000).optional(),
  type: agentTypeSchema,
  identities: agentIdentitiesSchema.optional(),
});

export const updateAgentSchema = z.object({
  name: z.string().min(1).max(255).optional(),
  description: z.string().max(2000).optional(),
  identities: agentIdentitiesSchema.optional(),
});

// Trust signal schemas
export const signalSourceTypeSchema = z.enum(['a2a', 'mcp', 'blockchain', 'manual', 'api', 'enterprise']);

export const signalSourceSchema = z.object({
  type: signalSourceTypeSchema,
  name: z.string().min(1).max(255),
  url: z.string().url().optional(),
  verified: z.boolean().default(false),
});

export const signalTypeSchema = z.enum([
  'transaction', 'task_completion', 'protocol_compliance', 'dispute',
  'attestation', 'security_incident', 'review', 'uptime', 'response_time',
]);

export const trustSignalMetadataSchema = z.object({
  transactionId: z.string().optional(),
  counterpartyId: z.string().optional(),
  amount: z.number().positive().optional(),
  currency: z.string().length(3).optional(),
  description: z.string().max(1000).optional(),
  evidenceUrl: z.string().url().optional(),
}).catchall(z.unknown());

export const submitSignalSchema = z.object({
  agentId: z.string().min(1),
  type: signalTypeSchema,
  subtype: z.string().max(100).optional(),
  value: z.number().min(-1).max(1),
  weight: z.number().min(0).max(1).default(1),
  confidence: z.number().min(0).max(1),
  metadata: trustSignalMetadataSchema.default({}),
  occurredAt: z.coerce.date(),
  source: signalSourceSchema.optional(),
});

// Attestation schemas
export const attestationTypeSchema = z.enum([
  'identity_verification', 'security_audit', 'performance_test',
  'compliance_certification', 'business_verification', 'skill_endorsement',
]);

export const submitAttestationSchema = z.object({
  agentId: z.string().min(1),
  type: attestationTypeSchema,
  claim: z.string().min(1).max(2000),
  evidenceUrls: z.array(z.string().url()).max(10).default([]),
  expiresAt: z.coerce.date().optional(),
});

// Dispute schemas
export const disputeTypeSchema = z.enum([
  'non_delivery', 'quality_issue', 'payment_dispute', 'contract_breach', 'fraud', 'other',
]);

export const disputeEvidenceSchema = z.object({
  type: z.enum(['transaction_log', 'communication', 'contract', 'expert_opinion', 'other']),
  url: z.string().url(),
  submittedBy: z.string().min(1),
});

export const fileDisputeSchema = z.object({
  respondentId: z.string().min(1),
  type: disputeTypeSchema,
  description: z.string().min(10).max(5000),
  amount: z.number().positive().optional(),
  currency: z.string().length(3).optional(),
  evidence: z.array(disputeEvidenceSchema).max(10).default([]),
  requestEscrow: z.boolean().default(false),
});

// Reputation query schemas
export const queryReputationSchema = z.object({
  agents: z.array(z.string().min(1)).min(1).max(100),
  includeHistory: z.boolean().default(false),
  includeSignals: z.boolean().default(false),
});

export const verifyAgentSchema = z.object({
  did: z.string().min(1),
  minScore: z.number().min(0).max(1000).default(600),
  minConfidence: z.number().min(0).max(1).default(0.5),
  requireVerification: z.boolean().default(false),
});

// User schemas
export const createUserSchema = z.object({
  email: emailSchema,
  name: z.string().min(1).max(255).optional(),
});

export const updateUserSchema = z.object({
  name: z.string().min(1).max(255).optional(),
});

// Organization schemas
export const subscriptionTierSchema = z.enum(['free', 'pro', 'enterprise']);

export const createOrganizationSchema = z.object({
  name: z.string().min(1).max(255),
  slug: z.string().regex(/^[a-z0-9-]+$/, 'Slug must be lowercase alphanumeric with hyphens only').min(1).max(255),
  domain: z.string().min(1).max(255).optional(),
});

export const updateOrganizationSchema = z.object({
  name: z.string().min(1).max(255).optional(),
  domain: z.string().min(1).max(255).optional(),
});

// Checkout/payment schemas
export const checkoutSessionSchema = z.object({
  tier: subscriptionTierSchema,
  successUrl: z.string().url(),
  cancelUrl: z.string().url(),
});

// Pagination schemas
export const paginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  perPage: z.coerce.number().int().positive().max(100).default(20),
});

export const listSignalsSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  perPage: z.coerce.number().int().positive().max(100).default(20),
  type: signalTypeSchema.optional(),
  verified: z.coerce.boolean().optional(),
});

// Type inferences
export type CreateAgentInput = z.infer<typeof createAgentSchema>;
export type UpdateAgentInput = z.infer<typeof updateAgentSchema>;
export type SubmitSignalInput = z.infer<typeof submitSignalSchema>;
export type SubmitAttestationInput = z.infer<typeof submitAttestationSchema>;
export type FileDisputeInput = z.infer<typeof fileDisputeSchema>;
export type QueryReputationInput = z.infer<typeof queryReputationSchema>;
export type VerifyAgentInput = z.infer<typeof verifyAgentSchema>;
export type CreateUserInput = z.infer<typeof createUserSchema>;
export type UpdateUserInput = z.infer<typeof updateUserSchema>;
export type CreateOrganizationInput = z.infer<typeof createOrganizationSchema>;
export type UpdateOrganizationInput = z.infer<typeof updateOrganizationSchema>;
export type CheckoutSessionInput = z.infer<typeof checkoutSessionSchema>;
export type PaginationInput = z.infer<typeof paginationSchema>;
export type ListSignalsInput = z.infer<typeof listSignalsSchema>;

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import axios from 'axios';

const API_URL = process.env.ARTL_API_URL || 'http://localhost:3001/api/v1';
const API_KEY = process.env.ARTL_API_KEY || '';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json',
  },
});

const server = new Server(
  { name: 'artl-mcp', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'get_reputation_score',
        description: 'Get the reputation score for an agent by DID',
        inputSchema: {
          type: 'object',
          properties: {
            did: {
              type: 'string',
              description: 'Agent DID (did:artl:...)',
            },
            includeBreakdown: {
              type: 'boolean',
              default: false,
              description: 'Include score breakdown by category',
            },
          },
          required: ['did'],
        },
      },
      {
        name: 'verify_agent',
        description: 'Verify if an agent meets minimum reputation requirements',
        inputSchema: {
          type: 'object',
          properties: {
            did: {
              type: 'string',
              description: 'Agent DID to verify',
            },
            minScore: {
              type: 'number',
              default: 600,
              description: 'Minimum reputation score required (0-1000)',
            },
            minConfidence: {
              type: 'number',
              default: 0.5,
              description: 'Minimum confidence level required (0-1)',
            },
            requireVerification: {
              type: 'boolean',
              default: false,
              description: 'Require enterprise/domain verification',
            },
          },
          required: ['did'],
        },
      },
      {
        name: 'compare_agents',
        description: 'Compare reputation scores of multiple agents',
        inputSchema: {
          type: 'object',
          properties: {
            dids: {
              type: 'array',
              items: { type: 'string' },
              minItems: 2,
              maxItems: 5,
              description: 'Array of agent DIDs to compare',
            },
          },
          required: ['dids'],
        },
      },
      {
        name: 'submit_transaction_signal',
        description: 'Submit a trust signal after completing a transaction',
        inputSchema: {
          type: 'object',
          properties: {
            counterpartyDid: {
              type: 'string',
              description: 'DID of the agent you transacted with',
            },
            outcome: {
              type: 'string',
              enum: ['success', 'partial', 'failure'],
              description: 'Outcome of the transaction',
            },
            amount: {
              type: 'number',
              description: 'Transaction amount (if applicable)',
            },
            currency: {
              type: 'string',
              description: 'Currency code (e.g., USD)',
            },
            description: {
              type: 'string',
              description: 'Brief description of the transaction',
            },
          },
          required: ['counterpartyDid', 'outcome'],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'get_reputation_score': {
        const { did, includeBreakdown = false } = args as { did: string; includeBreakdown?: boolean };
        const response = await api.get(`/agents/${did}/reputation`);
        const data = response.data;

        const riskLevel = data.reputation.overall >= 800 ? 'low' : 
                         data.reputation.overall >= 500 ? 'medium' : 'high';

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                did: data.did,
                name: data.name,
                reputation: data.reputation,
                riskLevel,
                recommendation: riskLevel === 'low' 
                  ? 'Safe to transact. High reputation with consistent history.'
                  : riskLevel === 'medium'
                  ? 'Proceed with caution. Moderate reputation score.'
                  : 'High risk. Limited history or negative signals detected.',
              }, null, 2),
            },
          ],
        };
      }

      case 'verify_agent': {
        const { did, minScore = 600, minConfidence = 0.5, requireVerification = false } = args as any;
        const response = await api.get(`/agents/${did}/reputation`);
        const data = response.data;

        const meetsScore = data.reputation.overall >= minScore;
        const meetsConfidence = data.reputation.confidence >= minConfidence;
        const meetsVerification = !requireVerification || 
          ['enterprise', 'kyc'].includes(data.verificationStatus.level);

        const meetsRequirements = meetsScore && meetsConfidence && meetsVerification;

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                did: data.did,
                verified: true,
                reputation: data.reputation,
                meetsRequirements,
                checks: {
                  score: { required: minScore, actual: data.reputation.overall, passed: meetsScore },
                  confidence: { required: minConfidence, actual: data.reputation.confidence, passed: meetsConfidence },
                  verification: { required: requireVerification, actual: data.verificationStatus.level, passed: meetsVerification },
                },
                reason: meetsRequirements ? undefined : 
                  !meetsScore ? `Score below minimum (${data.reputation.overall} < ${minScore})` :
                  !meetsConfidence ? `Confidence below minimum (${data.reputation.confidence} < ${minConfidence})` :
                  'Verification level insufficient',
              }, null, 2),
            },
          ],
        };
      }

      case 'compare_agents': {
        const { dids } = args as { dids: string[] };
        const response = await api.post('/reputation/query', { agents: dids });
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(response.data, null, 2),
            },
          ],
        };
      }

      case 'submit_transaction_signal': {
        const { counterpartyDid, outcome, amount, currency, description } = args as any;
        
        const value = outcome === 'success' ? 0.8 : outcome === 'partial' ? 0.3 : -0.8;
        
        const response = await api.post('/signals', {
          agentId: counterpartyDid,
          type: 'transaction',
          subtype: `${outcome}_payment`,
          value,
          confidence: 0.95,
          metadata: { amount, currency, description },
          occurredAt: new Date().toISOString(),
        });

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                status: 'Signal recorded',
                signalId: response.data.id,
                estimatedImpact: response.data.estimatedImpact,
              }, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('ARTL MCP server running on stdio');
}

main().catch(console.error);
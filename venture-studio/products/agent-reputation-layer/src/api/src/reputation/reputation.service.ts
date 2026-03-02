import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { ReputationEngine } from './reputation.engine';

@Injectable()
export class ReputationService {
  constructor(
    private prisma: PrismaService,
    private engine: ReputationEngine,
  ) {}

  async query(dids: string[]) {
    const results = await Promise.all(
      dids.map(async (did) => {
        const agent = await this.prisma.agent.findUnique({
          where: { did },
        });

        if (!agent) {
          return {
            did,
            found: false,
            message: 'Agent not found',
          };
        }

        const signalCount = await this.prisma.trustSignal.count({
          where: { agentId: agent.id },
        });

        return {
          did,
          found: true,
          agent: {
            id: agent.id,
            did: agent.did,
            name: agent.name,
            reputation: agent.reputation,
            verificationStatus: agent.verificationStatus,
            signalCount,
          },
        };
      }),
    );

    return { results };
  }

  async recalculate(agentId: string) {
    const agent = await this.prisma.agent.findUnique({
      where: { id: agentId },
    });

    if (!agent) {
      throw new NotFoundException(`Agent not found: ${agentId}`);
    }

    // Calculate new score
    const result = await this.engine.calculateScore(agentId);

    // Update agent reputation
    const updatedAgent = await this.prisma.agent.update({
      where: { id: agentId },
      data: {
        reputation: {
          overall: result.overall,
          confidence: result.confidence,
          breakdown: result.breakdown,
          lastCalculatedAt: new Date().toISOString(),
          nextRecalculationAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
        },
      },
    });

    // Record in history
    await this.prisma.reputationHistory.create({
      data: {
        agentId,
        overallScore: result.overall,
        confidence: result.confidence,
        signalsCount: await this.prisma.trustSignal.count({ where: { agentId } }),
        breakdown: result.breakdown,
      },
    });

    return {
      agentId,
      did: agent.did,
      reputation: updatedAgent.reputation,
      riskLevel: this.engine.getRiskLevel(result.overall),
      recommendation: this.engine.getRecommendation(result.overall, result.confidence),
    };
  }

  async getHistory(did: string, limit = 30) {
    const agent = await this.prisma.agent.findUnique({
      where: { did },
    });

    if (!agent) {
      throw new NotFoundException(`Agent not found: ${did}`);
    }

    const history = await this.prisma.reputationHistory.findMany({
      where: { agentId: agent.id },
      orderBy: { timestamp: 'desc' },
      take: limit,
    });

    return {
      did,
      history: history.map(h => ({
        timestamp: h.timestamp,
        score: h.overallScore,
        confidence: h.confidence,
        signalsCount: h.signalsCount,
        breakdown: h.breakdown,
      })),
    };
  }

  async getLeaderboard(limit = 100) {
    const agents = await this.prisma.agent.findMany({
      where: {
        reputation: {
          path: ['overall'],
          gt: 0,
        },
      },
      orderBy: {
        reputation: {
          path: ['overall'],
          order: 'desc',
        },
      },
      take: limit,
    });

    return {
      agents: agents.map((agent, index) => ({
        rank: index + 1,
        did: agent.did,
        name: agent.name,
        type: agent.type,
        reputation: agent.reputation,
        verificationStatus: agent.verificationStatus,
      })),
    };
  }
}

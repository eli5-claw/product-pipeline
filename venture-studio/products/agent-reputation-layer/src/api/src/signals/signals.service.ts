import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { ReputationEngine } from '../reputation/reputation.engine';

@Injectable()
export class SignalsService {
  constructor(
    private prisma: PrismaService,
    private reputationEngine: ReputationEngine,
  ) {}

  async create(data: any) {
    // Find agent by DID or ID
    let agent = await this.prisma.agent.findUnique({
      where: { did: data.agentId },
    });

    if (!agent) {
      agent = await this.prisma.agent.findUnique({
        where: { id: data.agentId },
      });
    }

    if (!agent) {
      throw new NotFoundException('Agent not found');
    }

    const signal = await this.prisma.trustSignal.create({
      data: {
        agentId: agent.id,
        sourceType: data.source?.type || 'api',
        sourceName: data.source?.name || 'API',
        sourceUrl: data.source?.url,
        sourceVerified: data.source?.verified || false,
        signalType: data.type,
        signalSubtype: data.subtype,
        value: data.value,
        weight: data.weight || 1,
        confidence: data.confidence,
        metadata: data.metadata || {},
        occurredAt: new Date(data.occurredAt || Date.now()),
        expiresAt: data.expiresAt ? new Date(data.expiresAt) : null,
      },
    });

    // Trigger async reputation recalculation
    const recalculationResult = await this.triggerRecalculation(agent.id);

    return {
      id: signal.id,
      status: 'recorded',
      estimatedImpact: this.estimateImpact(data.value, data.weight, data.confidence),
      recalculationScheduled: true,
      newReputation: recalculationResult,
    };
  }

  async findByAgent(did: string, page: number, perPage: number) {
    const agent = await this.prisma.agent.findUnique({
      where: { did },
    });

    if (!agent) {
      throw new NotFoundException('Agent not found');
    }

    const skip = (page - 1) * perPage;
    const [signals, total] = await Promise.all([
      this.prisma.trustSignal.findMany({
        where: { agentId: agent.id },
        skip,
        take: perPage,
        orderBy: { occurredAt: 'desc' },
      }),
      this.prisma.trustSignal.count({
        where: { agentId: agent.id },
      }),
    ]);

    return {
      data: signals,
      pagination: {
        page,
        perPage,
        total,
        totalPages: Math.ceil(total / perPage),
      },
    };
  }

  private estimateImpact(value: number, weight: number, confidence: number): number {
    return Math.abs(value * weight * confidence * 10);
  }

  private async triggerRecalculation(agentId: string): Promise<any> {
    // Update last active
    await this.prisma.agent.update({
      where: { id: agentId },
      data: { lastActiveAt: new Date() },
    });

    // Calculate new score
    const result = await this.reputationEngine.calculateScore(agentId);

    // Update agent reputation
    await this.prisma.agent.update({
      where: { id: agentId },
      data: {
        reputation: {
          overall: result.overall,
          confidence: result.confidence,
          breakdown: result.breakdown,
          lastCalculatedAt: new Date().toISOString(),
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
      overall: result.overall,
      confidence: result.confidence,
      riskLevel: this.reputationEngine.getRiskLevel(result.overall),
    };
  }
}

import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class AgentsService {
  constructor(private prisma: PrismaService) {}

  async create(data: any) {
    const did = `did:artl:${uuidv4()}`;
    const apiKey = `artl_live_${uuidv4().replace(/-/g, '')}`;
    
    const agent = await this.prisma.agent.create({
      data: {
        did,
        name: data.name,
        description: data.description,
        type: data.type,
        identities: data.identities || {},
        reputation: {
          overall: 500,
          confidence: 0,
          breakdown: {
            transactionHistory: 0,
            protocolCompliance: 0,
            communityTrust: 0,
            verificationLevel: 0,
          },
        },
        verificationStatus: { level: 'none' },
      },
    });

    await this.prisma.apiKey.create({
      data: {
        agentId: agent.id,
        keyHash: await this.hashKey(apiKey),
        keyPrefix: apiKey.slice(0, 8),
        scopes: ['read:reputation', 'write:signals'],
      },
    });

    return { agent, apiKey };
  }

  async findAll(page: number, perPage: number) {
    const skip = (page - 1) * perPage;
    const [agents, total] = await Promise.all([
      this.prisma.agent.findMany({
        skip,
        take: perPage,
        orderBy: { createdAt: 'desc' },
      }),
      this.prisma.agent.count(),
    ]);

    return {
      data: agents,
      pagination: {
        page,
        perPage,
        total,
        totalPages: Math.ceil(total / perPage),
      },
    };
  }

  async findByDid(did: string) {
    const agent = await this.prisma.agent.findUnique({
      where: { did },
    });

    if (!agent) {
      throw new NotFoundException(`Agent with DID ${did} not found`);
    }

    return agent;
  }

  async getReputation(did: string) {
    const agent = await this.findByDid(did);
    
    const signalCounts = await this.prisma.trustSignal.groupBy({
      by: ['value'],
      where: { agentId: agent.id },
      _count: true,
    });

    return {
      agentId: agent.id,
      did: agent.did,
      name: agent.name,
      reputation: agent.reputation,
      verificationStatus: agent.verificationStatus,
      signalCounts: {
        total: signalCounts.reduce((acc, s) => acc + s._count, 0),
        positive: signalCounts.find(s => s.value > 0)?._count || 0,
        negative: signalCounts.find(s => s.value < 0)?._count || 0,
        neutral: signalCounts.find(s => s.value === 0)?._count || 0,
      },
    };
  }

  async update(id: string, data: any) {
    return this.prisma.agent.update({
      where: { id },
      data: {
        ...data,
        updatedAt: new Date(),
      },
    });
  }

  async remove(id: string) {
    return this.prisma.agent.delete({
      where: { id },
    });
  }

  private async hashKey(key: string): Promise<string> {
    const crypto = await import('crypto');
    return crypto.createHash('sha256').update(key).digest('hex');
  }
}
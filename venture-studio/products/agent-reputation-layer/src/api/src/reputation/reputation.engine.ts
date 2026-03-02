import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { ReputationCalculationResult, ReputationBreakdown } from '../../../shared/types';

@Injectable()
export class ReputationEngine {
  constructor(private prisma: PrismaService) {}

  /**
   * Calculate comprehensive reputation score for an agent
   */
  async calculateScore(agentId: string): Promise<ReputationCalculationResult> {
    const [signals, attestations, agent] = await Promise.all([
      this.prisma.trustSignal.findMany({
        where: { agentId },
        orderBy: { occurredAt: 'desc' },
      }),
      this.prisma.attestation.findMany({
        where: { agentId, status: 'verified' },
      }),
      this.prisma.agent.findUnique({
        where: { id: agentId },
      }),
    ]);

    if (!agent) {
      throw new Error(`Agent not found: ${agentId}`);
    }

    // Apply time decay to signals
    const decayedSignals = this.applyTimeDecay(signals);

    // Calculate category scores
    const transactionScore = this.calculateTransactionScore(decayedSignals);
    const complianceScore = this.calculateComplianceScore(decayedSignals);
    const communityScore = this.calculateCommunityScore(decayedSignals, attestations);
    const verificationScore = this.calculateVerificationScore(agent.verificationStatus as any);

    // Calculate overall score
    const overall = Math.round(
      transactionScore + complianceScore + communityScore + verificationScore
    );

    // Calculate confidence based on signal volume and diversity
    const confidence = this.calculateConfidence(signals, attestations);

    const breakdown: ReputationBreakdown = {
      transactionHistory: Math.round(transactionScore),
      protocolCompliance: Math.round(complianceScore),
      communityTrust: Math.round(communityScore),
      verificationLevel: Math.round(verificationScore),
    };

    return {
      overall: Math.min(1000, Math.max(0, overall)),
      confidence: Math.min(1, Math.max(0, confidence)),
      breakdown,
    };
  }

  /**
   * Apply exponential time decay to signals
   * Signals lose relevance over time
   */
  private applyTimeDecay(signals: any[]): any[] {
    const now = Date.now();
    const ONE_YEAR = 365 * 24 * 60 * 60 * 1000;

    return signals.map(signal => {
      const age = now - new Date(signal.occurredAt).getTime();
      const decayFactor = Math.exp(-age / ONE_YEAR);
      return {
        ...signal,
        effectiveWeight: Number(signal.weight) * decayFactor,
        age,
      };
    });
  }

  /**
   * Calculate transaction history score (0-250)
   */
  private calculateTransactionScore(signals: any[]): number {
    const transactionSignals = signals.filter(
      s => s.signalType === 'transaction'
    );

    if (transactionSignals.length === 0) {
      return 0;
    }

    // Calculate weighted score
    const weightedSum = transactionSignals.reduce((sum, s) => {
      const value = Number(s.value); // -1 to +1
      const weight = s.effectiveWeight || Number(s.weight);
      const confidence = Number(s.confidence);
      return sum + (value * weight * confidence);
    }, 0);

    const totalWeight = transactionSignals.reduce(
      (sum, s) => sum + (s.effectiveWeight || Number(s.weight)),
      0
    );

    if (totalWeight === 0) return 0;

    // Normalize to 0-1 range, then scale to 0-250
    const normalizedScore = (weightedSum / totalWeight + 1) / 2;
    
    // Volume bonus: more transactions = higher confidence in score
    const volumeBonus = Math.min(1, transactionSignals.length / 50);
    
    return normalizedScore * 250 * (0.5 + 0.5 * volumeBonus);
  }

  /**
   * Calculate protocol compliance score (0-250)
   */
  private calculateComplianceScore(signals: any[]): number {
    const complianceSignals = signals.filter(s =>
      ['protocol_compliance', 'uptime', 'response_time'].includes(s.signalType)
    );

    if (complianceSignals.length === 0) {
      return 0;
    }

    // Group by subtype for more granular scoring
    const bySubtype: Record<string, any[]> = {};
    complianceSignals.forEach(s => {
      const subtype = s.signalSubtype || s.signalType;
      if (!bySubtype[subtype]) bySubtype[subtype] = [];
      bySubtype[subtype].push(s);
    });

    // Calculate score per subtype
    let totalScore = 0;
    let subtypeCount = 0;

    for (const subtype of Object.keys(bySubtype)) {
      const subtypeSignals = bySubtype[subtype];
      const weightedSum = subtypeSignals.reduce((sum, s) => {
        const value = Number(s.value);
        const weight = s.effectiveWeight || Number(s.weight);
        const confidence = Number(s.confidence);
        return sum + (value * weight * confidence);
      }, 0);

      const totalWeight = subtypeSignals.reduce(
        (sum, s) => sum + (s.effectiveWeight || Number(s.weight)),
        0
      );

      if (totalWeight > 0) {
        const normalizedScore = (weightedSum / totalWeight + 1) / 2;
        totalScore += normalizedScore;
        subtypeCount++;
      }
    }

    // Average across subtypes, scale to 250
    const avgScore = subtypeCount > 0 ? totalScore / subtypeCount : 0;
    return avgScore * 250;
  }

  /**
   * Calculate community trust score (0-250)
   */
  private calculateCommunityScore(signals: any[], attestations: any[]): number {
    const communitySignals = signals.filter(s =>
      ['review', 'attestation'].includes(s.signalType)
    );

    // Calculate signal-based score
    let signalScore = 0;
    if (communitySignals.length > 0) {
      const weightedSum = communitySignals.reduce((sum, s) => {
        const value = Number(s.value);
        const weight = s.effectiveWeight || Number(s.weight);
        const confidence = Number(s.confidence);
        return sum + (value * weight * confidence);
      }, 0);

      const totalWeight = communitySignals.reduce(
        (sum, s) => sum + (s.effectiveWeight || Number(s.weight)),
        0
      );

      if (totalWeight > 0) {
        const normalizedScore = (weightedSum / totalWeight + 1) / 2;
        signalScore = normalizedScore * 150; // Max 150 from signals
      }
    }

    // Calculate attestation-based score (up to 100)
    let attestationScore = 0;
    if (attestations.length > 0) {
      const totalAttestationWeight = attestations.reduce((sum, a) => {
        return sum + (Number(a.weight) || 0.1);
      }, 0);

      // Cap at 1.0 total weight for attestations
      attestationScore = Math.min(1, totalAttestationWeight) * 100;
    }

    return signalScore + attestationScore;
  }

  /**
   * Calculate verification level score (0-250)
   */
  private calculateVerificationScore(verificationStatus: any): number {
    const levelScores: Record<string, number> = {
      'none': 0,
      'email': 50,
      'domain': 125,
      'enterprise': 200,
      'kyc': 250,
    };

    const baseScore = levelScores[verificationStatus?.level] || 0;
    
    // Check if verification is expired
    if (verificationStatus?.expiresAt) {
      const expiresAt = new Date(verificationStatus.expiresAt);
      if (expiresAt < new Date()) {
        return Math.max(0, baseScore - 100); // Penalty for expired verification
      }
    }

    return baseScore;
  }

  /**
   * Calculate confidence score (0-1)
   */
  private calculateConfidence(signals: any[], attestations: any[]): number {
    // Base confidence from signal volume
    const volumeConfidence = Math.min(1, signals.length / 100);

    // Diversity bonus: signals from multiple sources
    const sourceTypes = new Set(signals.map(s => s.sourceType)).size;
    const diversityBonus = Math.min(0.3, sourceTypes / 10);

    // Recency bonus: signals within last 30 days
    const now = Date.now();
    const thirtyDaysAgo = now - 30 * 24 * 60 * 60 * 1000;
    const recentSignals = signals.filter(
      s => new Date(s.occurredAt).getTime() > thirtyDaysAgo
    );
    const recencyBonus = Math.min(0.2, recentSignals.length / 20);

    // Attestation bonus
    const attestationBonus = Math.min(0.2, attestations.length / 5);

    return Math.min(1, volumeConfidence + diversityBonus + recencyBonus + attestationBonus);
  }

  /**
   * Get risk level based on reputation score
   */
  getRiskLevel(score: number): 'low' | 'medium' | 'high' | 'unknown' {
    if (score >= 800) return 'low';
    if (score >= 500) return 'medium';
    if (score > 0) return 'high';
    return 'unknown';
  }

  /**
   * Get recommendation text based on reputation
   */
  getRecommendation(score: number, confidence: number): string {
    if (confidence < 0.3) {
      return 'Insufficient data to make a recommendation. Proceed with caution.';
    }

    if (score >= 800) {
      return 'Safe to transact. High reputation with consistent history.';
    }
    if (score >= 600) {
      return 'Generally trustworthy. Standard verification recommended for large transactions.';
    }
    if (score >= 400) {
      return 'Proceed with caution. Limited history or mixed signals detected.';
    }
    return 'High risk. Limited history or negative signals detected. Consider escrow.';
  }
}

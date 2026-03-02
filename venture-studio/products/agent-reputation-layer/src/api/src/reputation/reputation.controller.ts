import { Controller, Post, Body, Get, Param, Query, UseGuards } from '@nestjs/common';
import { ReputationService } from './reputation.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('reputation')
export class ReputationController {
  constructor(private readonly reputationService: ReputationService) {}

  @Post('query')
  async query(@Body() body: { agents: string[] }) {
    return this.reputationService.query(body.agents);
  }

  @Post(':did/recalculate')
  @UseGuards(JwtAuthGuard)
  async recalculate(@Param('did') did: string) {
    const agent = await this.reputationService.query({ agents: [did] });
    if (!agent.results[0]?.found) {
      return { error: 'Agent not found' };
    }
    const agentId = agent.results[0].agent.id;
    return this.reputationService.recalculate(agentId);
  }

  @Get(':did/history')
  async getHistory(
    @Param('did') did: string,
    @Query('limit') limit = 30,
  ) {
    return this.reputationService.getHistory(did, +limit);
  }

  @Get('leaderboard/top')
  async getLeaderboard(@Query('limit') limit = 100) {
    return this.reputationService.getLeaderboard(+limit);
  }
}

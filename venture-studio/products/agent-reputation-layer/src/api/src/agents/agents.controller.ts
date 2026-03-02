import { Controller, Get, Post, Patch, Delete, Body, Param, Query, UseGuards } from '@nestjs/common';
import { AgentsService } from './agents.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('agents')
export class AgentsController {
  constructor(private readonly agentsService: AgentsService) {}

  @Post()
  @UseGuards(JwtAuthGuard)
  async create(@Body() createAgentDto: any) {
    return this.agentsService.create(createAgentDto);
  }

  @Get()
  @UseGuards(JwtAuthGuard)
  async findAll(@Query('page') page = 1, @Query('perPage') perPage = 20) {
    return this.agentsService.findAll(+page, +perPage);
  }

  @Get(':did')
  async findOne(@Param('did') did: string) {
    return this.agentsService.findByDid(did);
  }

  @Get(':did/reputation')
  async getReputation(@Param('did') did: string) {
    return this.agentsService.getReputation(did);
  }

  @Patch(':id')
  @UseGuards(JwtAuthGuard)
  async update(@Param('id') id: string, @Body() updateAgentDto: any) {
    return this.agentsService.update(id, updateAgentDto);
  }

  @Delete(':id')
  @UseGuards(JwtAuthGuard)
  async remove(@Param('id') id: string) {
    return this.agentsService.remove(id);
  }
}
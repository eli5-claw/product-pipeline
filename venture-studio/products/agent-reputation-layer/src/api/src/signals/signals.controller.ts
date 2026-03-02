import { Controller, Post, Body, Get, Param, Query, UseGuards } from '@nestjs/common';
import { SignalsService } from './signals.service';
import { ApiKeyGuard } from '../auth/api-key.guard';

@Controller('signals')
export class SignalsController {
  constructor(private readonly signalsService: SignalsService) {}

  @Post()
  @UseGuards(ApiKeyGuard)
  async create(@Body() createSignalDto: any) {
    return this.signalsService.create(createSignalDto);
  }

  @Get('agent/:did')
  async findByAgent(
    @Param('did') did: string,
    @Query('page') page = 1,
    @Query('perPage') perPage = 50,
  ) {
    return this.signalsService.findByAgent(did, +page, +perPage);
  }
}
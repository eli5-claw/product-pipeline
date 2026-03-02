import { Module } from '@nestjs/common';
import { ReputationService } from './reputation.service';
import { ReputationController } from './reputation.controller';
import { ReputationEngine } from './reputation.engine';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [ReputationController],
  providers: [ReputationService, ReputationEngine],
  exports: [ReputationService, ReputationEngine],
})
export class ReputationModule {}

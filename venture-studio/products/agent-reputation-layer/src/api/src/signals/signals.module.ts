import { Module } from '@nestjs/common';
import { SignalsService } from './signals.service';
import { SignalsController } from './signals.controller';
import { PrismaModule } from '../prisma/prisma.module';
import { ReputationModule } from '../reputation/reputation.module';

@Module({
  imports: [PrismaModule, ReputationModule],
  controllers: [SignalsController],
  providers: [SignalsService],
  exports: [SignalsService],
})
export class SignalsModule {}

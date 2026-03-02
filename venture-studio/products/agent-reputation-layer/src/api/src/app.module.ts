import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { ThrottlerModule } from '@nestjs/throttler';
import { PrismaModule } from './prisma/prisma.module';
import { AgentsModule } from './agents/agents.module';
import { ReputationModule } from './reputation/reputation.module';
import { SignalsModule } from './signals/signals.module';
import { AuthModule } from './auth/auth.module';
import { UsersModule } from './users/users.module';
import { PaymentsModule } from './payments/payments.module';
import { WebhooksModule } from './webhooks/webhooks.module';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    ThrottlerModule.forRoot([{
      ttl: 60000,
      limit: 100,
    }]),
    PrismaModule,
    AgentsModule,
    ReputationModule,
    SignalsModule,
    AuthModule,
    UsersModule,
    PaymentsModule,
    WebhooksModule,
  ],
})
export class AppModule {}
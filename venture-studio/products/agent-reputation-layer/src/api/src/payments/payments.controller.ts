import { Controller, Post, Body, Headers } from '@nestjs/common';
import { PaymentsService } from './payments.service';

@Controller('payments')
export class PaymentsController {
  constructor(private readonly paymentsService: PaymentsService) {}

  @Post('checkout')
  async createCheckout(@Body() body: { tier: string; successUrl: string; cancelUrl: string }) {
    return this.paymentsService.createCheckoutSession(body.tier, body.successUrl, body.cancelUrl);
  }

  @Post('webhook')
  async webhook(@Body() body: any, @Headers('stripe-signature') signature: string) {
    return this.paymentsService.handleWebhook(body, signature);
  }
}
import { Injectable } from '@nestjs/common';

@Injectable()
export class WebhooksService {
  async process(payload: any) {
    // Webhook processing placeholder
    return { processed: true };
  }
}
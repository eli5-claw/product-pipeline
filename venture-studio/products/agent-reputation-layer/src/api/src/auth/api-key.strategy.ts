import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { HeaderAPIKeyStrategy } from 'passport-headerapikey';
import { AuthService } from './auth.service';

@Injectable()
export class ApiKeyStrategy extends PassportStrategy(HeaderAPIKeyStrategy, 'api-key') {
  constructor(private authService: AuthService) {
    super({ header: 'X-API-Key', prefix: '' }, true, async (apiKey, done) => {
      const user = await this.authService.validateApiKey(apiKey);
      if (user) {
        done(null, user);
      } else {
        done(null, false);
      }
    });
  }
}
import { Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthService {
  constructor(private jwtService: JwtService) {}

  async validateApiKey(key: string): Promise<any> {
    // In production, validate against database
    if (key.startsWith('artl_live_')) {
      return { agentId: 'test', scopes: ['read:reputation', 'write:signals'] };
    }
    return null;
  }

  async login(user: any) {
    const payload = { sub: user.id, email: user.email };
    return {
      access_token: this.jwtService.sign(payload),
    };
  }
}
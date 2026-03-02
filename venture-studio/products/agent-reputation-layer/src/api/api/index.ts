import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from '../src/app.module';

// Vercel serverless handler
export default async function handler(req: any, res: any) {
  const app = await NestFactory.create(AppModule);
  
  app.enableCors({
    origin: process.env.FRONTEND_URL || '*',
    credentials: true,
  });
  
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    transform: true,
  }));
  
  app.setGlobalPrefix('api/v1');
  
  await app.init();
  const server = app.getHttpAdapter().getInstance();
  return server(req, res);
}

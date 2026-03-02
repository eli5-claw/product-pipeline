import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.enableCors({
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true,
  });
  
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    transform: true,
  }));
  
  app.setGlobalPrefix('api/v1');

  // Health check endpoint
  const httpAdapter = app.getHttpAdapter();
  httpAdapter.get('/health', (req, res) => {
    res.json({ 
      status: 'ok', 
      timestamp: new Date().toISOString(),
      version: '1.0.0',
    });
  });
  
  const port = process.env.PORT || 3001;
  await app.listen(port);
  console.log(`ARTL API running on port ${port}`);
}

// For Vercel serverless deployment
if (process.env.VERCEL) {
  // Vercel serverless handler
  const serverless = require('@vercel/node');
  module.exports = async (req: any, res: any) => {
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

    // Health check
    const httpAdapter = app.getHttpAdapter();
    httpAdapter.get('/health', (req, res) => {
      res.json({ 
        status: 'ok', 
        timestamp: new Date().toISOString(),
        version: '1.0.0',
      });
    });
    
    await app.init();
    const server = app.getHttpAdapter().getInstance();
    return server(req, res);
  };
} else {
  // Local/Docker development
  bootstrap();
}

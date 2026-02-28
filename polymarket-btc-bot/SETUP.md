# Polymarket BTC Trading Bot - Setup Guide

## Prerequisites

1. **Rust** (1.75 or later)
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   source $HOME/.cargo/env
   ```

2. **Docker** (optional, for containerized deployment)
   ```bash
   # Follow instructions at https://docs.docker.com/get-docker/
   ```

3. **Polymarket Account**
   - Create an account at https://polymarket.com
   - Generate API keys from your account settings
   - Fund your wallet with USDC on Polygon

## Configuration

### 1. Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
BOT_POLYMARKET__API_KEY=your_api_key
BOT_POLYMARKET__API_SECRET=your_api_secret
BOT_POLYMARKET__PRIVATE_KEY=your_wallet_private_key
```

### 2. Configuration Files

The bot uses YAML configuration files in the `config/` directory:

- `development.yaml` - Development settings
- `production.yaml` - Production settings (AWS deployment)

Key settings to review:

```yaml
trading:
  min_edge_threshold: 0.02    # Minimum 2% edge to trade
  max_open_positions: 5        # Max concurrent positions

risk:
  kelly_fraction: 0.25         # Conservative quarter-Kelly
  max_position_size_usd: 1000  # Max $1k per position
  max_daily_loss_usd: 5000     # Stop at $5k daily loss
```

## Building

### Local Build

```bash
# Development build
cargo build

# Optimized release build
cargo build --release
```

### Docker Build

```bash
make docker-build
```

## Running

### Local Development

```bash
# Load environment variables
source .env

# Run with development config
RUN_MODE=development cargo run

# Run with production config
RUN_MODE=production cargo run --release
```

### Docker

```bash
# Start all services (bot + monitoring)
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

## Testing

```bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_kelly_criterion
```

## Deployment

### AWS eu-west-2 (London)

1. **Configure Terraform**
   ```bash
   cd terraform
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your settings
   ```

2. **Deploy**
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

3. **Configure Secrets**
   SSH into the instance and add your API credentials to `/opt/polymarket-bot/.env`

## Monitoring

### Local

- Health check: http://localhost:8080/health
- Metrics: http://localhost:9090/metrics

### With Docker Compose

- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9091

## Troubleshooting

### Build Errors

1. **Missing OpenSSL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install libssl-dev pkg-config
   
   # macOS
   brew install openssl
   ```

2. **Linking Errors**
   ```bash
   rustup update
   cargo clean
   cargo build
   ```

### Runtime Errors

1. **Connection Refused**
   - Check firewall settings
   - Verify API credentials
   - Check Polymarket/Binance API status

2. **Rate Limiting**
   - Reduce `scan_interval_ms` in config
   - Check your API tier limits

## Security Best Practices

1. **Never commit credentials**
   - Use `.env` file (already in `.gitignore`)
   - Use environment variables in production

2. **Use dedicated API keys**
   - Create separate keys for dev/prod
   - Restrict IP addresses if possible

3. **Monitor access logs**
   - Review CloudWatch logs regularly
   - Set up alerts for unusual activity

## Next Steps

1. Review the [README.md](README.md) for detailed documentation
2. Check [monitoring/grafana/dashboards/](monitoring/grafana/dashboards/) for metrics
3. Read the code in `src/` to understand the implementation

## Support

- GitHub Issues: https://github.com/yourusername/polymarket-btc-bot/issues
- Discord: [Your Discord Server]

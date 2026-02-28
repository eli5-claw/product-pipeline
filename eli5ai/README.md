# Eli5AI — Autonomous Media Agent

Fully autonomous content agent for tech/AI/crypto. Generates threads in @Eli5DeFi style with auto-generated infographics.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp config/example.env config/.env
# Edit config/.env with your API keys

# Run once (test mode)
python src/main.py --test

# Run autonomously
python src/main.py --daemon
```

## Architecture

- `src/ingest/` — Data ingestion from APIs/RSS
- `src/ranker/` — Story ranking and selection
- `src/generate/` — Content generation (threads)
- `src/visual/` — Infographic rendering
- `src/publish/` — X/Twitter API publisher
- `src/memory/` — Performance tracking and style evolution

## Style Guide

See `config/style.md` for the complete Eli5AI voice and formatting rules.

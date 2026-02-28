# Testing Guide

## Quick Start

```bash
cd polymarket_bot

# Install test dependencies
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python tests/test_bot.py

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

## Test Categories

### Unit Tests (No API needed)
- `TestBotConfig` - Configuration validation
- `TestRiskManager` - Position sizing, limits
- `TestPerformanceTracker` - Stats calculation
- `TestMath` - Profit/loss calculations

### Mocked Tests (No real API calls)
- `TestPolymarketClient` - API client with mocked responses
- Simulation mode verification
- Error handling

### Integration Tests (Requires credentials)
- `TestIntegration` - Real API calls
- Skipped automatically if no credentials

## Running Without Credentials

Most tests work without Polymarket credentials:

```bash
# These work without credentials
python -m pytest tests/test_bot.py::TestBotConfig -v
python -m pytest tests/test_bot.py::TestRiskManager -v
python -m pytest tests/test_bot.py::TestMath -v
```

## Adding New Tests

```python
def test_new_feature(self):
    """Description of what this tests."""
    # Setup
    config = BotConfig(some_setting=True)
    
    # Execute
    result = some_function(config)
    
    # Assert
    self.assertEqual(result, expected_value)
```

## Continuous Integration

Add to `.github/workflows/test.yml`:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pip install pytest
      - run: python -m pytest tests/ -v
```

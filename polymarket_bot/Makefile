# Test Suite Makefile

.PHONY: test test-unit test-mocked test-integration test-coverage lint format clean

# Run all tests
test:
	python -m pytest tests/ -v

# Run only unit tests (no API calls)
test-unit:
	python -m pytest tests/test_bot.py::TestBotConfig tests/test_bot.py::TestRiskManager tests/test_bot.py::TestPerformanceTracker tests/test_bot.py::TestMath -v

# Run mocked tests
test-mocked:
	python -m pytest tests/test_bot.py::TestPolymarketClient -v

# Run integration tests (requires credentials)
test-integration:
	python -m pytest tests/test_bot.py::TestIntegration -v

# Run with coverage report
test-coverage:
	python -m pytest tests/ --cov=enhanced_bot --cov-report=term-missing --cov-report=html

# Lint code
lint:
	flake8 enhanced_bot.py tests/ --max-line-length=100

# Format code
format:
	black enhanced_bot.py tests/ --line-length=100

# Clean generated files
clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf __pycache__/
	rm -rf tests/__pycache__/
	rm -f .coverage
	rm -f bot.log

# Run simulation mode test
test-simulation:
	SIMULATION_MODE=true python -c "from enhanced_bot import BotConfig; c = BotConfig(simulation_mode=True); print('Simulation mode:', c.simulation_mode)"

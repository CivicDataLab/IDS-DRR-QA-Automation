# Contributing to IDS-DRR QA Automation

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Run tests
6. Submit a pull request

## Development Setup

```bash
# Clone repository
git clone https://github.com/your-username/IDS-DRR-QA-Automation.git
cd IDS-DRR-QA-Automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your settings
```

## Running Tests

```bash
# Smoke tests
pytest -m smoke -v

# Parallel execution
pytest -n 4 tests/ -v

# All tests
pytest tests/ -v
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions/classes
- Keep functions focused and small

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG if applicable
5. Request review from maintainers

## Test Guidelines

- Mark tests appropriately (`@pytest.mark.smoke`, etc.)
- Ensure tests are independent
- Use Page Object Model pattern
- Add self-healing support for new locators

## Questions?

Open an issue for discussion before starting major changes.

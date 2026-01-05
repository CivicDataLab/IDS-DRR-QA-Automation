# IDS-DRR QA Automation

Pytest-based test automation framework with self-healing and parallel execution.

## Features

- Self-healing tests - Auto-adapt to UI changes
- Parallel execution - Run tests simultaneously
- Enhanced reporting - Detailed test and healing reports

## Quick Start

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your application URL

# Run tests
pytest -m smoke -v                # Quick smoke tests
pytest -n 4 -m smoke -v           # Parallel (4 workers)
./run_parallel_tests.sh -n 4      # Using helper script
```

## Project Structure

```
tests/          # Test files
pages/          # Page Object Model
locators/       # Element locators
config/         # Configuration
utils/          # Utilities
conftest.py     # Pytest fixtures
pytest.ini      # Configuration
```

## Running Tests

### Standard Execution

```bash
# By marker
pytest -m smoke -v
pytest -m analytics -v
pytest -m dataset -v

# Specific test
pytest tests/test_analytics.py::TestAnalyticsNavigation -v
```

### Parallel Execution

```bash
# Auto-detect workers
pytest -n auto -v

# Specific workers
pytest -n 4 tests/ -v      # 4 workers (recommended)
pytest -n 8 tests/ -v      # 8 workers

# Using helper script
./run_parallel_tests.sh                # Default: 4 workers
./run_parallel_tests.sh --auto         # Auto-detect
./run_parallel_tests.sh -n 8 -m smoke  # 8 workers, smoke tests
```

### GitHub Actions

```bash
# Push to trigger CI/CD
git push origin main

# Or manually via GitHub Actions UI
```

## Test Markers

- `smoke` - Critical tests
- `analytics` - Analytics page
- `dataset` - Dataset page
- `component` - UI components
- `flow` - End-to-end flows
- `negative` - Error cases
- `edge_case` - Edge scenarios

## Configuration

**.env**
```ini
URL=https://your-app-url.com
LOCAL=true
HEADLESS=false
```

## Reports

```bash
# View latest report
./view_reports.sh

# List all reports
./view_reports.sh --all

# Self-healing summary
./view_reports.sh --self-healing

# Clean old reports
./view_reports.sh --clean 30
```

## Performance

| Workers | Time vs Serial | Speedup |
|---------|----------------|---------|
| 1 (serial) | 100% | 1x |
| 2 workers | ~60% | 1.7x |
| 4 workers | ~35% | 2.9x |
| 8 workers | ~20% | 5x |

## Documentation

- [docs/QUICKSTART.md](docs/QUICKSTART.md) - Quick setup guide
- [docs/SELF_HEALING_GUIDE.md](docs/SELF_HEALING_GUIDE.md) - Complete reference
- [docs/EXAMPLES.md](docs/EXAMPLES.md) - Usage examples
- [docs/REPORTS_GUIDE.md](docs/REPORTS_GUIDE.md) - Report management
- [docs/MULTISTATE_QUICKSTART.md](docs/MULTISTATE_QUICKSTART.md) - Multi-state quick start
- [docs/MULTISTATE_TESTING_GUIDE.md](docs/MULTISTATE_TESTING_GUIDE.md) - Multi-state testing guide
- [.github/workflows/README.md](.github/workflows/README.md) - CI/CD setup

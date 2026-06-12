# Usage Examples

## Basic Parallel Execution

```bash
# 4 workers
pytest -n 4 tests/ -v

# Expected: 4 browser instances, ~65% faster
```

## Smoke Tests

```bash
# Fast validation
pytest -n auto -m smoke -v

# All-states comprehensive smoke test (tests all 5 states with dropdowns + indicators)
pytest -m smoke -k "TestAllStatesIndicatorSmoke" -v

# Use case: CI/CD pre-deployment checks, post-deployment validation
```

## With Auto-Retry

```bash
# Retry failures
pytest -n 4 --reruns 2 --reruns-delay 1 -m analytics

# Handles flaky tests automatically
```

## Test Categories

```bash
# Analytics
pytest -n 4 -m analytics -v

# Dataset
pytest -n 4 -m dataset -v

# Negative tests
pytest -n 2 -m negative -v
```

## Helper Script

```bash
# Default (4 workers)
./run_parallel_tests.sh

# Auto-detect
./run_parallel_tests.sh --auto

# 8 workers, smoke tests
./run_parallel_tests.sh -n 8 -m smoke

# Retry failures
./run_parallel_tests.sh -n 4 -r 2

# Specific file
./run_parallel_tests.sh -t tests/test_analytics.py -n 4

# Disable healing
./run_parallel_tests.sh -n 4 --no-healing

# Serial
./run_parallel_tests.sh --serial -m smoke
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest -n 4 --reruns 2 -v
      - uses: actions/upload-artifact@v4
        with:
          name: reports
          path: reports/
```

## Debugging

```bash
# Single test
pytest tests/test_analytics.py::TestMultiStateNavigation::test_navigate_to_analytics_from_homepage -v -s

# Detailed logs
pytest tests/ --log-cli-level=DEBUG

# Disable healing
pytest tests/ --disable-healing

# Last failed
pytest --lf -v

# With debugger
pytest tests/test_analytics.py::test_name -v -s --pdb
```

## Performance Testing

```bash
# Compare worker counts
time pytest tests/test_analytics.py -v        # Serial
time pytest -n 2 tests/test_analytics.py -v   # 2 workers
time pytest -n 4 tests/test_analytics.py -v   # 4 workers
time pytest -n 8 tests/test_analytics.py -v   # 8 workers
```

## Viewing Reports

```bash
# Latest report
./view_reports.sh

# List all
./view_reports.sh --all

# Healing summary
./view_reports.sh --self-healing

# Manual
open reports/test_report_*.html
cat reports/self_healing/summary_*.txt
tail -100 reports/test_execution.log
```

## Advanced Filtering

```bash
# Smoke AND analytics
pytest -n 4 -m "smoke and analytics" -v

# Not slow
pytest -n 4 -m "not slow" -v

# Analytics but not edge cases
pytest -n 4 -m "analytics and not edge_case" -v

# Smoke OR negative
pytest -n 4 -m "smoke or negative" -v
```

## Custom Configuration

```bash
# Custom timeout
pytest -n 4 --timeout=120 tests/ -v

# Custom report
pytest -n 4 --html=custom_reports/my_report.html tests/ -v

# Verbose healing
pytest -n 4 --log-cli-level=INFO tests/ -v

# Stop on first failure
pytest -n 4 -x tests/ -v
```

## Workflows

### Daily Development

```bash
# Morning: Smoke
pytest -n auto -m smoke

# Development: Affected tests
pytest tests/test_analytics.py -v

# Before commit: Full + retries
pytest -n 4 --reruns 2 tests/ -v
```

### CI/CD Pipeline

```bash
# Fast validation
pytest -n auto -m smoke --reruns 2

# All-states comprehensive smoke (recommended for post-deployment)
pytest -m smoke -k "TestAllStatesIndicatorSmoke" -v

# Full regression
pytest -n 8 --reruns 1 --html=reports/report.html
```

## Analyzing Healing

```bash
# Count events
cat reports/self_healing/healing_report_*.json | jq '.total_healing_events'

# List healed elements
cat reports/self_healing/healing_report_*.json | jq '.events[].element_name'

# Most used strategy
cat reports/self_healing/healing_report_*.json | jq '.events[].strategy' | sort | uniq -c

# Learned locators
cat config/learned_locators.json | jq
```

## Common Patterns

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
pytest -n 4 -m smoke --disable-warnings -q
```

### Nightly Build

```bash
#!/bin/bash
pytest -n 8 --reruns 2 --html=reports/nightly_$(date +%Y%m%d).html tests/ -v
```

### PR Validation

```bash
#!/bin/bash
pytest -n auto -m "smoke or analytics" --reruns 1 -v
```

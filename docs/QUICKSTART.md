# Quick Start Guide

## Setup (5 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your application URL

# Run first test
pytest -n 4 -m smoke -v
```

## Common Commands

```bash
# Basic
pytest tests/                          # All tests (serial)
pytest -m smoke                        # Smoke tests only

# All-States Smoke Test (comprehensive - tests all 5 states)
pytest -m smoke -k "TestAllStatesIndicatorSmoke" -v

# Parallel (Recommended)
pytest -n 4 tests/                     # 4 workers
pytest -n auto tests/                  # Auto-detect CPUs
pytest -n 4 -m smoke                   # Parallel smoke tests

# With retry
pytest -n 4 --reruns 2                 # Retry failures 2x

# Helper script
./run_parallel_tests.sh                # 4 workers (default)
./run_parallel_tests.sh --auto         # Auto workers
./run_parallel_tests.sh -n 8 -r 2      # 8 workers, retry 2x

# Debugging
pytest tests/test_analytics.py -v      # Single file
pytest --disable-healing               # Disable self-healing
```

## Worker Count Guide

| Machine Type | Workers | Command |
|-------------|---------|---------|
| Laptop | 2 | `pytest -n 2` |
| Standard | 4 | `pytest -n 4` |
| High-end | 8 | `pytest -n 8` |
| Auto | Auto | `pytest -n auto` |

## How Self-Healing Works

**Before:**
```python
# Fails if XPath changes
element = driver.find_element(By.XPATH, "/html/body/div[1]/button")
```

**After:**
```python
# Same code, framework auto-tries alternatives:
# 1. Original XPath (fails)
# 2. Learned locator (if exists)
# 3. Relaxed XPath (success!)
# Test passes, no code changes needed
```

## Reports

```bash
# View latest
./view_reports.sh

# List all
./view_reports.sh --all

# Healing summary
./view_reports.sh --self-healing

# Clean old reports
./view_reports.sh --clean 30
```

## Performance

| Tests | Serial | Parallel (4 workers) | Speedup |
|-------|--------|---------------------|---------|
| 30 | 15 min | ~4 min | 3.8x |
| 60 | 30 min | ~8 min | 3.8x |

## Configuration (Optional)

**Self-healing:** `config/self_healing_config.py`
```python
class SelfHealingConfig:
    ENABLED = True
    MAX_HEALING_ATTEMPTS = 3  # Optimized for performance
    LEARNING_MODE = True
    HEALING_TIMEOUT = 3       # 3 seconds per attempt
```

**Pytest:** `pytest.ini`
```ini
[pytest]
# Set default workers (optional)
# dist = loadscope
```

## Troubleshooting

**Tests fail in parallel but pass serially?**
```python
# Mark as serial
@pytest.mark.serial
def test_must_run_alone(driver):
    pass
```

**Too many browsers?**
```bash
# Reduce workers
pytest -n 2
```

## Next Steps

1. Read [SELF_HEALING_GUIDE.md](SELF_HEALING_GUIDE.md) for details
2. Try different worker counts
3. Check healing reports
4. Set up [GitHub Actions](../.github/workflows/README.md)

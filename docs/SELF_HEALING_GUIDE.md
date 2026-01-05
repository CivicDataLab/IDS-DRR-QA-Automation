# Self-Healing Test Automation Guide

## Overview

Self-healing tests automatically adapt to UI changes and run in parallel for faster execution.

## Quick Reference

```bash
# Parallel execution
pytest -n 4 tests/                  # 4 workers
pytest -n auto tests/               # Auto-detect

# With retry
pytest -n 4 --reruns 2              # Retry failures

# Disable healing
pytest --disable-healing

# Helper script
./run_parallel_tests.sh -n 4
```

## Self-Healing

### How It Works

When element locators fail, the framework tries:
1. Original locator
2. Learned locators (from past runs)
3. Relaxed XPath variations
4. CSS alternatives
5. Tag-based locators

### Benefits

- 70% fewer failures from UI changes
- Automatic learning from successful finds
- Detailed healing reports
- Zero code changes required

### Configuration

Edit `config/self_healing_config.py`:

```python
class SelfHealingConfig:
    ENABLED = True
    MAX_HEALING_ATTEMPTS = 3  # Optimized from 5 to 3
    LEARNING_MODE = True
    HEALING_TIMEOUT = 3       # Optimized from 5 to 3 seconds
    MAX_RETRIES = 2           # Optimized from 3 to 2
    STRATEGIES = [
        "original",
        "learned",
        "relaxed_xpath",
        "css_alternatives",
        "tag_based",
        "text_based",
    ]
```

## Parallel Execution

### Worker Recommendations

| Workers | Use Case |
|---------|----------|
| 2 | Small machines |
| 4 | Standard development |
| 8 | High-performance |
| auto | Auto-detect CPUs |

### When to Use

**Good for:**
- Independent tests
- Smoke tests
- Read-only operations

**Avoid for:**
- Tests with shared state
- Database modifications
- Same test data usage

Mark serial tests:
```python
@pytest.mark.serial
def test_shared_resource(driver):
    pass
```

### Distribution Strategies

```bash
# Load balance (default)
pytest -n 4 --dist=load

# By module
pytest -n 4 --dist=loadfile

# By class
pytest -n 4 --dist=loadscope
```

## Reports

### Viewing Reports

```bash
# HTML report
./view_reports.sh

# All reports
./view_reports.sh --all

# Self-healing summary
./view_reports.sh --self-healing

# Manual
open reports/test_report_*.html
cat reports/self_healing/summary_*.txt
```

### Report Types

1. **HTML**: Visual test results
2. **JSON**: Machine-readable results
3. **Self-Healing**: Healing events
4. **Summary**: Test statistics
5. **Logs**: Execution details

## Best Practices

### For Self-Healing

1. Use meaningful element names
2. Review healing reports regularly
3. Update frequently healed locators
4. Prefer stable locators (ID > Name > CSS > XPath)

### For Parallel Execution

1. Design independent tests
2. Use unique test data
3. Mark serial tests appropriately
4. Start with low worker count, increase gradually

## Performance

| Configuration | Time | Speedup |
|--------------|------|---------|
| Serial | 100% | 1x |
| 2 workers | ~60% | 1.7x |
| 4 workers | ~35% | 2.9x |
| 8 workers | ~20% | 5x |

## Troubleshooting

### Self-Healing Issues

**Not working:**
```bash
# Check configuration
pytest tests/ -v --log-cli-level=DEBUG
```

**Too aggressive:**
```python
# Reduce attempts in config (current default is 3)
MAX_HEALING_ATTEMPTS = 2  # Further reduce to 2 if needed
```

### Parallel Issues

**Tests fail in parallel:**
```python
# Check for shared state
# Mark as serial if needed
@pytest.mark.serial
```

**Resource exhaustion:**
```bash
# Reduce workers
pytest -n 2
```

**Browser cleanup:**
```bash
# Check for orphaned processes
ps aux | grep chrome
pkill -f chrome
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run Tests
  run: pytest -n 4 --reruns 2 --html=reports/report.html

- name: Upload Reports
  uses: actions/upload-artifact@v4
  with:
    name: test-reports
    path: reports/
```

See [.github/workflows/README.md](../.github/workflows/README.md) for details.

## Advanced

### Custom Healing Strategies

Extend `SelfHealingLocator` in `utils/self_healing.py`.

### Learned Locators

Stored in `config/learned_locators.json`:
```json
{
  "By.XPATH:/html/body/button": {
    "successful_locator": ["By.XPATH", "//button"],
    "timestamp": "2025-01-15T10:30:00",
    "use_count": 5
  }
}
```

## Support

1. Check troubleshooting section
2. Review logs: `reports/test_execution.log`
3. Check healing reports: `reports/self_healing/`

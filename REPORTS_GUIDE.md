# Test Reports Guide

## Report Naming

Reports are timestamped: `test_report_YYYYMMDD_HHMMSS.html`

Example: `test_report_20251229_143025.html` = Dec 29, 2025 at 14:30:25

## Quick Commands

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

## Report Types

1. **HTML** (`test_report_*.html`) - Visual test results
2. **JSON** (`test_report_*.json`) - Machine-readable
3. **Self-Healing Summary** (`summary_*.txt`) - Healing events
4. **Healing Details** (`healing_report_*.json`) - Detailed logs
5. **Execution Log** (`test_execution.log`) - Complete trace

## HTML Report Contents

- Environment (Python, browser, URL)
- Summary (total, passed, failed, duration)
- Test results (name, status, duration, errors)
- Screenshots (if failed)
- Self-healing status

## Self-Healing Reports

Located in `reports/self_healing/`:

**Summary** (`summary_*.txt`):
```
Total Tests: 50
Passed: 48
Failed: 2
Pass Rate: 96.00%
Self-Healing Events: 3
Healing Rate: 0.06 events/test
```

**Detailed** (`healing_report_*.json`):
```json
{
  "total_healing_events": 3,
  "events": [{
    "element_name": "Map View Button",
    "strategy": "relaxed_xpath",
    "original_locator": "By.XPATH:/html/body/main/div/button[1]",
    "successful_locator": "By.XPATH://button[1]",
    "timestamp": "2025-12-29T14:25:15"
  }]
}
```

## Workflow

### After Test Run

```bash
# Run tests
pytest -n 4 tests/ -v

# View report
./view_reports.sh
```

### Managing Reports

```bash
# Check disk usage
du -sh reports/

# Clean old (keep 30 days)
./view_reports.sh --clean 30

# Delete specific
rm reports/test_report_20251215_*.html
```

## Retention Strategy

**Recommended:**
- Daily runs: 7 days
- Weekly regression: 30 days
- Releases: 90+ days

```bash
# Weekly cleanup
./view_reports.sh --clean 7

# Monthly
./view_reports.sh --clean 30

# Quarterly
./view_reports.sh --clean 90
```

## Comparing Reports

```bash
# List with dates
./view_reports.sh --all

# Open two reports
open reports/test_report_20251229_143025.html
open reports/test_report_20251228_164533.html

# Compare healing
diff reports/self_healing/summary_20251229_143025.txt \
     reports/self_healing/summary_20251228_164533.txt
```

## Track Improvements

```bash
# Healing trends
grep "Healing Rate" reports/self_healing/summary_*.txt

# Output shows improvement over time
# summary_20251225.txt:Healing Rate: 0.12
# summary_20251226.txt:Healing Rate: 0.08
# summary_20251227.txt:Healing Rate: 0.05
```

## CI/CD Integration

```yaml
# GitHub Actions
- name: Upload Reports
  uses: actions/upload-artifact@v4
  with:
    name: test-reports-${{ github.run_number }}
    path: |
      reports/test_report_*.html
      reports/self_healing/
```

## Troubleshooting

**No reports:**
```bash
# Create directory
mkdir -p reports/self_healing

# Check config
grep "html" pytest.ini
```

**Can't open:**
```bash
# Check file
ls -lh reports/test_report_*.html

# Fix permissions
chmod 644 reports/test_report_*.html
```

**Too many reports:**
```bash
# Check usage
du -sh reports/

# Clean
./view_reports.sh --clean 7
```

## Helper Script Reference

```bash
./view_reports.sh              # Latest (default)
./view_reports.sh --latest     # Same as above
./view_reports.sh --all        # List all
./view_reports.sh --self-healing  # Healing summary
./view_reports.sh --clean 30   # Clean old
./view_reports.sh --help       # Help
```

## Best Practices

1. Clean reports regularly (weekly/monthly)
2. Archive important runs (releases)
3. Review healing reports for trends
4. Compare pass rates over time
5. Use helper script for management

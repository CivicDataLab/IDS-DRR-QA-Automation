# Multi-State Analytics Testing Framework

## Overview

The Multi-State Analytics Testing Framework provides an automated, scalable solution for testing analytics indicators across multiple Indian states in the IDS-DRR application. This framework automatically discovers available indicators for each state and generates dynamic, data-driven tests.

## Key Features

### 🚀 Automated Discovery
- Automatically discovers all available indicators for each state
- Generates YAML configuration files for easy management
- No manual indicator mapping required

### 📊 Dynamic Test Generation
- Tests are dynamically generated from configuration files
- Add new states without changing test code
- Pytest parametrization for efficient execution

### ⚡ Parallel Execution
- Built-in support for parallel test execution
- Significantly reduces test execution time
- Configurable worker count

### 📈 Enhanced Reporting
- State-wise test result aggregation
- Section-level coverage reports
- HTML and JSON output formats
- Cross-state comparison analytics

### 🔄 Self-Healing
- Integrates with existing self-healing locator framework
- Automatic locator updates when UI changes
- Reduced maintenance overhead

## Architecture

```
IDS-DRR-QA-Automation/
├── config/states/              # Auto-generated state configurations
│   ├── assam.yaml
│   ├── himachal_pradesh.yaml
│   ├── odisha.yaml
│   ├── bihar.yaml
│   ├── uttar_pradesh.yaml
│   └── states_master.yaml      # Master index file
├── tests/
│   └── test_analytics.py  # Multi-state test suite
├── utils/
│   ├── state_indicator_discovery.py  # Discovery utility
│   ├── state_config_loader.py        # Config loader
│   └── pytest_multistate_plugin.py   # Reporting plugin
├── scripts/
│   └── discover_state_indicators.py  # CLI discovery tool
└── docs/
    └── MULTISTATE_TESTING_GUIDE.md   # This file
```

## Quick Start

### Step 1: Discover State Indicators

Run the discovery script to automatically detect all available indicators:

```bash
# Discover all states
python scripts/discover_state_indicators.py

# Discover specific states only
python scripts/discover_state_indicators.py --states Assam "Himachal pradesh"

# Force overwrite existing configs
python scripts/discover_state_indicators.py --force
```

This will:
- Navigate to the analytics page for each state
- Automatically detect all available indicators in each section (Hazard, Exposure, Vulnerability, Government Response)
- Generate YAML configuration files in `config/states/`
- Create a master index file for quick reference

### Step 2: Validate Configurations

Validate that all configurations were generated correctly:

```bash
python scripts/discover_state_indicators.py --validate
```

### Step 3: Run Multi-State Tests

```bash
# Run all multi-state tests
pytest tests/test_analytics.py -v

# Run tests for a specific state
pytest tests/test_analytics.py -v -k "assam"

# Run tests for a specific section
pytest tests/test_analytics.py -v -k "hazard"

# Run with parallel execution (4 workers)
pytest tests/test_analytics.py -v -n 4

# Generate HTML report
pytest tests/test_analytics.py -v --html=reports/multistate_report.html
```

## Configuration Files

### State Configuration Format

Each state has a YAML configuration file (`config/states/{state_key}.yaml`):

```yaml
state_name: Assam
state_key: assam
discovered_at: '2024-01-15T10:30:00'
sections:
  hazard:
    name: Hazard
    indicators:
      - name: Total Monthly Rainfall
        key: total_monthly_rainfall
        position: 1
        enabled: true
        section: Hazard
      - name: Sum of Inundation Intensities
        key: sum_of_inundation_intensities
        position: 2
        enabled: true
        section: Hazard
  exposure:
    name: Exposure
    indicators:
      - name: Total Households
        key: total_households
        position: 1
        enabled: true
        section: Exposure
  # ... more sections
```

### Master Configuration

The master config (`config/states/states_master.yaml`) provides a quick overview:

```yaml
discovery_timestamp: '2024-01-15T10:30:00'
total_states: 5
states:
  assam:
    name: Assam
    config_file: assam.yaml
    total_indicators: 29
    sections:
      hazard: 3
      exposure: 4
      vulnerability: 16
      government_response: 6
  # ... more states
```

## Test Structure

### Test Classes

The framework includes several test classes:

#### 1. `TestMultiStateIndicators`
Tests individual indicators across all states:
- Navigates to analytics page
- Selects target state
- Expands appropriate section
- Validates indicator loads correctly
- Takes screenshot for verification

#### 2. `TestMultiStateBasicFunctionality`
Smoke tests for basic functionality:
- State selection validation
- Configuration validation
- Indicator availability checks

#### 3. `TestSectionCoverageByState`
Complete section coverage tests:
- Tests all indicators in each section
- Validates section expand/collapse
- Reports section-level success rates

#### 4. `TestCrossStateComparison`
Cross-state analysis:
- Validates common sections across states
- Generates coverage comparison reports
- Identifies inconsistencies

#### 5. `TestAllStatesIndicatorSmoke` (NEW)
Comprehensive smoke test for all states:
- Tests all 5 states in a single flow
- For each state validates:
  - State selection from dropdown
  - View selection (Map view)
  - District dropdown selection
  - Revenue circle dropdown selection
  - Section expand (Hazard)
  - Indicator selection
- Provides detailed pass/fail reporting per state
- Ideal for quick validation after deployments

```bash
# Run the all-states smoke test
pytest -m smoke -k "TestAllStatesIndicatorSmoke" -v
```

## Usage Examples

### Test Specific State and Section

```bash
pytest tests/test_analytics.py -v -k "assam and hazard"
```

### Test All Exposure Indicators Across All States

```bash
pytest tests/test_analytics.py::TestSectionCoverageByState::test_exposure_section_coverage -v
```

### Run Smoke Tests Only

```bash
pytest tests/test_analytics.py -v -m smoke
```

### Run All-States Comprehensive Smoke Test

```bash
# Tests all 5 states with expanded options (district, revenue circle, indicator)
pytest -m smoke -k "TestAllStatesIndicatorSmoke" -v
```

### Parallel Execution with Custom Workers

```bash
pytest tests/test_analytics.py -v -n 8
```

### Generate Multiple Report Formats

```bash
pytest tests/test_analytics.py -v \
  --html=reports/multistate.html \
  --self-contained-html \
  -n 4
```

## Reporting

### Console Report

After test execution, a detailed console report is generated:

```
================================================================================
                         MULTI-STATE TEST SUMMARY
================================================================================

Overall Results:
  Total States Tested: 5
  Total Tests: 145
  ✅ Passed: 142 (97.9%)
  ❌ Failed: 3 (2.1%)
  ⏭️  Skipped: 0
  ⏱️  Duration: 245.67s

--------------------------------------------------------------------------------
State-wise Breakdown:
--------------------------------------------------------------------------------

✅ Assam:
     Tests: 29/29 passed (100.0%)
     Sections:
       • Hazard: 3/3 (100.0%)
       • Exposure: 4/4 (100.0%)
       • Vulnerability: 16/16 (100.0%)
       • Government Response: 6/6 (100.0%)

⚠️ Himachal Pradesh:
     Tests: 27/29 passed (93.1%)
     Sections:
       • Hazard: 3/3 (100.0%)
       • Exposure: 4/4 (100.0%)
       • Vulnerability: 14/16 (87.5%)
       • Government Response: 6/6 (100.0%)

# ... more states
```

### HTML Report

Beautiful HTML reports with:
- Visual pass/fail indicators
- Progress bars for each state
- Section-level breakdowns
- Interactive filtering

Location: `reports/multistate/multistate_summary_{timestamp}.html`

### JSON Report

Machine-readable JSON for CI/CD integration:

```json
{
  "timestamp": "2024-01-15T12:30:00",
  "duration_seconds": 245.67,
  "summary": {
    "total_states": 5,
    "total_tests": 145,
    "total_passed": 142,
    "total_failed": 3
  },
  "states": {
    "assam": {
      "stats": { ... },
      "results": { ... }
    }
  }
}
```

Location: `reports/multistate/multistate_report_{timestamp}.json`

## Adding New States

To add a new state:

1. **Run Discovery** for the new state:
   ```bash
   python scripts/discover_state_indicators.py --states "New State Name"
   ```

2. **Validate** the configuration:
   ```bash
   python scripts/discover_state_indicators.py --validate
   ```

3. **Run Tests**:
   ```bash
   pytest tests/test_analytics.py -v -k "new_state"
   ```

That's it! No code changes required.

## Customization

### Filtering States

Edit the test to run only specific states:

```python
# In test_analytics.py
ENABLED_STATES = ["assam", "odisha"]  # Only test these states

def get_multistate_test_params():
    return config_loader.get_test_parameters(states=ENABLED_STATES)
```

### Filtering Sections

Test specific sections only:

```python
def get_multistate_test_params():
    return config_loader.get_test_parameters(
        sections=["hazard", "exposure"]
    )
```

### Disabling Specific Indicators

Edit the state YAML file and set `enabled: false`:

```yaml
indicators:
  - name: Some Indicator
    key: some_indicator
    enabled: false  # This indicator will be skipped
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Multi-State Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Multi-State Tests
        run: |
          pytest tests/test_analytics.py -v -n 4 \
            --html=reports/multistate.html
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: multistate-report
          path: reports/
```

## Troubleshooting

### Issue: Discovery fails for a state

**Solution**: Check if the state name matches exactly (case-insensitive matching is applied). Verify network connectivity and application availability.

### Issue: Tests fail for specific indicators

**Solution**:
1. Check if the indicator is actually available for that state
2. Review the screenshot in the reports directory
3. Check the self-healing logs for locator issues

### Issue: Parallel execution causes failures

**Solution**:
- Reduce worker count: `-n 2` instead of `-n 4`
- Check for shared state or resource conflicts
- Ensure each test is independent

### Issue: Configuration out of date

**Solution**: Re-run discovery with `--force` flag:
```bash
python scripts/discover_state_indicators.py --force
```

## Performance Optimization

### Recommended Settings

For optimal performance:

```bash
# 4 parallel workers, optimized reporting
pytest tests/test_analytics.py -v -n 4 \
  --tb=short \
  --maxfail=10 \
  -q
```

### Execution Time Estimates

- Single state (full suite): ~2-3 minutes
- All 5 states (sequential): ~10-15 minutes
- All 5 states (4 workers): ~4-6 minutes

## Best Practices

1. **Regular Discovery**: Run discovery weekly or when UI changes are deployed
2. **Version Control**: Commit generated YAML configs to track changes
3. **Validation**: Always validate configs after discovery
4. **Parallel Execution**: Use `-n 4` for CI/CD, `-n 2` for local development
5. **Selective Testing**: Use markers and filters during development
6. **Review Reports**: Check HTML reports for visual validation

## Support

For issues or questions:
1. Check this documentation
2. Review test output and error messages
3. Check generated screenshots in `screenshots/analytics/`
4. Review self-healing logs in `reports/self_healing/`

## Changelog

### Version 1.0.0 (Current)
- ✅ Automated state indicator discovery
- ✅ Dynamic test generation
- ✅ Parallel execution support
- ✅ Enhanced multi-state reporting
- ✅ Self-healing locator integration
- ✅ 5 states supported (Assam, Himachal Pradesh, Odisha, Bihar, Uttar Pradesh)

### Roadmap
- [ ] Add Chart and Table view testing
- [ ] Add district-level multi-state testing
- [ ] Add performance benchmarking across states
- [ ] Add visual regression testing
- [ ] Add API-level indicator validation

# 🌍 Multi-State Analytics Testing Framework

> Automated, scalable testing for analytics indicators across multiple Indian states

## What is This?

A complete automation framework that **automatically discovers** and **dynamically tests** all analytics indicators across multiple states (Assam, Himachal Pradesh, Odisha, Bihar, Uttar Pradesh) with **zero manual configuration**.

## ✨ Key Features

- 🔍 **Auto-Discovery**: Automatically detects all available indicators for each state
- 🎯 **Data-Driven**: Tests generated dynamically from YAML configurations
- ⚡ **Parallel Execution**: Run tests 4x faster with parallel workers
- 📊 **Rich Reporting**: State-wise HTML/JSON reports with coverage analysis
- 🔄 **Self-Healing**: Integrates with self-healing locators
- 📈 **Scalable**: Add new states without code changes

## 🚀 Quick Start

### 1. Discover State Indicators
```bash
python scripts/discover_state_indicators.py
```

### 2. Run Multi-State Tests
```bash
pytest tests/test_analytics_multistate.py -v -n 4
```

### 3. View Reports
```bash
open reports/multistate/multistate_summary_*.html
```

**That's it!** 🎉

## 📖 Documentation

- **[Quick Start Guide](docs/MULTISTATE_QUICKSTART.md)** - Get running in 5 minutes
- **[Complete Guide](docs/MULTISTATE_TESTING_GUIDE.md)** - Full documentation

## 🏗️ What Was Built

### New Files Created

```
utils/
├── state_indicator_discovery.py     # Auto-discovery utility
├── state_config_loader.py           # Configuration loader
└── pytest_multistate_plugin.py      # Enhanced reporting plugin

tests/
└── test_analytics_multistate.py     # Multi-state test suite

scripts/
└── discover_state_indicators.py     # CLI discovery tool

config/states/                        # Auto-generated configs
├── assam.yaml
├── himachal_pradesh.yaml
├── odisha.yaml
├── bihar.yaml
├── uttar_pradesh.yaml
└── states_master.yaml

docs/
├── MULTISTATE_TESTING_GUIDE.md      # Full documentation
└── MULTISTATE_QUICKSTART.md         # Quick start guide
```

### Modified Files

- `pages/analytics_page.py` - Added state selection methods
- `conftest.py` - Registered multi-state plugin

## 🎯 Use Cases

### Test All States (Parallel)
```bash
pytest tests/test_analytics_multistate.py -v -n 4
```

### Test Single State
```bash
pytest tests/test_analytics_multistate.py -v -k "assam"
```

### Test Single Section Across All States
```bash
pytest tests/test_analytics_multistate.py -v -k "hazard"
```

### Test Specific State + Section
```bash
pytest tests/test_analytics_multistate.py -v -k "assam and exposure"
```

### Smoke Tests Only
```bash
pytest tests/test_analytics_multistate.py -v -m smoke
```

## 📊 Sample Report Output

```
================================================================================
                         MULTI-STATE TEST SUMMARY
================================================================================

Overall Results:
  Total States Tested: 5
  Total Tests: 145
  ✅ Passed: 142 (97.9%)
  ❌ Failed: 3 (2.1%)
  Duration: 245.67s

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

...
```

## 🔮 Adding New States

Adding a new state is **literally this simple**:

```bash
# 1. Discover the new state
python scripts/discover_state_indicators.py --states "New State Name"

# 2. Run tests
pytest tests/test_analytics_multistate.py -v -k "new_state"
```

**No code changes required!** ✨

## 🏆 Benefits

### For Developers
- No manual indicator mapping
- Automatic test generation
- Quick feedback with parallel execution
- Easy debugging with screenshots

### For QA
- Comprehensive state coverage
- Visual HTML reports
- Cross-state comparison
- Automated regression testing

### For CI/CD
- JSON reports for parsing
- Parallel execution support
- Stable, self-healing tests
- Clear pass/fail metrics

## 📈 Performance

| Execution Mode | Time |
|----------------|------|
| Single state (sequential) | ~2-3 minutes |
| All 5 states (sequential) | ~10-15 minutes |
| All 5 states (4 workers) | ~4-6 minutes |

**~70% time savings with parallel execution!**

## 🛠️ Technical Architecture

### Discovery Process
1. Navigates to analytics page
2. Selects each state from dropdown
3. Expands each section (Hazard, Exposure, Vulnerability, Gov Response)
4. Discovers all available indicators
5. Generates YAML configuration files

### Test Execution
1. Loads state configurations from YAML
2. Generates test parameters dynamically
3. Pytest parametrizes tests for each state+indicator combination
4. Runs tests in parallel (optional)
5. Aggregates results by state and section
6. Generates multi-format reports

### Configuration Format
```yaml
state_name: Assam
state_key: assam
sections:
  hazard:
    name: Hazard
    indicators:
      - name: Total Monthly Rainfall
        key: total_monthly_rainfall
        enabled: true
        section: Hazard
```

## 🔄 Maintenance

### When to Re-discover
- After UI updates
- When new indicators are added
- When states are added/removed
- Monthly (as best practice)

### How to Re-discover
```bash
python scripts/discover_state_indicators.py --force
```

## 🎓 Learning Resources

- [Quick Start Guide](docs/MULTISTATE_QUICKSTART.md) - 5-minute tutorial
- [Complete Guide](docs/MULTISTATE_TESTING_GUIDE.md) - Deep dive
- [Architecture](docs/MULTISTATE_TESTING_GUIDE.md#architecture) - Technical details
- [Best Practices](docs/MULTISTATE_TESTING_GUIDE.md#best-practices) - Tips & tricks

## 🤝 Contributing

To extend the framework:
1. Add discovery logic in `utils/state_indicator_discovery.py`
2. Update test logic in `tests/test_analytics_multistate.py`
3. Enhance reporting in `utils/pytest_multistate_plugin.py`
4. Update documentation in `docs/`

## 📝 Version History

### v1.0.0 - Initial Release
- ✅ Automated state discovery
- ✅ Dynamic test generation
- ✅ Parallel execution support
- ✅ Multi-format reporting
- ✅ Self-healing integration
- ✅ 5 states supported

### Roadmap
- Chart/Table view testing
- District-level testing
- Performance benchmarking
- Visual regression testing
- API validation

## 🙏 Credits

Built for the IDS-DRR QA Automation project to enable comprehensive, scalable multi-state analytics testing.

---

**Ready to test at scale?** Start with the [Quick Start Guide](docs/MULTISTATE_QUICKSTART.md)!

# Multi-State Testing - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Discover Indicators

```bash
python scripts/discover_state_indicators.py
```

This will automatically:
- Open the application in a browser
- Navigate through each state (Assam, Himachal Pradesh, Odisha, Bihar, Uttar Pradesh)
- Discover all available indicators in each section
- Generate YAML configuration files in `config/states/`

**Expected Output:**
```
Starting Multi-State Indicator Discovery...
Navigating to analytics page...
Discovering indicators for: Assam
  ✅ Hazard: 3 indicators
  ✅ Exposure: 4 indicators
  ✅ Vulnerability: 16 indicators
  ✅ Government Response: 6 indicators
...
✅ Saved Assam configuration to config/states/assam.yaml
```

**Duration:** ~5-10 minutes for all states

---

### Step 2: Validate Configurations

```bash
python scripts/discover_state_indicators.py --validate
```

**Expected Output:**
```
VALIDATING STATE CONFIGURATIONS
✅ Found 5 state configurations

Assam (assam):
  Total Indicators: 29
  Sections:
    • Hazard: 3 indicators
    • Exposure: 4 indicators
    • Vulnerability: 16 indicators
    • Government Response: 6 indicators
  ✅ All required sections present

✅ ALL CONFIGURATIONS VALID
```

---

### Step 3: Run Tests

```bash
# Run all tests with parallel execution
pytest tests/test_analytics_multistate.py -v -n 4
```

**Expected Output:**
```
tests/test_analytics_multistate.py::TestMultiStateIndicators::test_indicator_loads_for_state[assam-Assam-hazard-total_monthly_rainfall-Total Monthly Rainfall] PASSED
tests/test_analytics_multistate.py::TestMultiStateIndicators::test_indicator_loads_for_state[assam-Assam-hazard-sum_of_inundation_intensities-Sum of Inundation Intensities] PASSED
...

================================================================================
                         MULTI-STATE TEST SUMMARY
================================================================================

Overall Results:
  Total States Tested: 5
  Total Tests: 145
  ✅ Passed: 145 (100.0%)
  ❌ Failed: 0 (0.0%)
  Duration: 245.67s
```

---

## 📊 View Reports

After running tests, check the reports:

### HTML Report
```bash
open reports/multistate/multistate_summary_*.html
```

### JSON Report
```bash
cat reports/multistate/multistate_report_*.json
```

---

## 🎯 Common Use Cases

### Test Single State
```bash
pytest tests/test_analytics_multistate.py -v -k "assam"
```

### Test Single Section (All States)
```bash
pytest tests/test_analytics_multistate.py -v -k "hazard"
```

### Test Specific State + Section
```bash
pytest tests/test_analytics_multistate.py -v -k "assam and hazard"
```

### Run Smoke Tests Only
```bash
pytest tests/test_analytics_multistate.py -v -m smoke
```

### Generate HTML Report
```bash
pytest tests/test_analytics_multistate.py -v --html=reports/my_report.html
```

---

## 🔄 Re-discover When UI Changes

If the application UI is updated:

```bash
# Re-run discovery (overwrites existing configs)
python scripts/discover_state_indicators.py --force
```

---

## 📁 Generated Files

After discovery, you'll have:

```
config/states/
├── assam.yaml                  # Assam indicators
├── himachal_pradesh.yaml       # Himachal Pradesh indicators
├── odisha.yaml                 # Odisha indicators
├── bihar.yaml                  # Bihar indicators
├── uttar_pradesh.yaml          # Uttar Pradesh indicators
└── states_master.yaml          # Master index
```

---

## ⚡ Performance Tips

**For CI/CD:**
```bash
pytest tests/test_analytics_multistate.py -v -n 4 --tb=short
```

**For Local Development:**
```bash
pytest tests/test_analytics_multistate.py -v -n 2 -k "assam"
```

**For Debugging:**
```bash
pytest tests/test_analytics_multistate.py -v -s -k "specific_test_name"
```

---

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Discovery fails | Check network connectivity and application URL |
| Tests fail for new state | Re-run discovery with `--force` |
| Parallel execution issues | Reduce workers: `-n 2` |
| Old configurations | Run `python scripts/discover_state_indicators.py --force` |

---

## 📚 Full Documentation

For detailed information, see [MULTISTATE_TESTING_GUIDE.md](MULTISTATE_TESTING_GUIDE.md)

---

## 🎉 You're All Set!

The framework is now ready to:
- ✅ Test all 5 states automatically
- ✅ Discover and adapt to UI changes
- ✅ Run tests in parallel for speed
- ✅ Generate comprehensive reports
- ✅ Scale to additional states effortlessly

**Next Steps:**
1. Review the generated YAML configs in `config/states/`
2. Run tests locally to verify everything works
3. Integrate into your CI/CD pipeline
4. Set up automated discovery runs when UI changes

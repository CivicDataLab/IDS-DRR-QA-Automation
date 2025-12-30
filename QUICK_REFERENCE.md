# Multi-State Testing - Quick Reference Card

## 🎯 Common Commands

### Discovery
```bash
# Discover all states
python scripts/discover_state_indicators.py

# Force update configs
python scripts/discover_state_indicators.py --force

# Validate configs
python scripts/discover_state_indicators.py --validate
```

### Testing
```bash
# All states (parallel)
pytest tests/test_analytics_multistate.py -v -n 4

# Single state
pytest tests/test_analytics_multistate.py -v -k "assam"

# Single section
pytest tests/test_analytics_multistate.py -v -k "hazard"

# State + section
pytest tests/test_analytics_multistate.py -v -k "assam and hazard"

# Smoke tests
pytest tests/test_analytics_multistate.py -v -m smoke

# With HTML report
pytest tests/test_analytics_multistate.py -v --html=reports/my_report.html
```

### Environment Setup
```bash
# Test against DEV
echo "DEV_URL='https://drr-dev.open-contracting.in/'" >> .env

# Test against PROD (remove DEV_URL)
sed -i '/DEV_URL/d' .env
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `scripts/discover_state_indicators.py` | Run discovery |
| `tests/test_analytics_multistate.py` | Multi-state tests |
| `config/states/*.yaml` | State configurations |
| `config/states/states_master.yaml` | Master index |
| `docs/MULTISTATE_QUICKSTART.md` | Quick start guide |
| `docs/MULTISTATE_TESTING_GUIDE.md` | Full documentation |

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Required
URL='https://drr.open-contracting.in/'
HOME_URL_USERNAME='username'
HOME_URL_PASSWORD='password'

# Optional - for dev testing
DEV_URL='https://drr-dev.open-contracting.in/'

# Browser settings
HEADLESS=false
DEFAULT_TIMEOUT=10
```

### Supported States
- Assam
- Himachal pradesh
- Odisha
- Bihar
- Uttar pradesh

## 📊 Reports Location

| Report Type | Location |
|-------------|----------|
| HTML Summary | `reports/multistate/multistate_summary_*.html` |
| JSON Data | `reports/multistate/multistate_report_*.json` |
| Screenshots | `screenshots/analytics/` |
| Test Reports | `reports/multistate_test_report.html` |

## 🎨 Markers

```bash
-m smoke          # Smoke tests only
-m analytics      # Analytics tests
-m multistate     # Multi-state tests
-m section_coverage  # Section coverage tests
-m cross_state    # Cross-state comparison
```

## ⚡ Performance Tips

```bash
# Fast (4 workers)
pytest tests/test_analytics_multistate.py -v -n 4

# Debug (no parallel, verbose)
pytest tests/test_analytics_multistate.py -v -s

# CI/CD optimized
pytest tests/test_analytics_multistate.py -v -n 4 --tb=short -q
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Discovery fails | Check network, verify DEV_URL/URL |
| Tests fail | Re-run discovery with `--force` |
| Parallel issues | Reduce workers: `-n 2` |
| Missing configs | Run `python scripts/discover_state_indicators.py` |

## 🔄 Workflow

```
1. Set DEV_URL (if testing dev)
   ↓
2. Run discovery
   ↓
3. Validate configs
   ↓
4. Run tests
   ↓
5. View reports
```

## 📞 Quick Help

```bash
# Discovery help
python scripts/discover_state_indicators.py --help

# Pytest help
pytest tests/test_analytics_multistate.py --help

# List all markers
pytest --markers

# List all tests
pytest tests/test_analytics_multistate.py --collect-only
```

## 🌟 Pro Tips

1. **Use DEV_URL for development**: Faster feedback, no prod impact
2. **Run discovery weekly**: Keep configs up to date
3. **Use parallel execution**: 4 workers = 70% time savings
4. **Check HTML reports**: Visual validation is easier
5. **Commit YAML configs**: Track indicator changes over time

## 📖 Documentation

- Quick Start: [docs/MULTISTATE_QUICKSTART.md](docs/MULTISTATE_QUICKSTART.md)
- Full Guide: [docs/MULTISTATE_TESTING_GUIDE.md](docs/MULTISTATE_TESTING_GUIDE.md)
- Overview: [MULTISTATE_FRAMEWORK.md](MULTISTATE_FRAMEWORK.md)

---

**Need more help?** Check the full documentation or implementation summary.

🤖 Claude Code - Multi-State Testing Framework

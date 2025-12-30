# Project Structure

```
IDS-DRR-QA-Automation/
│
├── tests/                    # Test files (125+ tests)
│   ├── test_analytics.py     # 50+ tests
│   ├── test_dataset.py       # 40+ tests
│   └── test_components.py    # 35+ tests
│
├── pages/                    # Page Objects
│   ├── base_page.py
│   ├── common_page.py
│   ├── analytics_page.py
│   └── dataset_page.py
│
├── locators/                 # Locators
│   ├── common_locators.py
│   ├── analytics_locators.py
│   └── dataset_locators.py
│
├── config/                   # Configuration
│   ├── config.py
│   ├── test_data.py
│   └── self_healing_config.py
│
├── utils/                    # Utilities
│   ├── driver_factory.py
│   └── self_healing.py
│
├── .github/workflows/        # GitHub Actions
│   ├── test-automation.yml
│   └── README.md
│
├── conftest.py              # Pytest fixtures
├── pytest.ini               # Pytest config
├── requirements.txt         # Dependencies
├── .env.example             # Env template
├── run_tests.sh             # Test runner
├── run_parallel_tests.sh    # Parallel runner
└── view_reports.sh          # Report viewer
```

## Metrics

- **Tests**: 125+
- **Test Files**: 3
- **Test Classes**: 27
- **Markers**: 9
- **Page Objects**: 4
- **Locator Files**: 3

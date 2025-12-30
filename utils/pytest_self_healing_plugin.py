"""
Pytest plugin for self-healing test reporting and management
"""

import pytest
import json
import os
from datetime import datetime
from pathlib import Path


class SelfHealingPlugin:
    """Plugin to track and report self-healing activities during test runs"""

    def __init__(self):
        self.healing_events = []
        self.test_results = {}
        self.report_dir = "reports/self_healing"
        os.makedirs(self.report_dir, exist_ok=True)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Capture test results and healing information"""
        outcome = yield
        report = outcome.get_result()

        if report.when == "call":
            test_name = item.nodeid

            # Try to get healing report from the test's driver/page objects
            if hasattr(item, 'funcargs'):
                driver = item.funcargs.get('driver')
                if driver and hasattr(driver, '_healing_events'):
                    self.healing_events.extend(driver._healing_events)

            self.test_results[test_name] = {
                "outcome": report.outcome,
                "duration": report.duration,
                "timestamp": datetime.now().isoformat()
            }

    def pytest_sessionfinish(self, session, exitstatus):
        """Generate healing report at end of test session"""
        self._generate_healing_report()

    def _generate_healing_report(self):
        """Generate comprehensive healing and test results report"""
        # Calculate test statistics
        total_tests = len(self.test_results)
        passed = sum(1 for r in self.test_results.values() if r['outcome'] == 'passed')
        failed = sum(1 for r in self.test_results.values() if r['outcome'] == 'failed')
        healing_events = len(self.healing_events)

        # Calculate pass rate and healing rate
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        healing_rate = (healing_events / total_tests) if total_tests > 0 else 0

        report_file = os.path.join(
            self.report_dir,
            f"self_healing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        # Ensure directory exists before writing
        os.makedirs(self.report_dir, exist_ok=True)

        report_data = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed": passed,
                "failed": failed,
                "pass_rate": round(pass_rate, 2),
                "total_healing_events": healing_events,
                "healing_rate_per_test": round(healing_rate, 2)
            },
            "test_results": self.test_results,
            "healing_events": self.healing_events
        }

        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"\n{'='*70}")
        print(f"📊 Self-Healing Test Report Generated")
        print(f"{'='*70}")
        print(f"   Report Location: {report_file}")
        print(f"   Total Tests: {total_tests} | Passed: {passed} | Failed: {failed}")
        print(f"   Pass Rate: {pass_rate:.2f}%")
        print(f"   Self-Healing Events: {healing_events}")
        print(f"   Healing Rate: {healing_rate:.2f} events/test")
        print(f"{'='*70}\n")


def pytest_configure(config):
    """Register the self-healing plugin"""
    config.pluginmanager.register(SelfHealingPlugin(), "self_healing_plugin")

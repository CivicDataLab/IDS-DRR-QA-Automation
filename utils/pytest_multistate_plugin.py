"""
Pytest Plugin for Multi-State Test Reporting

Provides enhanced reporting for multi-state analytics tests including:
- State-wise test results aggregation
- Indicator coverage matrix
- Section-wise success rates
- Cross-state comparison reports
"""

import pytest
import json
import os
from datetime import datetime
from collections import defaultdict


class MultiStateReportPlugin:
    """Enhanced reporting for multi-state tests"""

    def __init__(self):
        self.test_results = defaultdict(lambda: defaultdict(list))
        self.state_stats = defaultdict(lambda: {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "sections": defaultdict(lambda: {
                "total": 0,
                "passed": 0,
                "failed": 0
            })
        })
        self.start_time = None
        self.end_time = None

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Capture test results"""
        outcome = yield
        report = outcome.get_result()

        # Only process call phase (actual test execution)
        if report.when == "call":
            # Check if this is a multi-state test
            if hasattr(item, 'callspec'):
                params = item.callspec.params

                if 'state_key' in params or 'state_name' in params:
                    state_key = params.get('state_key', 'unknown')
                    state_name = params.get('state_name', state_key)
                    section = params.get('section', 'general')
                    indicator = params.get('indicator_name', params.get('indicator_key', 'unknown'))

                    # Record result
                    result_data = {
                        "test_name": item.name,
                        "state_key": state_key,
                        "state_name": state_name,
                        "section": section,
                        "indicator": indicator,
                        "outcome": report.outcome,
                        "duration": report.duration,
                        "nodeid": item.nodeid
                    }

                    self.test_results[state_key][section].append(result_data)

                    # Update stats
                    stats = self.state_stats[state_key]
                    stats["total"] += 1

                    if report.outcome == "passed":
                        stats["passed"] += 1
                        stats["sections"][section]["passed"] += 1
                    elif report.outcome == "failed":
                        stats["failed"] += 1
                        stats["sections"][section]["failed"] += 1
                    elif report.outcome == "skipped":
                        stats["skipped"] += 1

                    stats["sections"][section]["total"] += 1

    def pytest_sessionstart(self, session):
        """Capture session start time"""
        self.start_time = datetime.now()

    def pytest_sessionfinish(self, session, exitstatus):
        """Generate reports at end of session"""
        self.end_time = datetime.now()

        # Generate reports
        self._generate_console_report()
        self._generate_json_report()
        self._generate_html_summary()

    def _generate_console_report(self):
        """Print console summary report"""
        print("\n\n" + "="*80)
        print(" "*25 + "MULTI-STATE TEST SUMMARY")
        print("="*80 + "\n")

        if not self.state_stats:
            print("No multi-state tests detected.\n")
            return

        # Overall summary
        total_tests = sum(stats["total"] for stats in self.state_stats.values())
        total_passed = sum(stats["passed"] for stats in self.state_stats.values())
        total_failed = sum(stats["failed"] for stats in self.state_stats.values())
        total_skipped = sum(stats["skipped"] for stats in self.state_stats.values())

        print(f"Overall Results:")
        print(f"  Total States Tested: {len(self.state_stats)}")
        print(f"  Total Tests: {total_tests}")
        print(f"  ✅ Passed: {total_passed} ({total_passed/total_tests*100:.1f}%)")
        print(f"  ❌ Failed: {total_failed} ({total_failed/total_tests*100:.1f}%)")
        print(f"  ⏭️  Skipped: {total_skipped}")

        duration = (self.end_time - self.start_time).total_seconds()
        print(f"  ⏱️  Duration: {duration:.2f}s")

        # Per-state breakdown
        print("\n" + "-"*80)
        print("State-wise Breakdown:")
        print("-"*80 + "\n")

        for state_key, stats in sorted(self.state_stats.items()):
            state_name = state_key.replace('_', ' ').title()

            pass_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            status_icon = "✅" if pass_rate == 100 else "⚠️" if pass_rate >= 80 else "❌"

            print(f"{status_icon} {state_name}:")
            print(f"     Tests: {stats['passed']}/{stats['total']} passed ({pass_rate:.1f}%)")

            # Section breakdown
            if stats["sections"]:
                print(f"     Sections:")
                for section_key, section_stats in sorted(stats["sections"].items()):
                    section_pass_rate = (
                        section_stats["passed"] / section_stats["total"] * 100
                        if section_stats["total"] > 0 else 0
                    )
                    section_name = section_key.replace('_', ' ').title()
                    print(f"       • {section_name}: {section_stats['passed']}/{section_stats['total']} "
                          f"({section_pass_rate:.1f}%)")

            print()

        print("="*80 + "\n")

    def _generate_json_report(self):
        """Generate JSON report file"""
        report_dir = "reports/multistate"
        os.makedirs(report_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(report_dir, f"multistate_report_{timestamp}.json")

        report_data = {
            "timestamp": self.end_time.isoformat(),
            "duration_seconds": (self.end_time - self.start_time).total_seconds(),
            "summary": {
                "total_states": len(self.state_stats),
                "total_tests": sum(stats["total"] for stats in self.state_stats.values()),
                "total_passed": sum(stats["passed"] for stats in self.state_stats.values()),
                "total_failed": sum(stats["failed"] for stats in self.state_stats.values()),
                "total_skipped": sum(stats["skipped"] for stats in self.state_stats.values())
            },
            "states": {}
        }

        for state_key, stats in self.state_stats.items():
            report_data["states"][state_key] = {
                "stats": stats,
                "results": dict(self.test_results[state_key])
            }

        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"📊 JSON report saved to: {report_path}")

    def _generate_html_summary(self):
        """Generate HTML summary report"""
        report_dir = "reports/multistate"
        os.makedirs(report_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(report_dir, f"multistate_summary_{timestamp}.html")

        html_content = self._build_html_report()

        with open(report_path, 'w') as f:
            f.write(html_content)

        print(f"📊 HTML summary saved to: {report_path}")

    def _build_html_report(self):
        """Build HTML report content"""
        total_tests = sum(stats["total"] for stats in self.state_stats.values())
        total_passed = sum(stats["passed"] for stats in self.state_stats.values())
        total_failed = sum(stats["failed"] for stats in self.state_stats.values())

        pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Multi-State Test Report - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            color: #666;
            font-size: 14px;
        }}
        .state-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .state-header {{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4caf50 0%, #8bc34a 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        .section-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }}
        .section-item {{
            padding: 10px;
            background: #f9f9f9;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }}
        .passed {{ color: #4caf50; }}
        .failed {{ color: #f44336; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌍 Multi-State Analytics Test Report</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p>Duration: {(self.end_time - self.start_time).total_seconds():.2f}s</p>
    </div>

    <div class="summary">
        <div class="stat-card">
            <div class="stat-label">States Tested</div>
            <div class="stat-value">{len(self.state_stats)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Total Tests</div>
            <div class="stat-value">{total_tests}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Passed</div>
            <div class="stat-value passed">{total_passed}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Failed</div>
            <div class="stat-value failed">{total_failed}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Pass Rate</div>
            <div class="stat-value">{pass_rate:.1f}%</div>
        </div>
    </div>

    <h2>State-wise Results</h2>
"""

        # Add state cards
        for state_key, stats in sorted(self.state_stats.items()):
            state_name = state_key.replace('_', ' ').title()
            state_pass_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0

            html += f"""
    <div class="state-card">
        <div class="state-header">
            <span>{state_name}</span>
            <span>{stats['passed']}/{stats['total']} Tests</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {state_pass_rate}%">
                {state_pass_rate:.1f}%
            </div>
        </div>
        <div class="section-grid">
"""

            for section_key, section_stats in sorted(stats["sections"].items()):
                section_name = section_key.replace('_', ' ').title()
                section_pass_rate = (
                    section_stats["passed"] / section_stats["total"] * 100
                    if section_stats["total"] > 0 else 0
                )

                html += f"""
            <div class="section-item">
                <strong>{section_name}</strong><br>
                <span class="passed">{section_stats['passed']}</span> / {section_stats['total']}
                ({section_pass_rate:.1f}%)
            </div>
"""

            html += """
        </div>
    </div>
"""

        html += """
</body>
</html>
"""

        return html


def pytest_configure(config):
    """Register the plugin"""
    if not hasattr(config, '_multistate_plugin'):
        plugin = MultiStateReportPlugin()
        config._multistate_plugin = plugin
        config.pluginmanager.register(plugin, "multistate_report_plugin")

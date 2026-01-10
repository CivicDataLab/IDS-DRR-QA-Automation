#!/usr/bin/env python3
"""
Merge multiple pytest JUnit XML reports and generate a consolidated pytest-html style report.
This script is used in GitHub Actions to consolidate results from parallel test shards.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import sys


def merge_junit_xml_files(xml_files):
    """Merge multiple JUnit XML files into a single structure."""
    all_testcases = []
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    total_time = 0.0

    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Get testsuite statistics
        total_tests += int(root.get('tests', 0))
        total_failures += int(root.get('failures', 0))
        total_errors += int(root.get('errors', 0))
        total_skipped += int(root.get('skipped', 0))
        total_time += float(root.get('time', 0.0))

        # Collect all test cases
        for testsuite in root.findall('.//testsuite'):
            for testcase in testsuite.findall('testcase'):
                classname = testcase.get('classname', '')
                name = testcase.get('name', '')
                time = float(testcase.get('time', 0))
                file_path = testcase.get('file', '')
                line = testcase.get('line', '')

                # Determine status and get details
                failure = testcase.find('failure')
                error = testcase.find('error')
                skipped = testcase.find('skipped')

                if failure is not None:
                    status = 'failed'
                    message = failure.get('message', '')
                    details = failure.text or ''
                elif error is not None:
                    status = 'error'
                    message = error.get('message', '')
                    details = error.text or ''
                elif skipped is not None:
                    status = 'skipped'
                    message = skipped.get('message', '')
                    details = ''
                else:
                    status = 'passed'
                    message = ''
                    details = ''

                all_testcases.append({
                    'classname': classname,
                    'name': name,
                    'time': time,
                    'file': file_path,
                    'line': line,
                    'status': status,
                    'message': message,
                    'details': details
                })

    total_passed = total_tests - total_failures - total_errors - total_skipped
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

    return {
        'testcases': all_testcases,
        'total_tests': total_tests,
        'total_passed': total_passed,
        'total_failures': total_failures,
        'total_errors': total_errors,
        'total_skipped': total_skipped,
        'total_time': total_time,
        'pass_rate': pass_rate
    }


def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ''
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


def generate_pytest_html_report(data, output_path):
    """Generate a pytest-html style report from merged data."""
    testcases = data['testcases']

    # Read the pytest-html CSS from the actual pytest-html package if available
    # Otherwise use a simplified version
    html = f'''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Test Report</title>
    <style>
      body {{
        font-family: Helvetica, Arial, sans-serif;
        font-size: 12px;
        min-width: 1200px;
        color: #999;
      }}
      h1 {{
        font-size: 24px;
        color: black;
      }}
      h2 {{
        font-size: 16px;
        color: black;
      }}
      p {{
        color: black;
      }}
      a {{
        color: #999;
      }}
      table {{
        border-collapse: collapse;
      }}
      tbody tr:nth-child(odd) {{
        background-color: #f6f6f6;
      }}
      tbody tr:hover {{
        background-color: #e6f2ff;
      }}
      th, td {{
        padding: 12px;
        text-align: left;
        vertical-align: top;
        border: 1px solid #E6E6E6;
      }}
      th {{
        font-weight: bold;
        background-color: #3498db;
        color: white;
      }}
      .passed, .passed a {{
        color: #5cb85c;
      }}
      .failed, .error, .failed a, .error a {{
        color: #d9534f;
      }}
      .skipped, .xfailed, .xpassed, .skipped a, .xfailed a, .xpassed a {{
        color: #f0ad4e;
      }}
      .summary {{
        width: 80%;
        margin: 20px 0;
      }}
      .summary th {{
        background-color: #2c3e50;
      }}
      .summary td {{
        font-weight: bold;
      }}
      .col-result {{
        width: 80px;
      }}
      .col-name {{
        width: 400px;
      }}
      .col-duration {{
        width: 80px;
      }}
      .extra {{
        display: none;
      }}
      .collapsed {{
        display: none;
      }}
      .log {{
        background-color: #e6e6e6;
        border: 1px solid #e6e6e6;
        color: black;
        display: block;
        font-family: "Courier New", Courier, monospace;
        padding: 10px;
        white-space: pre-wrap;
        word-wrap: break-word;
      }}
    </style>
  </head>
  <body>
    <h1>Test Report</h1>
    <p>Report generated on {datetime.now().strftime('%d-%b-%Y at %H:%M:%S')} by pytest-html</p>
    <p><em>Consolidated from {len(list(Path('reports').glob('junit_shard_*.xml')))} parallel shards in GitHub Actions</em></p>

    <h2>Summary</h2>
    <table class="summary">
      <thead>
        <tr>
          <th>Tests</th>
          <th>Passed</th>
          <th>Failed</th>
          <th>Errors</th>
          <th>Skipped</th>
          <th>Pass Rate</th>
          <th>Duration</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{data['total_tests']}</td>
          <td class="passed">{data['total_passed']}</td>
          <td class="failed">{data['total_failures']}</td>
          <td class="error">{data['total_errors']}</td>
          <td class="skipped">{data['total_skipped']}</td>
          <td>{data['pass_rate']:.1f}%</td>
          <td>{data['total_time']:.2f}s</td>
        </tr>
      </tbody>
    </table>

    <h2>Results</h2>
    <table id="results-table">
      <thead>
        <tr>
          <th class="col-result">Result</th>
          <th class="col-name">Test</th>
          <th class="col-duration">Duration</th>
        </tr>
      </thead>
      <tbody>
'''

    for test in testcases:
        status_class = test['status']
        status_text = test['status'].upper()

        test_name = f"{test['classname']}.{test['name']}" if test['classname'] else test['name']

        html += f'''        <tr>
          <td class="col-result {status_class}">{status_text}</td>
          <td class="col-name">{escape_html(test_name)}</td>
          <td class="col-duration">{test['time']:.2f}s</td>
        </tr>
'''

        if test['message'] or test['details']:
            log_content = f"{escape_html(test['message'])}\n{escape_html(test['details'])}" if test['message'] else escape_html(test['details'])
            html += f'''        <tr class="extra">
          <td colspan="3">
            <div class="log">{log_content}</div>
          </td>
        </tr>
'''

    html += '''      </tbody>
    </table>
  </body>
</html>'''

    Path(output_path).write_text(html)
    print(f"✓ Generated consolidated pytest-html report: {output_path}")
    print(f"  Total: {data['total_tests']} | Passed: {data['total_passed']} | Failed: {data['total_failures']} | Errors: {data['total_errors']} | Skipped: {data['total_skipped']}")
    print(f"  Pass Rate: {data['pass_rate']:.1f}% | Duration: {data['total_time']:.2f}s")


def main():
    # Find all JUnit XML files from shards
    reports_dir = Path('reports')
    xml_files = sorted(reports_dir.glob('junit_shard_*.xml'))

    if not xml_files:
        print("Error: No JUnit XML files found matching pattern 'junit_shard_*.xml'")
        sys.exit(1)

    print(f"Found {len(xml_files)} JUnit XML files to merge")

    # Merge the results
    merged_data = merge_junit_xml_files(xml_files)

    # Generate consolidated HTML report
    output_path = reports_dir / 'report.html'
    generate_pytest_html_report(merged_data, output_path)


if __name__ == '__main__':
    main()

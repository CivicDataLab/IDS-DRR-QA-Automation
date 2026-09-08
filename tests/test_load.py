"""
Load Tests — lightweight concurrent HTTP/GraphQL probes.

Not a real load-testing tool (no Locust/k6) — deliberately so. This is
`concurrent.futures.ThreadPoolExecutor` + `requests` (both already dependencies)
firing a modest number of concurrent plain HTTP requests, to catch the dev
server falling over or degrading badly under simultaneous traffic.

Kept HTTP-only and moderate (10 concurrent x 3 waves): there's an existing,
separately-confirmed limit on how many concurrent *Selenium browsers* the dev
server tolerates well (~16, see project_idsdrr_ci_concurrency_cap), and this
suite runs alongside that in CI — an HTTP-only probe is much lighter than a
browser, so this doesn't compound with it, but it's still deliberately modest
rather than an actual stress test.

NOT in the smoke marker (too slow for the fast PR gate) and NOT run by
default in full regression — see the marker registration in pytest.ini;
wiring `not load` into the CI default is a follow-up, this is opt-in via
`-m load` for now.

Run:
    pytest tests/test_load.py -v -m load
"""

import concurrent.futures
import time

import pytest
import requests

from config.config import Config

CONCURRENCY = 10
WAVES = 3
MAX_ERROR_RATE = 0.1  # tolerate an occasional blip, not a systemic failure
P95_THRESHOLD_MS = 5000

GRAPHQL_URL = "https://hp.drr.backend.open-contracting.in/graphql"
GRAPHQL_QUERY = {"query": "{getStates{name}}"}


def _hit_get(url):
    t0 = time.monotonic()
    try:
        response = requests.get(url, timeout=15)
        return response.status_code < 500, (time.monotonic() - t0) * 1000
    except requests.RequestException:
        return False, (time.monotonic() - t0) * 1000


def _hit_graphql(url, payload):
    t0 = time.monotonic()
    try:
        response = requests.post(url, json=payload, timeout=15)
        ok = response.status_code < 500 and "errors" not in response.json()
        return ok, (time.monotonic() - t0) * 1000
    except (requests.RequestException, ValueError):
        return False, (time.monotonic() - t0) * 1000


def _run_waves(fire_one):
    """Fire CONCURRENCY requests per wave, WAVES times; return (error_rate, p95_ms)."""
    all_results = []
    for _ in range(WAVES):
        with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
            futures = [executor.submit(fire_one) for _ in range(CONCURRENCY)]
            all_results.extend(f.result() for f in futures)

    total = len(all_results)
    failures = sum(1 for ok, _ in all_results if not ok)
    latencies = sorted(latency for _, latency in all_results)
    p95_index = max(0, int(total * 0.95) - 1)
    p95 = latencies[p95_index]

    error_rate = failures / total
    print(
        f"📊 {total} requests ({CONCURRENCY} x {WAVES} waves): "
        f"{failures} failed ({error_rate:.0%}), p95={p95:.0f}ms, max={latencies[-1]:.0f}ms"
    )
    return error_rate, p95


@pytest.mark.load
class TestLoad:
    """Concurrent-request probes against the frontend and the data layer."""

    def test_home_page_under_concurrent_load(self):
        """Home page stays healthy under 10 concurrent requests x 3 waves"""
        error_rate, p95 = _run_waves(lambda: _hit_get(Config.BASE_URL))
        assert error_rate <= MAX_ERROR_RATE, f"Error rate {error_rate:.0%} exceeds {MAX_ERROR_RATE:.0%}"
        assert p95 < P95_THRESHOLD_MS, f"p95 latency {p95:.0f}ms exceeds {P95_THRESHOLD_MS}ms"

    def test_analytics_page_under_concurrent_load(self):
        """Analytics dashboard stays healthy under 10 concurrent requests x 3 waves"""
        url = f"{Config.BASE_URL.rstrip('/')}/assam/analytics?indicator=risk-score&view=map"
        error_rate, p95 = _run_waves(lambda: _hit_get(url))
        assert error_rate <= MAX_ERROR_RATE, f"Error rate {error_rate:.0%} exceeds {MAX_ERROR_RATE:.0%}"
        assert p95 < P95_THRESHOLD_MS, f"p95 latency {p95:.0f}ms exceeds {P95_THRESHOLD_MS}ms"

    def test_data_layer_graphql_under_concurrent_load(self):
        """Data layer GraphQL (getStates) stays healthy under 10 concurrent requests x 3 waves"""
        error_rate, p95 = _run_waves(lambda: _hit_graphql(GRAPHQL_URL, GRAPHQL_QUERY))
        assert error_rate <= MAX_ERROR_RATE, f"Error rate {error_rate:.0%} exceeds {MAX_ERROR_RATE:.0%}"
        assert p95 < P95_THRESHOLD_MS, f"p95 latency {p95:.0f}ms exceeds {P95_THRESHOLD_MS}ms"

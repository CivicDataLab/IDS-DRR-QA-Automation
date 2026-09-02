"""
DataSpace Availability Tests — the DataSpace instances IDS-DRR depends on.

IDS-DRR reads its datasets from CivicDataSpace. When a DataSpace host goes
down, nothing in the IDS-DRR UI suite notices: the frontend still renders and
most component tests still pass. In 2026 the production instance
(https://dataspace.open-contracting.in) served HTTP 502 for five weeks before
anyone spotted it. These checks exist so that outage is caught on day one.

These are deliberately plain HTTP probes rather than browser tests — an
availability check should not depend on Chrome starting, and a 502 is visible
in the status line long before any DOM exists to inspect.

Run:
    pytest tests/test_dataspace_availability.py -v
    pytest tests/test_dataspace_availability.py -m smoke -v
"""

import pytest
import requests

from config.config import Config

HEALTHY_STATUS = 200


def _probe(url):
    """GET a host following redirects; return the response or None on transport failure."""
    try:
        return requests.get(
            url,
            timeout=Config.HTTP_TIMEOUT,
            allow_redirects=True,
            headers={"User-Agent": "IDS-DRR-QA-Automation/availability-smoke"},
        )
    except requests.RequestException as exc:
        pytest.fail(f"DataSpace host unreachable: {url} — {type(exc).__name__}: {exc}")


@pytest.mark.component
@pytest.mark.smoke
class TestDataSpaceAvailability:
    """Availability smoke checks for the DataSpace instances behind IDS-DRR"""

    @pytest.mark.parametrize(
        "label,url",
        [
            ("dev", Config.DATASPACE_DEV_URL),
            ("prod", Config.DATASPACE_PROD_URL),
        ],
    )
    def test_dataspace_host_is_healthy(self, label, url):
        """DataSpace host answers 200 after redirects"""
        response = _probe(url)
        assert response.status_code == HEALTHY_STATUS, (
            f"DataSpace {label} host unhealthy: {url} returned "
            f"HTTP {response.status_code} (final URL: {response.url})"
        )
        print(f"✅ DataSpace {label} healthy: {url} → HTTP {response.status_code}")

    @pytest.mark.parametrize(
        "label,url",
        [
            ("dev", Config.DATASPACE_DEV_URL),
            ("prod", Config.DATASPACE_PROD_URL),
        ],
    )
    def test_dataspace_host_serves_html_body(self, label, url):
        """DataSpace host serves a non-empty HTML document, not just a bare status line"""
        response = _probe(url)

        if response.status_code != HEALTHY_STATUS:
            pytest.fail(
                f"DataSpace {label} host unhealthy: {url} returned "
                f"HTTP {response.status_code} (final URL: {response.url})"
            )

        content_type = response.headers.get("Content-Type", "")
        assert "html" in content_type.lower(), (
            f"DataSpace {label} host ({url}) did not serve HTML — "
            f"Content-Type: {content_type!r}"
        )
        assert "<html" in response.text.lower(), (
            f"DataSpace {label} host ({url}) returned HTTP 200 but no HTML document "
            f"({len(response.text)} bytes)"
        )
        print(f"✅ DataSpace {label} served HTML: {url} ({len(response.text)} bytes)")

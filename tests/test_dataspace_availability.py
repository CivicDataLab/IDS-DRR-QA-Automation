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


def _probe_graphql(url):
    """POST a trivial GraphQL query; return the response or None on transport failure."""
    try:
        return requests.post(
            url,
            timeout=Config.HTTP_TIMEOUT,
            json={"query": "{__typename}"},
            headers={
                "Content-Type": "application/json",
                "User-Agent": "IDS-DRR-QA-Automation/availability-smoke",
            },
        )
    except requests.RequestException as exc:
        pytest.fail(f"DataSpace API unreachable: {url} — {type(exc).__name__}: {exc}")


@pytest.mark.component
@pytest.mark.smoke
class TestDataSpaceApiAvailability:
    """Availability smoke checks for the DataSpace GraphQL APIs

    Separate from the web-UI checks above on purpose. The API and the frontend are
    different processes on the same host — a container and a pm2 app — and on
    2026-09-03 both went down for unrelated reasons. Either can die while the other
    stays green, so neither check substitutes for the other.
    """

    @pytest.mark.parametrize(
        "label,url",
        [
            ("dev", Config.DATASPACE_DEV_API_URL),
            ("prod", Config.DATASPACE_PROD_API_URL),
        ],
    )
    def test_dataspace_api_answers_graphql(self, label, url):
        """DataSpace GraphQL API answers a trivial query with a well-formed result"""
        response = _probe_graphql(url)

        assert response.status_code == HEALTHY_STATUS, (
            f"DataSpace {label} API unhealthy: {url} returned "
            f"HTTP {response.status_code} (body: {response.text[:200]!r})"
        )

        try:
            payload = response.json()
        except ValueError:
            pytest.fail(
                f"DataSpace {label} API ({url}) returned HTTP 200 but not JSON "
                f"— body: {response.text[:200]!r}"
            )

        # A 502 page or an nginx error would fail above; this catches a live server
        # that answers but has a broken schema.
        assert payload.get("data", {}).get("__typename"), (
            f"DataSpace {label} API ({url}) answered without a GraphQL result "
            f"— payload: {payload}"
        )
        print(f"✅ DataSpace {label} API healthy: {url} → {payload['data']['__typename']}")

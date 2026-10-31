"""
Raster API error handling - coverage for IDS-DRR-Data-Management#104.

Before #104 the raster routes (layer/views.py) let Django's Http404 propagate,
so a map client asking for a layer that does not exist got Django's HTML 404
page, and a tile failure surfaced as an HTML error. The map client parses these
responses as JSON, so the fix turns every failure into `{"error": "..."}` with
the right status code.

These are read-only GET probes of the public backend, using a geography code
that cannot exist, so they never touch real layer data.

Out of scope here: the HTTP 500 "Could not render tile" branch. It needs a
geography that exists with a corrupt raster, which cannot be produced from
outside without modifying data.

Run:
    pytest tests/test_raster_api.py -v
"""

import pytest

from utils import idsdrr_backend

UNKNOWN_LAYER = {
    "module": "flood",
    "indicator": "qa-nonexistent-indicator",
    "geography_code": "qa-nonexistent-geography",
    "period": "2026_01",
}

RASTER_ROUTES = [
    pytest.param("/raster/metadata", {}, id="metadata"),
    pytest.param("/raster/value", {"lat": "26.1", "lng": "91.7"}, id="value"),
    pytest.param("/raster/tiles/5/24/13.png", {}, id="tile"),
]


@pytest.mark.flow
@pytest.mark.negative
class TestRasterErrorResponses:
    """Raster routes answer failures with JSON bodies, not Django's HTML pages."""

    @pytest.mark.parametrize("path,extra", RASTER_ROUTES)
    def test_unknown_geography_returns_json_404(self, path, extra):
        """An unknown layer is a JSON 404 with an `error` message"""
        response = idsdrr_backend.get(path, **UNKNOWN_LAYER, **extra)

        assert response.status_code == 404, (
            f"{path}: expected 404 for an unknown geography, got {response.status_code}"
        )
        content_type = response.headers.get("Content-Type", "")
        assert content_type.startswith("application/json"), (
            f"{path}: 404 body is {content_type!r}, not JSON (looks like Django's HTML "
            f"404 page, the pre-#104 behaviour): {response.text[:120]!r}"
        )
        body = response.json()
        assert isinstance(body.get("error"), str) and body["error"], (
            f"{path}: JSON 404 has no non-empty `error` message: {body}"
        )

    def test_invalid_coordinate_returns_json_400(self):
        """A non-numeric latitude is rejected as a JSON 400 naming the bad parameter"""
        response = idsdrr_backend.get(
            "/raster/value", **{**UNKNOWN_LAYER, "lat": "abc", "lng": "91.7"}
        )

        assert response.status_code == 400, (
            f"expected 400 for lat=abc, got {response.status_code}: {response.text[:120]!r}"
        )
        assert response.headers.get("Content-Type", "").startswith("application/json")
        assert "lat" in response.json().get("error", ""), (
            f"400 body should name the invalid parameter: {response.text[:120]!r}"
        )

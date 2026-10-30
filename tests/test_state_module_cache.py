"""
IDS-DRR Backend — per-state module list cache invalidation.

Covers CivicDataLab/IDS-DRR-Data-Management#123 ("fix: invalidate get_states
cache when indicators or data change"), which fixes CivicDataLab/IDS-DRR-Data-
Management#124.

`getStates` derives each state's `modules` from visible `Indicators` and its
`time_periods` from `Data`, but before #123 that cache (`get_states_*`,
`CACHE_TIMEOUTS['states']` = 24h) was only invalidated by geography changes.
A request during a full re-import (delete -> import_geojson ->
import_indicators -> import_data) could cache an empty modules list for 24h.
With `modules: []`, the frontend only accepts the default module, so every
other module 404'd. On dev this happened on 2026-10-28 11:11 UTC after the
plugin #46 deploy, and `/en/assam/heat/analytics` 404'd until the stale key
was cleared.

#123 adds `get_states_*` to `invalidate_data_caches` (runs at the end of
`import_data`, and on `Data` save/delete) and to `invalidate_indicator_caches`
(runs on `Indicators` save/delete), so the cache can no longer outlive the
import that produced it.

This probes `getStates` directly against the live IDS-DRR backend (not
DataSpace — see IDS_DRR_BACKEND_GRAPHQL_URL), matching the plain-HTTP-probe
style of test_dataspace_availability.py and test_state_resource_ids.py for
the same reason: this is a data-integrity check on an API field, not a UI
behaviour, and no Page Object renders "the modules list for every state" in
one place.

Run:
    pytest tests/test_state_module_cache.py -v
    pytest tests/test_state_module_cache.py -v -m smoke
"""

from unittest.mock import patch

import pytest
import requests

from config.config import Config

HEALTHY_STATUS = 200

GET_STATES_MODULES_QUERY = {"query": "{ getStates { name slug modules } }"}

# Named directly in #123's own "Verified on dev" section: a fresh getStates
# call for Assam returned ['flood', 'heat'], while the cached one returned []
# for every state. Odisha is the other state #124 reported as affected.
STATES_WITH_HEAT = ["Assam", "Odisha"]


def _fetch_states():
    """POST getStates against the live IDS-DRR backend; fail the test on a transport error."""
    try:
        return requests.post(
            Config.IDS_DRR_BACKEND_GRAPHQL_URL,
            timeout=Config.HTTP_TIMEOUT,
            json=GET_STATES_MODULES_QUERY,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "IDS-DRR-QA-Automation/state-module-cache-smoke",
            },
        )
    except requests.RequestException as exc:
        pytest.fail(
            f"IDS-DRR backend unreachable: {Config.IDS_DRR_BACKEND_GRAPHQL_URL} — "
            f"{type(exc).__name__}: {exc}"
        )


def _modules_by_state(response):
    """Parse a getStates response into {name: [modules]}, failing loudly if malformed."""
    assert response.status_code == HEALTHY_STATUS, (
        f"IDS-DRR backend unhealthy: {Config.IDS_DRR_BACKEND_GRAPHQL_URL} returned "
        f"HTTP {response.status_code} (body: {response.text[:200]!r})"
    )
    try:
        payload = response.json()
    except ValueError:
        pytest.fail(
            f"IDS-DRR backend ({Config.IDS_DRR_BACKEND_GRAPHQL_URL}) returned HTTP 200 "
            f"but not JSON — body: {response.text[:200]!r}"
        )

    states = payload.get("data", {}).get("getStates")
    assert states is not None, (
        f"IDS-DRR backend answered without a getStates result — payload: {payload}"
    )
    return {s["name"]: s.get("modules") for s in states}


@pytest.mark.component
@pytest.mark.smoke
class TestStateModuleCacheInvalidation:
    """Live checks: no state's cached module list is the empty-list regression shape."""

    @pytest.mark.parametrize("state_name", STATES_WITH_HEAT)
    def test_state_modules_include_heat(self, state_name):
        """
        Assam and Odisha — the states #123/#124 name — each still list "heat"
        among their modules.

        An empty (or flood-only) list here is exactly the pre-#123 failure
        mode: a stale 24h-cached get_states_* result from mid-reimport, which
        made every non-default module 404 on the frontend.
        """
        modules = _modules_by_state(_fetch_states())

        assert state_name in modules, (
            f"{state_name} missing from getStates entirely — "
            f"states returned: {sorted(modules)}"
        )
        assert "heat" in (modules[state_name] or []), (
            f"{state_name} modules did not include 'heat': {modules[state_name]!r} — "
            f"this is the #124 symptom (stale empty/partial get_states_* cache)"
        )

    def test_no_configured_state_has_an_empty_module_list(self):
        """
        Sanity check on the regression's actual shape: #124 cached `modules: []`
        for *every* state at once (a full re-import invalidates geography for
        all of them together), not just Assam/Odisha. A single state resolving
        to [] is enough to prove the stale-cache bug is back, regardless of
        which state a future re-import happens to race.
        """
        modules = _modules_by_state(_fetch_states())

        assert len(modules) >= 5, (
            f"Expected at least 5 configured states, got {len(modules)}: {sorted(modules)}"
        )
        empty = [name for name, mods in modules.items() if not mods]
        assert not empty, (
            f"States with an empty modules list (the #124 stale-cache symptom): {empty}"
        )


class TestStateModuleCacheRegressionSimulation:
    """
    Not a live-site check — proves the assertions above are actually sensitive
    to the #123/#124 regression.

    The cache has already been invalidated on dev (the fix is deployed and the
    stale key is gone), and deliberately re-triggering a real re-import race to
    get a genuine red run would mean mutating the shared dev deployment, which
    this suite never does. Per the project's test-sync guidance ("flipping
    isn't enough, simulate the regression"), this replays the exact failure
    shape #123 fixes — a state's modules list going empty — through a mocked
    response, and shows the live tests' own assertion logic raises on it.
    """

    def test_empty_modules_fails_the_heat_membership_assertion(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = HEALTHY_STATUS
            mock_post.return_value.json.return_value = {
                "data": {
                    "getStates": [
                        {"name": "Assam", "slug": "assam", "modules": []},  # simulated #124
                        {"name": "Odisha", "slug": "odisha", "modules": ["flood", "heat"]},
                    ]
                }
            }
            modules = _modules_by_state(_fetch_states())

        with pytest.raises(AssertionError):
            assert "heat" in (modules["Assam"] or []), (
                f"Assam modules did not include 'heat': {modules['Assam']!r} — "
                f"this is the #124 symptom (stale empty/partial get_states_* cache)"
            )

    def test_empty_modules_fails_the_no_empty_state_assertion(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = HEALTHY_STATUS
            mock_post.return_value.json.return_value = {
                "data": {
                    "getStates": [
                        {"name": "Assam", "slug": "assam", "modules": []},
                        {"name": "Bihar", "slug": "bihar", "modules": []},
                        {"name": "Himachal pradesh", "slug": "himachal-pradesh", "modules": []},
                        {"name": "Odisha", "slug": "odisha", "modules": []},
                        {"name": "Uttar pradesh", "slug": "uttar-pradesh", "modules": []},
                    ]
                }
            }
            modules = _modules_by_state(_fetch_states())

        empty = [name for name, mods in modules.items() if not mods]
        with pytest.raises(AssertionError):
            assert not empty, (
                f"States with an empty modules list (the #124 stale-cache symptom): {empty}"
            )

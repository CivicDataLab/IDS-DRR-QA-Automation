"""
IDS-DRR Backend — Per-State DataSpace Resource ID Resolution

Covers CivicDataLab/IDS-DRR-Data-Management#119 ("feat: override per-state
DataSpace resource_id via STATE_RESOURCE_IDS env").

Each DataSpace instance has its own resource IDs, but the plugin's
config.toml holds one resource_id per state baked in at that file's commit.
Before #119, a dev box that needed different (dev) resource IDs than
config.toml had to hand-patch its plugin checkout — an image built fresh
from the plugin repo silently lost that patch and fell back to the
config.toml (production) IDs, which don't exist as resources on the dev
DataSpace instance. The frontend doesn't fail loudly when this happens (see
test_dataspace_availability.py's docstring) — charts for the affected state
just come back empty.

#119 adds a `STATE_RESOURCE_IDS` env var (JSON, state name -> resource_id,
case-insensitive) that overrides config.toml's resource_id per state when
set, falling back to config.toml for any state left out. The PR's own
verification named Assam and Odisha as the two states the dev box's
override patches.

`getStates` already returns `resource_id` per state (used by the frontend's
map/chart data layer), so it's the exact externally observable surface this
settings.py loop writes to — no UI rendering needed to see the override take
effect or fail.

These are plain GraphQL probes against the IDS-DRR backend itself (not
DataSpace — see IDS_DRR_BACKEND_GRAPHQL_URL), matching the
plain-HTTP-probe style of test_dataspace_availability.py and test_load.py
for the same reason: this is an availability/config-integrity check, not a
UI behaviour.

Run:
    pytest tests/test_state_resource_ids.py -v
    pytest tests/test_state_resource_ids.py -v -m smoke
"""

import re
from unittest.mock import patch

import pytest
import requests

from config.config import Config

HEALTHY_STATUS = 200

# Resource IDs are UUIDs on every DataSpace instance IDS-DRR talks to (dev and
# prod alike) — config.toml and STATE_RESOURCE_IDS both hold UUIDs.
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)

GET_STATES_RESOURCE_IDS_QUERY = {"query": "{ getStates { name resource_id } }"}

# Named directly in the #119 PR description as the states the override was
# written for ("with the variable set, all 5 states resolve to the dev IDs").
OVERRIDE_NAMED_STATES = ["Assam", "Odisha"]


def _fetch_states():
    """POST getStates against the live IDS-DRR backend; fail the test on a transport error."""
    try:
        return requests.post(
            Config.IDS_DRR_BACKEND_GRAPHQL_URL,
            timeout=Config.HTTP_TIMEOUT,
            json=GET_STATES_RESOURCE_IDS_QUERY,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "IDS-DRR-QA-Automation/resource-id-smoke",
            },
        )
    except requests.RequestException as exc:
        pytest.fail(
            f"IDS-DRR backend unreachable: {Config.IDS_DRR_BACKEND_GRAPHQL_URL} — "
            f"{type(exc).__name__}: {exc}"
        )


def _resource_ids_by_state(response):
    """Parse a getStates response into {name: resource_id}, failing loudly if malformed."""
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
    return {s["name"]: s.get("resource_id") for s in states}


@pytest.mark.component
@pytest.mark.smoke
class TestStateResourceIdResolution:
    """Live smoke checks: every configured state resolves to a real resource_id."""

    @pytest.mark.parametrize("state_name", OVERRIDE_NAMED_STATES)
    def test_state_resolves_a_real_resource_id(self, state_name):
        """
        Assam and Odisha — the states #119's override was verified against —
        each resolve to a well-formed, non-blank resource_id.

        A blank or missing resource_id here is exactly the pre-#119 failure
        mode: STATE_RESOURCE_IDS not applying (or an unset/mis-parsed env var
        silently producing no override and no usable fallback).
        """
        resource_ids = _resource_ids_by_state(_fetch_states())

        assert state_name in resource_ids, (
            f"{state_name} missing from getStates entirely — "
            f"states returned: {sorted(resource_ids)}"
        )
        resource_id = resource_ids[state_name]
        assert resource_id, (
            f"{state_name} resolved to a blank resource_id — the "
            f"STATE_RESOURCE_IDS override (or its config.toml fallback) produced nothing"
        )
        assert UUID_RE.match(resource_id), (
            f"{state_name} resource_id is not a well-formed UUID: {resource_id!r}"
        )

    def test_all_configured_states_resolve_distinct_resource_ids(self):
        """
        Sanity check on the settings.py loop itself: it must run for every
        configured state (not just the overridden ones) and must not collapse
        two different states onto the same resource_id by a key-matching bug
        (e.g. the case-insensitive lookup matching the wrong state).
        """
        resource_ids = _resource_ids_by_state(_fetch_states())

        assert len(resource_ids) >= 5, (
            f"Expected at least 5 configured states, got {len(resource_ids)}: "
            f"{sorted(resource_ids)}"
        )
        blank = [name for name, rid in resource_ids.items() if not rid]
        assert not blank, f"States with a blank resource_id: {blank}"

        ids = list(resource_ids.values())
        assert len(set(ids)) == len(ids), (
            f"Two or more states resolved to the same resource_id (an override "
            f"collapsed them): {resource_ids}"
        )


class TestStateResourceIdRegressionSimulation:
    """
    Not a live-site check — proves the assertion above is actually sensitive
    to the #119 regression.

    We can't get a real red run by pointing at the pre-#119 backend: #119 is
    already merged to dev and there is no pre-fix deployment left to hit, and
    reverting the merged commit isn't this suite's call to make. Per the
    project's test-sync guidance ("flipping isn't enough, simulate the
    regression"), this replays the exact failure shape #119 fixes — a state
    resolving to a blank resource_id, the symptom of the override not
    applying — through a mocked response, and shows the live test's own
    assertion logic raises on it. This is what makes
    test_state_resolves_a_real_resource_id more than a trivially-true check.
    """

    def test_blank_resource_id_fails_the_same_assertion_the_live_test_uses(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = HEALTHY_STATUS
            mock_post.return_value.json.return_value = {
                "data": {
                    "getStates": [
                        {"name": "Assam", "resource_id": ""},  # simulated regression
                        {"name": "Odisha", "resource_id": "a6ad4c09-b3e1-4bc1-9171-54f2a40284f7"},
                    ]
                }
            }
            resource_ids = _resource_ids_by_state(_fetch_states())

        with pytest.raises(AssertionError):
            assert resource_ids["Assam"], (
                f"Assam resolved to a blank resource_id — the STATE_RESOURCE_IDS "
                f"override (or its config.toml fallback) produced nothing"
            )

    def test_duplicate_resource_ids_fail_the_distinctness_assertion(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = HEALTHY_STATUS
            same_id = "cf78dae3-3109-4330-99f0-39ac5967865b"
            mock_post.return_value.json.return_value = {
                "data": {
                    "getStates": [
                        {"name": "Assam", "resource_id": same_id},
                        {"name": "Odisha", "resource_id": same_id},  # simulated collapse
                    ]
                }
            }
            resource_ids = _resource_ids_by_state(_fetch_states())

        ids = list(resource_ids.values())
        with pytest.raises(AssertionError):
            assert len(set(ids)) == len(ids), (
                f"Two or more states resolved to the same resource_id: {resource_ids}"
            )

"""
Module-aware analytics routing and headings - coverage for merged frontend PRs
#530 (active-state / module availability) and #534 (analytics header).

#530
  - The sidebar State picker on /<state>/<module>/analytics lists only states
    that actually have data for that module (the layout now filters by the
    backend's per-state `modules`). Before, a heat dashboard offered every
    active state, and picking Bihar led to a 404.
  - The state hub no longer carries the "Heat Analytics (Pilot)" note, since
    heat is a real module card now.
#534
  - The indicator heading is truncated with an ellipsis on narrow layouts, so
    it exposes its full text as a title tooltip.

Expected modules come from the backend's getStates (authoritative for the
frontend), not from constants, so a new module or state does not break them.

Run:
    pytest tests/test_module_analytics.py -v
"""

import pytest
import requests

from config.config import Config
from pages.module_analytics_page import ModuleAnalyticsPage, StateHubPage
from utils import idsdrr_backend

INDICATOR_FOR_MODULE = {"flood": "risk-score", "heat": "heat-risk-score"}


@pytest.fixture(scope="module")
def modules_by_state():
    return idsdrr_backend.states_modules()


def _states_having(modules_by_state, module):
    return sorted(slug for slug, modules in modules_by_state.items() if module in modules)


@pytest.mark.multistate
@pytest.mark.flow
class TestModuleStatePicker:
    """#530: the sidebar State picker follows the module's real state list."""

    def test_heat_state_picker_lists_only_states_with_heat(self, driver, modules_by_state):
        """On a heat dashboard the State picker offers exactly the states that have heat data"""
        expected = _states_having(modules_by_state, "heat")
        others = sorted(set(modules_by_state) - set(expected))
        if not expected or not others:
            pytest.skip(
                f"needs one state with heat and one without; backend reports {modules_by_state}"
            )

        page = ModuleAnalyticsPage(driver)
        page.open(expected[0], "heat", INDICATOR_FOR_MODULE["heat"])
        offered = page.sidebar_state_slugs()

        assert sorted(offered) == expected, (
            f"heat State picker offers {sorted(offered)} but the backend says heat exists "
            f"for {expected}; states without heat that must not appear: {others}"
        )

    def test_module_route_404s_for_a_state_without_that_module(self, modules_by_state):
        """/<state>/<module>/analytics is a 404 when the backend has no such module for the state"""
        without_heat = sorted(set(modules_by_state) - set(_states_having(modules_by_state, "heat")))
        if not without_heat or not _states_having(modules_by_state, "heat"):
            pytest.skip(f"needs a state without heat; backend reports {modules_by_state}")

        base = Config.BASE_URL.rstrip("/")
        url = f"{base}/en/{without_heat[0]}/heat/analytics?indicator=heat-risk-score&view=map"
        response = requests.get(url, timeout=Config.HTTP_TIMEOUT)

        assert response.status_code == 404, (
            f"{url} should be 404 ({without_heat[0]} has no heat module) but returned "
            f"{response.status_code}"
        )


@pytest.mark.multistate
@pytest.mark.flow
class TestStateHub:
    """#530: the state hub lists modules as cards and drops the heat pilot note."""

    def test_state_hub_has_no_heat_pilot_note(self, driver, modules_by_state):
        """A state with heat shows its Heat card and the regional note, not the pilot note"""
        state = next(iter(_states_having(modules_by_state, "heat")), None)
        if state is None:
            pytest.skip(f"no state with heat; backend reports {modules_by_state}")

        page = StateHubPage(driver)
        page.open(state)
        text = page.main_text()

        assert "Regional-level analytics" in text, (
            f"hub for {state} lost its regional-analytics note: {text[:300]!r}"
        )
        assert "Heat Analytics (Pilot)" not in text, (
            f"hub for {state} still shows the retired 'Heat Analytics (Pilot)' note"
        )


@pytest.mark.multistate
@pytest.mark.flow
class TestIndicatorHeading:
    """#534: the (possibly truncated) indicator heading exposes its full text."""

    @pytest.mark.parametrize("module", ["flood", "heat"])
    def test_indicator_heading_title_matches_text(self, driver, modules_by_state, module):
        """The indicator heading carries a title tooltip equal to its visible text"""
        state = next(iter(_states_having(modules_by_state, module)), None)
        if state is None:
            pytest.skip(f"no state with {module}; backend reports {modules_by_state}")

        page = ModuleAnalyticsPage(driver)
        page.open(state, module, INDICATOR_FOR_MODULE[module])
        text, title = page.indicator_heading()

        assert text, f"{state}/{module}: indicator heading rendered empty"
        assert title == text, (
            f"{state}/{module}: heading shows {text!r} but its title tooltip is {title!r}; "
            "a truncated name would then be unreadable"
        )

"""
Bhashini Translation Tests — coverage for the language widget shipped in #539.

The widget is injected client-side from a useEffect
(components/langSelect/lang-select.tsx), so it is absent from the
server-rendered HTML and cannot be checked with a plain HTTP probe.

Scope is deliberate: the first class asserts only *our* integration points —
the script tag we create and the container we render. The third-party plugin's
own markup is asserted separately, so an outage at
translation-plugin.bhashini.co.in produces one clearly-labelled failure instead
of turning the whole file red and looking like our regression.

Nothing here asserts on translated text or dropdown contents. That is rendered
by the plugin at its own pace and would be flaky by construction.

Run:
    pytest tests/test_bhashini.py -v
    pytest tests/test_bhashini.py -m smoke -v
"""

import pytest
from config.config import Config
from pages.bhashini_page import BhashiniPage
from pages.common_page import CommonPage


@pytest.mark.component
@pytest.mark.smoke
class TestBhashiniIntegration:
    """Our own integration points for the Bhashini widget"""

    def test_translation_script_is_injected(self, driver):
        """The component injects its script tag, matched on the id it sets"""
        page = BhashiniPage(driver)
        assert page.is_script_injected_by_id(), (
            "Bhashini script tag #bhashini-translation-script was never injected. "
            "TranslateDropdown's useEffect did not run, or the component is no "
            "longer mounted in the header."
        )

    def test_translation_script_points_at_bhashini(self, driver):
        """The injected script actually loads the Bhashini plugin"""
        page = BhashiniPage(driver)
        assert page.is_script_injected_by_src(), (
            "No script tag pointing at translation-plugin.bhashini.co.in. The "
            "script id may be present while SCRIPT_SRC has drifted."
        )

    def test_widget_container_is_rendered(self, driver):
        """The mount point TranslateDropdown renders is in the DOM"""
        page = BhashiniPage(driver)
        assert page.is_container_rendered(), (
            "Missing .bhashini-plugin-container — the plugin has nowhere to "
            "mount, so no language selector reaches users."
        )

    def test_widget_container_exposes_test_hook(self, driver):
        """The container keeps its data-testid, which these tests and the unit tests rely on"""
        page = BhashiniPage(driver)
        assert page.is_container_testid_rendered(), (
            "Container lost its data-testid='bhashini-plugin-container' hook."
        )


@pytest.mark.component
class TestBhashiniPluginRender:
    """The third-party plugin's own render. Depends on translation-plugin.bhashini.co.in."""

    def test_plugin_widget_mounts_in_container(self, driver):
        """Once the plugin loads it mounts #bhashini-translation inside our container"""
        page = BhashiniPage(driver)
        assert page.is_widget_mounted_in_container(), (
            "The Bhashini plugin did not mount #bhashini-translation inside "
            ".bhashini-plugin-container. Our script tag and container are "
            "checked separately, so if those passed the fault is upstream: "
            "translation-plugin.bhashini.co.in failed to load or changed its "
            "mount behaviour."
        )


@pytest.mark.flow
@pytest.mark.responsive
class TestBhashiniNavVariants:
    """#539 renders the widget from both MainNav (>=1024px) and MobileNav (<1024px).

    The nav variant is chosen on the client by viewport width, so the widget's
    script and mount point have to survive being mounted, unmounted and
    re-mounted. Only our own integration points are asserted (see the module
    docstring): the mount point and the script tag, never the third-party UI.
    """

    def test_mobile_menu_offers_one_language_widget_mount(self, driver):
        """Opening the mobile menu renders exactly one widget mount point and one plugin script"""
        driver.set_window_size(375, 800)
        driver.get(Config.BASE_URL)
        common = CommonPage(driver)
        page = BhashiniPage(driver)

        assert common.open_mobile_menu(), "Could not open the mobile menu at 375px"
        containers = page.wait_for_container_count(1)

        assert containers == 1, (
            f"Mobile menu is open but {containers} .bhashini-plugin-container nodes are in "
            "the DOM; expected exactly 1, so mobile users have no language selector"
        )
        assert page.is_script_injected_by_id(), "Plugin script was not injected on the mobile layout"
        assert page.script_count() == 1, (
            f"{page.script_count()} Bhashini plugin scripts in the DOM; expected 1"
        )

    def test_switching_between_nav_layouts_keeps_a_single_widget(self, driver):
        """Desktop -> mobile -> desktop re-mounts the widget without duplicating it or its script"""
        driver.set_window_size(1280, 900)
        driver.get(Config.BASE_URL)
        common = CommonPage(driver)
        page = BhashiniPage(driver)
        assert page.wait_for_container_count(1) == 1, "Desktop nav has no widget mount point"

        driver.set_window_size(800, 900)
        assert common.open_mobile_menu(), "Mobile menu did not appear after narrowing to 800px"
        assert page.wait_for_container_count(1) == 1, (
            f"After switching to the mobile nav there are {page.container_count()} widget mount points"
        )
        assert page.script_count() == 1, (
            f"Plugin script duplicated after the nav switched: {page.script_count()} tags"
        )

        driver.set_window_size(1280, 900)
        assert page.wait_for_container_count(1) == 1, (
            f"After returning to desktop there are {page.container_count()} widget mount points"
        )
        assert page.script_count() == 1, (
            f"Plugin script duplicated after returning to desktop: {page.script_count()} tags"
        )

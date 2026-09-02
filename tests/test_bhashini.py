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
from pages.bhashini_page import BhashiniPage


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

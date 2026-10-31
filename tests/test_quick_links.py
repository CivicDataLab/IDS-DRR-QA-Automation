"""
Home page analytics quick-links carousel - coverage for merged frontend PR #534.

#534 wrapped the carousel track in a `min-w-0 flex-1` box between the two arrow
buttons (and dropped `justify-center` from the flex row). Before it, the track
could size itself to its cards and run underneath the arrows, so the first and
last cards were partly covered. The existing home-page tests only check that a
state link exists and that the Next arrow can be clicked, so none of them see
overlap.

Run:
    pytest tests/test_quick_links.py -v
"""

import pytest

from config.config import Config
from pages.home_page import HomePage

VIEWPORTS = [("desktop", 1280, 900), ("mobile", 375, 800)]


@pytest.mark.flow
class TestQuickLinksCarouselLayout:
    """The state-card track sits between the arrows and the arrows stay on screen."""

    @pytest.mark.parametrize("label,width,height", VIEWPORTS)
    def test_track_sits_between_the_arrows(self, driver, label, width, height):
        """The visible card track does not run under either arrow button"""
        driver.set_window_size(width, height)
        driver.get(Config.BASE_URL)  # re-render at this width
        geometry = HomePage(driver).quick_links_geometry()

        prev_right = geometry["prev"][1]
        next_left = geometry["next"][0]
        track_left, track_right = geometry["viewport"]

        assert track_left >= prev_right - 0.5, (
            f"{label}: card track starts at {track_left}px, under the Previous arrow "
            f"(which ends at {prev_right}px)"
        )
        assert track_right <= next_left + 0.5, (
            f"{label}: card track ends at {track_right}px, under the Next arrow "
            f"(which starts at {next_left}px)"
        )
        assert geometry["prev"][0] >= 0 and geometry["next"][1] <= width, (
            f"{label}: an arrow is pushed outside the {width}px viewport: "
            f"prev={geometry['prev']}, next={geometry['next']}"
        )

    def test_next_arrow_advances_the_cards(self, driver):
        """On desktop, with more state cards than fit, Next scrolls the track"""
        driver.set_window_size(1280, 900)
        driver.get(Config.BASE_URL)
        home = HomePage(driver)
        home.quick_links_geometry()  # wait for render

        if not home.quick_links_next_enabled():
            pytest.skip(
                f"all {home.quick_links_slide_count()} state cards already fit at 1280px; nothing to scroll"
            )
        assert home.click_quick_links_next(), (
            "Next arrow is enabled but clicking it did not move the card track"
        )

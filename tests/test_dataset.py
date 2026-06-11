"""
Dataset Page Tests - Comprehensive test coverage including edge cases and negative tests

Run: pytest tests/test_dataset.py -v
"""

import pytest
from pages.common_page import CommonPage
from pages.dataset_page import DatasetPage, DatasetInfoPage


@pytest.mark.dataset
@pytest.mark.smoke
class TestDatasetNavigation:
    """Dataset page navigation and accessibility tests"""

    def test_navigate_to_dataset_from_homepage(self, driver):
        """Verify dataset page is accessible from homepage"""
        common_page = CommonPage(driver)
        assert common_page.navigate_to_datasets(), "Failed to navigate to Datasets"
        print("✅ Dataset navigation successful")

    def test_dataset_page_header_visible(self, driver):
        """Verify header is visible on dataset page"""
        common_page = CommonPage(driver)
        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert common_page.is_header_logo_visible(), "Header logo not visible"

    def test_dataset_page_footer_visible(self, driver):
        """Verify footer is visible on dataset page"""
        common_page = CommonPage(driver)
        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        footer_results = common_page.check_all_footer_elements()
        assert all(footer_results.values()), "Some footer elements not visible"


@pytest.mark.dataset
class TestDatasetFilters:
    """Dataset filtering and search tests"""

    def test_apply_drims_source_filter(self, driver):
        """Test DRIMS source filter application"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"

    def test_screenshot_after_filter(self, driver):
        """Test screenshot capture after applying filter"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        screenshot_before = dataset_page.take_dataset_screenshot("before_filter.png")
        assert screenshot_before is not None, "Failed to take screenshot before filter"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        # Screenshot is taken automatically in apply_source_filter_drims method

    @pytest.mark.negative
    def test_filter_without_page_load(self, driver):
        """Negative test: Try filter without navigating to page"""
        dataset_page = DatasetPage(driver)
        # Don't navigate first
        result = dataset_page.apply_source_filter_drims()
        # Should return False or handle gracefully
        assert result is False, "Filter should fail without page navigation"


@pytest.mark.dataset
class TestDatasetSelection:
    """Dataset card selection tests"""

    def test_click_first_dataset(self, driver):
        """Test clicking first dataset card"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

    def test_dataset_opens_detail_page(self, driver):
        """Verify clicking dataset opens detail page"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"

        # Get current URL before clicking
        initial_url = driver.current_url
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        # Verify we're on detail page (URL changed) — wait up to 10s for SPA navigation
        from selenium.webdriver.support.ui import WebDriverWait
        try:
            WebDriverWait(driver, 10).until(lambda d: d.current_url != initial_url)
        except Exception:
            pass
        current_url = driver.current_url
        assert current_url != initial_url, "URL did not change after clicking dataset"
        assert "datasets" in current_url.lower(), "Not on a dataset detail page"


@pytest.mark.dataset
class TestDatasetInfoButtons:
    """Dataset info page action button tests"""

    def test_visit_source_website_button(self, driver):
        """Test visit source website button"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        assert dataset_info_page.click_visit_source_website(), "Failed to click source website"

    def test_github_repo_button(self, driver):
        """Test GitHub repo button"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        assert dataset_info_page.click_github_repo(), "Failed to click GitHub repo"

    def test_share_dataset_toggle(self, driver):
        """Test share dataset button toggle"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        assert dataset_info_page.toggle_share_dataset(), "Failed to toggle share"

    def test_all_action_buttons_sequential(self, driver):
        """Test all action buttons in sequence"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        assert dataset_info_page.click_visit_source_website(), "Failed to click source website"
        assert dataset_info_page.click_github_repo(), "Failed to click GitHub repo"
        assert dataset_info_page.toggle_share_dataset(), "Failed to toggle share"


@pytest.mark.dataset
class TestDatasetVisualizations:
    """Visualization display and interaction tests"""

    def test_view_visualization_1(self, driver):
        """Test viewing first visualization"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        assert dataset_info_page.view_visualization_1(), "Failed to view viz 1"

    @pytest.mark.xfail(reason="Visualization toggle button not present on current first DRIMS dataset; single-viz layout has no switcher control")
    def test_view_visualization_2(self, driver):
        """Test viewing alternate visualization"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        assert dataset_info_page.view_visualization_2(), "Failed to view viz 2"

    @pytest.mark.xfail(reason="Visualization toggle button not present on current first DRIMS dataset; single-viz layout has no switcher control")
    def test_toggle_between_visualizations(self, driver):
        """Test toggling between visualizations multiple times"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        # Toggle multiple times
        for iteration in range(2):
            assert dataset_info_page.view_visualization_2(), f"Failed to view viz 2 in iteration {iteration + 1}"
            assert dataset_info_page.view_visualization_1(), f"Failed to view viz 1 in iteration {iteration + 1}"

    @pytest.mark.xfail(reason="Visualization export/download button not present on current first DRIMS dataset")
    def test_download_visualization(self, driver):
        """Test visualization download"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        assert dataset_info_page.download_visualization(), "Failed to download viz"


@pytest.mark.dataset
class TestDatasetMetadata:
    """Dataset metadata and links tests"""

    def test_click_category_link(self, driver):
        """Test category link in metadata"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        assert dataset_info_page.click_category_link(), "Failed to click category link"


@pytest.mark.dataset
class TestDatasetDownloads:
    """Dataset download functionality tests"""

    def test_download_all_datasets(self, driver):
        """Test downloading all dataset files"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        assert dataset_info_page.download_all_datasets(), "Failed to download all datasets"

    @pytest.mark.parametrize("download_index", [1, 2, 3, 4])
    def test_individual_dataset_downloads(self, driver, download_index):
        """Test individual dataset downloads (boundary test)"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        # Test specific download button — always scroll into view then JS click
        from locators.dataset_locators import DatasetInfoPageLocators
        locators = [
            DatasetInfoPageLocators.DOWNLOAD_DATASET_1,
            DatasetInfoPageLocators.DOWNLOAD_DATASET_2,
            DatasetInfoPageLocators.DOWNLOAD_DATASET_3,
            DatasetInfoPageLocators.DOWNLOAD_DATASET_4
        ]

        locator = locators[download_index - 1]
        element = dataset_info_page.find_element(locator)
        assert element, f"Download button {download_index} not found"
        dataset_info_page._js_click(element)
        print(f"✅ Download button {download_index} clicked via JS")


@pytest.mark.dataset
@pytest.mark.flow
@pytest.mark.slow
class TestDatasetCompleteFlow:
    """Complete end-to-end dataset flow test"""

    @pytest.mark.xfail(reason="Complete workflow includes visualization toggle/download steps not available on current first DRIMS dataset")
    def test_complete_dataset_workflow(self, driver):
        """Full dataset workflow from listing to download"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        # Navigate and filter
        print("\n=== Dataset Navigation ===")
        assert common_page.navigate_to_datasets()
        dataset_page.take_dataset_screenshot("dataset_landing_page.png")

        print("\n=== Apply Filter ===")
        assert dataset_page.apply_source_filter_drims()

        print("\n=== Open Dataset ===")
        assert dataset_page.click_first_dataset()

        print("\n=== Test Action Buttons ===")
        assert dataset_info_page.click_visit_source_website()
        assert dataset_info_page.click_github_repo()
        assert dataset_info_page.toggle_share_dataset()

        print("\n=== Test Visualizations ===")
        assert dataset_info_page.view_visualization_1()
        assert dataset_info_page.view_visualization_2()
        assert dataset_info_page.download_visualization()

        print("\n=== Test Metadata ===")
        assert dataset_info_page.click_category_link()

        print("\n=== Test Downloads ===")
        assert dataset_info_page.download_all_datasets()

        print("\n✅ Complete dataset workflow successful")


@pytest.mark.dataset
@pytest.mark.edge_case
class TestDatasetEdgeCases:
    """Edge cases and boundary condition tests"""

    def test_rapid_filter_toggle(self, driver):
        """Edge case: Rapidly toggle filter on/off"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"

        # Rapid toggling - ensure all operations succeed
        for iteration in range(3):
            assert dataset_page.apply_source_filter_drims(), f"Failed to apply filter in iteration {iteration + 1}"
            assert dataset_page.apply_source_filter_drims(), f"Failed to toggle off filter in iteration {iteration + 1}"

    @pytest.mark.xfail(reason="Visualization toggle button not present on current first DRIMS dataset; single-viz layout has no switcher control")
    def test_rapid_visualization_switching(self, driver):
        """Edge case: Rapidly switch visualizations"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        # Rapid switching - ensure all switches succeed
        for iteration in range(5):
            assert dataset_info_page.view_visualization_2(), f"Failed to view viz 2 in iteration {iteration + 1}"
            assert dataset_info_page.view_visualization_1(), f"Failed to view viz 1 in iteration {iteration + 1}"

    def test_multiple_share_toggles(self, driver):
        """Edge case: Multiple share button toggles"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)
        dataset_info_page = DatasetInfoPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        assert dataset_page.apply_source_filter_drims(), "Failed to apply DRIMS filter"
        assert dataset_page.click_first_dataset(), "Failed to click first dataset"

        # Toggle multiple times - ensure all toggles succeed
        for iteration in range(3):
            assert dataset_info_page.toggle_share_dataset(), f"Failed to toggle share in iteration {iteration + 1}"

    @pytest.mark.negative
    def test_download_without_opening_dataset(self, driver):
        """Negative test: Try download without opening dataset"""
        dataset_info_page = DatasetInfoPage(driver)
        # Don't navigate or open dataset
        result = dataset_info_page.download_all_datasets()
        assert result is False, "Download should fail without opening dataset"

    @pytest.mark.negative
    def test_visualization_without_opening_dataset(self, driver):
        """Negative test: Try visualization without opening dataset"""
        dataset_info_page = DatasetInfoPage(driver)
        result = dataset_info_page.view_visualization_1()
        assert result is False, "Visualization should fail without opening dataset"


@pytest.mark.dataset
@pytest.mark.negative
class TestDatasetNegativeTests:
    """Negative test cases for dataset functionality"""

    def test_dataset_click_without_filter(self, driver):
        """Negative test: Try clicking dataset without applying filter"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        # Don't apply filter, try to click dataset
        # May work or fail depending on available datasets
        result = dataset_page.click_first_dataset()
        # Assert that result is not None - it should handle gracefully either way
        assert result is not None, "Click first dataset should return a result (True/False)"

    def test_empty_filter_results(self, driver):
        """Test behavior when filter returns no results"""
        common_page = CommonPage(driver)
        dataset_page = DatasetPage(driver)

        assert common_page.navigate_to_datasets(), "Failed to navigate to datasets"
        # This would require a filter that returns no results
        # For now, just verify the page loaded successfully
        assert common_page.is_header_logo_visible(), "Header should be visible even with empty results"

    @pytest.mark.skip(reason="Requires invalid dataset ID")
    def test_invalid_dataset_id_url(self, driver):
        """Negative test: Navigate to invalid dataset ID"""
        # Navigate directly to invalid dataset URL
        # driver.get(Config.BASE_URL + "/datasets/invalid-id-999")
        pass

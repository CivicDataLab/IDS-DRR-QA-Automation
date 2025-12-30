from pages.base_page import BasePage
from locators.dataset_locators import DatasetPageLocators, DatasetInfoPageLocators
from config.config import Config


class DatasetPage(BasePage):
    """Page Object for Dataset listing page"""

    def __init__(self, driver):
        super().__init__(driver)
        self.screenshot_dir = Config.DATASETS_SCREENSHOTS_DIR

    def apply_source_filter_drims(self):
        """Apply DRIMS source filter"""
        return self.click_and_screenshot(
            DatasetPageLocators.SOURCE_FILTER_DRIMS,
            "DRIMS Filter",
            "source_filter_applied.png",
            self.screenshot_dir
        )

    def click_first_dataset(self):
        """Click on the first dataset in the listing"""
        return self.click_and_screenshot(
            DatasetPageLocators.FIRST_DATASET_CARD,
            "First Dataset",
            "drims_dataset_info.png",
            self.screenshot_dir
        )

    def take_dataset_screenshot(self, filename):
        """Take screenshot in datasets directory"""
        return self.take_screenshot(filename, self.screenshot_dir)


class DatasetInfoPage(BasePage):
    """Page Object for Dataset info/detail page"""

    def __init__(self, driver):
        super().__init__(driver)
        self.screenshot_dir = Config.DATASETS_SCREENSHOTS_DIR

    def click_visit_source_website(self):
        """Click Visit Source Website button"""
        success = self.click(DatasetInfoPageLocators.VISIT_SOURCE_WEBSITE, "Visit Source Website")
        if success:
            self.dismiss_alert()
            self.take_screenshot("source_website_click.png", self.screenshot_dir)
        return success

    def click_github_repo(self):
        """Click GitHub Repo button"""
        success = self.click(DatasetInfoPageLocators.GITHUB_REPO, "GitHub Repo")
        if success:
            self.dismiss_alert()
            self.take_screenshot("github_repo_button_click.png", self.screenshot_dir)
        return success

    def toggle_share_dataset(self):
        """Toggle share dataset button"""
        success = self.click(DatasetInfoPageLocators.SHARE_DATASET, "Share Dataset")
        if success:
            self.take_screenshot("share_dataset_button.png", self.screenshot_dir)
            # Click again to close
            self.click(DatasetInfoPageLocators.SHARE_DATASET, "Share Dataset (close)")
        return success

    def view_visualization_1(self):
        """Scroll to and view first visualization"""
        element = self.find_element(DatasetInfoPageLocators.VISUALIZATION_1)
        if element:
            self.scroll_to_element(DatasetInfoPageLocators.VISUALIZATION_1)
            self.take_screenshot("demographic_damages_visualization.png", self.screenshot_dir)
            print("✅ Visualization 1 found and screenshot taken")
            return True
        else:
            print("❌ Visualization 1 not found")
            return False

    def view_visualization_2(self):
        """View alternate visualization"""
        success = self.click(DatasetInfoPageLocators.VISUALIZATION_2_BUTTON, "Visualization 2")
        if success:
            self.take_screenshot("infra_damage_visualization.png", self.screenshot_dir)
            # Go back to first visualization
            self.click(DatasetInfoPageLocators.VISUALIZATION_2_BACK_BUTTON, "Back to Visualization 1")
        return success

    def download_visualization(self):
        """Click visualization download button"""
        return self.click(DatasetInfoPageLocators.VISUALIZATION_DOWNLOAD, "Visualization Download")

    def click_category_link(self):
        """Click category link in metadata"""
        success = self.click(DatasetInfoPageLocators.CATEGORY_LINK, "Category Link")
        if success:
            self.scroll_to_element(DatasetInfoPageLocators.CATEGORY_LINK)
            self.take_screenshot("category_link_dataset_info.png", self.screenshot_dir)
        return success

    def download_all_datasets(self):
        """Download all available dataset files"""
        download_buttons = [
            (DatasetInfoPageLocators.DOWNLOAD_DATASET_1, False),
            (DatasetInfoPageLocators.DOWNLOAD_DATASET_2, False),
            (DatasetInfoPageLocators.DOWNLOAD_DATASET_3, True),  # Need scroll
            (DatasetInfoPageLocators.DOWNLOAD_DATASET_4, False)
        ]

        success_count = 0
        for idx, (locator, needs_scroll) in enumerate(download_buttons, 1):
            if needs_scroll:
                self.scroll_to_element(locator)

            if self.click(locator, f"Download Dataset {idx}"):
                success_count += 1

        print(f"✅ Downloaded {success_count}/{len(download_buttons)} datasets")
        return success_count == len(download_buttons)

    def take_dataset_screenshot(self, filename):
        """Take screenshot in datasets directory"""
        return self.take_screenshot(filename, self.screenshot_dir)

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
        # Guard: check the filter element exists (no self-healing) to confirm we're on the right page.
        # Self-healing relaxed XPath can match arbitrary buttons on wrong pages, so skip it here.
        if not self.find_element(DatasetPageLocators.SOURCE_FILTER_DRIMS, use_healing=False):
            print("❌ Source filter element not found — not on datasets listing page")
            return False
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
        """Toggle share dataset button (open then close)."""
        self.scroll_to_element(DatasetInfoPageLocators.SHARE_DATASET)
        success = self.click(DatasetInfoPageLocators.SHARE_DATASET, "Share Dataset")
        if success:
            self.take_screenshot("share_dataset_button.png", self.screenshot_dir)
            # Wait for the panel animation to settle before closing
            self.find_clickable_element(DatasetInfoPageLocators.SHARE_DATASET, timeout=5)
            self.click(DatasetInfoPageLocators.SHARE_DATASET, "Share Dataset (close)")
        return success

    def view_visualization_1(self):
        """Scroll to and view first visualization"""
        if "/dataset" not in self.driver.current_url.lower():
            print("❌ Not on a dataset info page — cannot view visualization")
            return False
        element = self.find_element(DatasetInfoPageLocators.VISUALIZATION_1)
        if element:
            self.scroll_to_element(DatasetInfoPageLocators.VISUALIZATION_1)
            self.take_screenshot("demographic_damages_visualization.png", self.screenshot_dir)
            print("✅ Visualization 1 found and screenshot taken")
            return True
        else:
            print("❌ Visualization 1 not found")
            return False

    def _js_click(self, element):
        """Click element via JavaScript to bypass interactability issues (off-screen, overlapping)."""
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

    def view_visualization_2(self):
        """View alternate visualization and return to visualization 1."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Scroll to the visualization widget before interacting
        self.scroll_to_element(DatasetInfoPageLocators.VISUALIZATION_1)

        success = self.click(DatasetInfoPageLocators.VISUALIZATION_2_BUTTON, "Visualization 2")
        if success:
            self.take_screenshot("infra_damage_visualization.png", self.screenshot_dir)
            # Wait briefly for the viz to render before clicking back
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(DatasetInfoPageLocators.VISUALIZATION_2_BACK_BUTTON)
                )
            except Exception:
                pass
            self.click(DatasetInfoPageLocators.VISUALIZATION_2_BACK_BUTTON, "Back to Visualization 1")
        return success

    def download_visualization(self):
        """Click visualization download button"""
        self.scroll_to_element(DatasetInfoPageLocators.VISUALIZATION_DOWNLOAD)
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
        if "/dataset" not in self.driver.current_url.lower():
            print("❌ Not on a dataset info page — cannot download datasets")
            return False
        download_buttons = [
            DatasetInfoPageLocators.DOWNLOAD_DATASET_1,
            DatasetInfoPageLocators.DOWNLOAD_DATASET_2,
            DatasetInfoPageLocators.DOWNLOAD_DATASET_3,
            DatasetInfoPageLocators.DOWNLOAD_DATASET_4,
        ]

        success_count = 0
        for idx, locator in enumerate(download_buttons, 1):
            # Always scroll each button into view before clicking (some may be off-screen)
            element = self.find_element(locator)
            if element:
                try:
                    self._js_click(element)
                    print(f"✅ Download Dataset {idx} clicked successfully")
                    success_count += 1
                except Exception as e:
                    print(f"❌ Download Dataset {idx} JS click failed: {e}")
                    # Fallback: regular click via base_page
                    if self.click(locator, f"Download Dataset {idx}"):
                        success_count += 1
            else:
                print(f"❌ Download Dataset {idx} element not found")

        print(f"✅ Downloaded {success_count}/{len(download_buttons)} datasets")
        return success_count == len(download_buttons)

    def take_dataset_screenshot(self, filename):
        """Take screenshot in datasets directory"""
        return self.take_screenshot(filename, self.screenshot_dir)

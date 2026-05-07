from pages.base_page import BasePage
from locators.common_locators import HeaderLocators, FooterLocators


class CommonPage(BasePage):
    """Page Object for common elements (header, footer) across all pages"""

    def __init__(self, driver):
        super().__init__(driver)

    # Navigation Methods
    def navigate_to_home(self):
        """Navigate to Home page"""
        return self.click(HeaderLocators.HOME_LINK, "Home Link")

    def navigate_to_analytics(self):
        """Navigate to Analytics page"""
        # Try primary locator first, fall back to alternative
        if not self.click(HeaderLocators.ANALYTICS_LINK, "Analytics Link"):
            return self.click(HeaderLocators.ANALYTICS_LINK_ALT, "Analytics Link (Alt)")
        return True

    def navigate_to_datasets(self):
        """Navigate to Datasets page"""
        # Try primary locator first, fall back to alternative
        if not self.click(HeaderLocators.DATASETS_LINK, "Datasets Link"):
            return self.click(HeaderLocators.DATASETS_LINK_ALT, "Datasets Link (Alt)")
        return True

    def navigate_to_about_us(self):
        """Navigate to About Us page"""
        return self.click(HeaderLocators.ABOUT_US_LINK, "About Us Link")

    # Header Visibility Checks
    def is_header_logo_visible(self):
        """Check if header logo is visible"""
        return self.is_element_visible(HeaderLocators.HEADER_LOGO, "Header Logo")

    def is_language_dropdown_visible(self):
        """Check if language dropdown is visible"""
        # Use shorter timeout since language dropdown may not be present on all pages
        return self.is_element_visible(HeaderLocators.LANGUAGE_DROPDOWN, "Language Dropdown", timeout=3)

    def is_nav_link_visible(self, link_name):
        """
        Check if a navigation link is visible

        Args:
            link_name: 'home', 'analytics', 'datasets', or 'about_us'

        Returns:
            bool: Visibility status
        """
        locator_map = {
            'home': HeaderLocators.HOME_LINK,
            'analytics': HeaderLocators.ANALYTICS_LINK,
            'datasets': HeaderLocators.DATASETS_LINK,
            'about_us': HeaderLocators.ABOUT_US_LINK
        }

        if link_name.lower() not in locator_map:
            print(f"❌ Unknown link name: {link_name}")
            return False

        return self.is_element_visible(
            locator_map[link_name.lower()],
            f"{link_name.title()} Link"
        )

    # Footer Visibility Checks
    def is_footer_logo_visible(self, logo_name):
        """
        Check if a footer logo is visible

        Args:
            logo_name: 'ids_drr', 'cdl', or 'ocp'

        Returns:
            bool: Visibility status
        """
        logo_map = {
            'ids_drr': FooterLocators.IDS_DRR_LOGO,
            'cdl': FooterLocators.CDL_LOGO,
            'ocp': FooterLocators.OCP_LOGO
        }

        if logo_name.lower() not in logo_map:
            print(f"❌ Unknown logo name: {logo_name}")
            return False

        return self.is_element_visible(
            logo_map[logo_name.lower()],
            f"{logo_name.upper()} Logo"
        )

    def is_partner_logo_visible(self, partner_name):
        """
        Check if a partner logo is visible

        Args:
            partner_name: 'rockefeller', 'pjmf', 'asdma', or 'hpsdma'

        Returns:
            bool: Visibility status
        """
        partner_map = {
            'rockefeller': FooterLocators.ROCKEFELLER_LOGO,
            'pjmf': FooterLocators.PJMF_LOGO,
            'asdma': FooterLocators.ASDMA_LOGO,
            'hpsdma': FooterLocators.HPSDMA_LOGO
        }

        if partner_name.lower() not in partner_map:
            print(f"❌ Unknown partner name: {partner_name}")
            return False

        return self.is_element_visible(
            partner_map[partner_name.lower()],
            f"{partner_name.title()} Logo"
        )

    def check_all_header_elements(self, include_language_dropdown=False):
        """
        Check visibility of all header elements

        Args:
            include_language_dropdown: Whether to include language dropdown in check (default: False)

        Returns:
            dict: Results of all checks
        """
        results = {
            'header_logo': self.is_header_logo_visible(),
            'home_link': self.is_nav_link_visible('home'),
            'analytics_link': self.is_nav_link_visible('analytics'),
            'datasets_link': self.is_nav_link_visible('datasets'),
            'about_us_link': self.is_nav_link_visible('about_us')
        }

        # Language dropdown is optional - may be hidden in some UI implementations
        if include_language_dropdown:
            results['language_dropdown'] = self.is_language_dropdown_visible()

        passed = sum(results.values())
        total = len(results)
        print(f"\nHeader Check Summary: {passed}/{total} elements visible")

        return results

    def check_all_footer_elements(self):
        """
        Check visibility of all footer elements

        Returns:
            dict: Results of all checks
        """
        results = {
            'ids_drr_logo': self.is_footer_logo_visible('ids_drr'),
            'cdl_logo': self.is_footer_logo_visible('cdl'),
            'ocp_logo': self.is_footer_logo_visible('ocp'),
            'rockefeller_logo': self.is_partner_logo_visible('rockefeller'),
            'pjmf_logo': self.is_partner_logo_visible('pjmf'),
            'asdma_logo': self.is_partner_logo_visible('asdma'),
            'hpsdma_logo': self.is_partner_logo_visible('hpsdma')
        }

        passed = sum(results.values())
        total = len(results)
        print(f"\nFooter Check Summary: {passed}/{total} elements visible")

        return results

    def check_analytics_footer_elements(self):
        """
        Check visibility of analytics page footer elements
        Analytics page footer only contains: IDS-DRR, CDL, and OCP logos
        (Partner logos are not displayed on analytics page)

        Returns:
            dict: Results of all checks
        """
        results = {
            'ids_drr_logo': self.is_footer_logo_visible('ids_drr'),
            'cdl_logo': self.is_footer_logo_visible('cdl'),
            'ocp_logo': self.is_footer_logo_visible('ocp')
        }

        passed = sum(results.values())
        total = len(results)
        print(f"\nAnalytics Footer Check Summary: {passed}/{total} logos visible")

        return results

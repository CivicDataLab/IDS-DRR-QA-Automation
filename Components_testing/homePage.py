from load_driver import load_driver
import homepage_component_visibility_test
import analytics_visibility_test
import dataset_page_visibility_test
import dataset_info_visibility_test
import about_us_visibility_test

if __name__ == '__main__':
    # Load driver
    driver = load_driver()
    # homepage_component_visibility_test.homepage_component_visibility_test(driver)
    # analytics_visibility_test.analytics_visibility_test(driver)
    # dataset_page_visibility_test.dataset_page_visibility_test(driver)
    # dataset_info_visibility_test.dataset_info_visibility_test(driver)
    about_us_visibility_test.about_us_visibility_test(driver)
    driver.quit()



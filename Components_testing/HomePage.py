from load_driver import load_driver
import homepage_component_visibility_test
import analytics_visibility_test

if __name__ == '__main__':
    # Load driver
    driver = load_driver()
    homepage_component_visibility_test.homepage_component_visibility_test(driver)
    analytics_visibility_test.analytics_visibility_test(driver)


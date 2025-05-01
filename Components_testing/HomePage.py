from load_driver import load_driver
import component_visibility_test

if __name__ == '__main__':
    # Load driver
    driver = load_driver()
    component_visibility_test.component_visibility_test(driver)



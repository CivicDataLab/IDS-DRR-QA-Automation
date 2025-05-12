from load_driver import load_driver
import consumer_analytics_flow
import consumer_dataset_flow


if __name__ == '__main__':
    # Load driver
    driver = load_driver()
    consumer_analytics_flow.consumer_analytics_flow_test(driver)
    # driver.quit()



import my_lib
def test_dropdown_with_values(driver, locator_type, locator_value, values_to_test,
                              screenshot_prefix=None, wait_before=1, wait_after=3,
                              description="Dropdown"):
    """
    Parameters:
        driver: Selenium WebDriver instance
        locator_type: By.ID, By.CSS_SELECTOR, By.XPATH, etc.
        locator_value: The value of the locator (e.g., "myDropdown" for ID)
        values_to_test: List of values to select in the dropdown
        screenshot_prefix: Prefix for screenshot filenames (will be appended with value)
        wait_before: Time to wait before each selection in seconds
        wait_after: Time to wait after each selection in seconds
        description: Description of the dropdown for logging purposes

    Returns:
        Dictionary with results for each value {value: success_status}
    """
    results = {}

    try:
        # Find the dropdown element once
        dropdown_element = driver.find_element(locator_type, locator_value)
        print(f"Found {description} element")

        # Test each value
        for value in values_to_test:
            try:
                my_lib.time.sleep(wait_before)

                # Set the value using JavaScript
                driver.execute_script(f"arguments[0].value='{value}';", dropdown_element)

                # Trigger change event with bubbling
                driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                                      dropdown_element)

                print(f"Selected option '{value}' in {description}")
                time.sleep(wait_after)

                # Take a screenshot if requested
                if screenshot_prefix:
                    # Create a safe filename
                    safe_value = str(value).replace('/', '_').replace('\\', '_').replace(':', '_')
                    screenshot_filename = f"{screenshot_prefix}_{safe_value}.png"
                    driver.save_screenshot(screenshot_filename)
                    print(f"Screenshot saved as {screenshot_filename}")

                results[value] = True

            except Exception as e:
                print(f"Failed to select option '{value}' in {description}: {e}")
                results[value] = False

    except Exception as e:
        print(f"Failed to locate {description} element: {e}")
        for value in values_to_test:
            results[value] = False

    # Print summary
    print(f"\n{description} Test Summary:")
    print(f"Element: {locator_type}='{locator_value}'")
    for value, success in results.items():
        print(f"  Value '{value}': {'✓ Success' if success else '✗ Failed'}")

    return results
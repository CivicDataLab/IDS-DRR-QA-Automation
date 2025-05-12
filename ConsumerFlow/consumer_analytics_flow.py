import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

map_district_values = []
chart_district_values = []
table_district_values = []
exceptions = []
screenshot_dir = './screenshots/analytics'
ss_prefix = ""
district_select = ""
revenue_circle_select = ""
calendar = ""

def consumer_analytics_flow_test(driver):

    # Create the directory if it doesn't exist
    global ss_prefix, district_select, revenue_circle_select, calendar
    os.makedirs(screenshot_dir, exist_ok=True)
    # moving to analytics page from homepage
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[2]/div/span"))
        )
        driver.find_element(By.XPATH, "/html/body/main/header/div/div[2]/div[1]/a[2]/div/span").click()
        print("✅ Analytics button clicked")
    except:
        print("❌ Analytics button not found")
        return
    # iterating for map, chart and table view
    for index in range(2, 4):
        time.sleep(3)
        xpath = f"/html/body/main/div/main/div/div[1]/button[{index}]/span"
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.find_element(By.XPATH, xpath).click()
        if index == 1:
            ss_prefix = "map_"
            district_select = "Sivasagar"
            revenue_circle_select = "Sibsagar"
            calendar = "7"
        elif index == 2:
            ss_prefix = "chart_"
            district_select = "Cachar"
            revenue_circle_select = "Sonai"
            calendar = "8"
        elif index == 3:
            ss_prefix = "table_"
            district_select = "South salmara mancachar"
            revenue_circle_select = "Mankachar"
            calendar = "9"

        # click on the district-select dropdown.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.NAME, "district-select"))
            )
        except:
            print("district-select dropdown found - Failed")
            exceptions.append(
                {"Exception": "district-select dropdown found - Failed",
                 }
            )
        else:
            time.sleep(4)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}analytics_page.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

            select_element = driver.find_element(By.NAME, "district-select")
            driver.find_element(By.NAME, "district-select").click()
            print("district-select dropdown click - Passed")
            select = Select(select_element)
            select.select_by_visible_text(f"{district_select}")
            time.sleep(4)

            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}_{district_select}_district.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)
            print(f"{district_select} district selected")

        # click on the revenue-select dropdown.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.NAME, "revenue-circle-select"))
            )
        except:
            print("revenue-circle-select dropdown found - Failed")
            exceptions.append(
                {"Exception": "revenue-circle-select dropdown found - Failed",
                 }
            )
        else:
            # time.sleep(2)
            select_element = driver.find_element(By.NAME, "revenue-circle-select")
            driver.find_element(By.NAME, "revenue-circle-select").click()
            print("revenue-circle-select dropdown click - Passed")
            select = Select(select_element)
            select.select_by_visible_text(f"{revenue_circle_select}")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}_{district_select}_{revenue_circle_select}.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)
            print("Sibsagar revenue circle selected selected")


        # click on the Calendar button dropdown.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@aria-label='Calendar']"))
            )
        except:
            print("calendar button found - Failed")
            exceptions.append(
                {"Exception": "calendar button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "//button[@aria-label='Calendar']").click()
            print("calendar button click - Passed")
            time.sleep(2)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}show_calendar.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)
            driver.find_element(By.XPATH, f"//button[@value='{calendar}']").click()
            print(f"{calendar} Month selected")
            time.sleep(4)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}{district_select}_{revenue_circle_select}_{calendar}_2024.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the expand Hazard options button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]")))
        except:
            print("Expand Hazard options button found - Failed")
            exceptions.append(
                {"Exception": "Expand Hazard options button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]").click()
            print("Expand Hazard options button click - Passed")
            time.sleep(2)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}hazard_show_options.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)


        # click on the Total Monthly rainfall button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/span/div/label/span"))
            )
        except:
            print("Total Monthly rainfall button found - Failed")
            exceptions.append(
                {"Exception": "Total Monthly rainfall button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/span/div/label/span").click()
            print("Total Monthly rainfall button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}hazard_monthly_rainfall.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)



        # click on the Sum of inundation intensities button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/span/div/label/span"))
            )
        except:
            print("Sum of inundation intensities button found - Failed")
            exceptions.append(
                {"Exception": "Sum of inundation intensities button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/span/div/label/span").click()
            print("Sum of inundation intensities button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}hazard_sum_inundation_ratio.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Mean elevation button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div/span/div/label/span"))
            )
        except:
            print("Mean elevation button found - Failed")
            exceptions.append(
                {"Exception": "Mean elevation button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div/span/div/label/span").click()
            print("Mean elevation button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}hazard_mean_elevation.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the collapse Hazard options button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]")))
        except:
            print("Collapse Hazard options button found - Failed")
            exceptions.append(
                {"Exception": "Collapse Hazard options button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]").click()
            print("Collapse Hazard options button click - Passed")
            time.sleep(2)

        # click on the expand Exposure options button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div/div/div/div[1]"))
            )
        except:
            print("Expand Exposure options button found - Failed")
            exceptions.append(
                {"Exception": "Expand Exposure options button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div/div/div/div[1]").click()
            print("Expand Exposure options button click - Passed")
            time.sleep(2)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}exposure_show_options.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)


        # click on the Total Number of households button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div/span/div/label/span"))
            )
        except:
            print("Total Number of households button found - Failed")
            exceptions.append(
                {"Exception": "Total Number of households button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div/span/div/label/span").click()
            print("Total Number of households button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}exposure_total_households.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)


        # click on the Population button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/span/div/label/span"))
            )
        except:
            print("Population button found - Failed")
            exceptions.append(
                {"Exception": "Population button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/span/div/label/span").click()
            print("Population button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}exposure_population.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Elderly population button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[3]/div/span/div/label/span"))
            )
        except:
            print("Elderly population button found - Failed")
            exceptions.append(
                {"Exception": "Elderly population button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[3]/div/span/div/label/span").click()
            print("Elderly population button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}exposure_elderly_population.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Children population button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[4]/div/span/div/label/span"))
            )
        except:
            print("Children population button found - Failed")
            exceptions.append(
                {"Exception": "Children population button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[4]/div/span/div/label/span").click()
            print("Children population button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}exposure_children_population.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Collapse Exposure options button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div/div/div/div[1]"))
            )
        except:
            print("Collapse Exposure options button found - Failed")
            exceptions.append(
                {"Exception": "Collapse Exposure options button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[2]/div/div/div/div[1]").click()
            print("Collapse Exposure options button click - Passed")
            time.sleep(2)

        # click on the expand Vulnerability options button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div/div/div/div[1]"))
            )
        except:
            print("Expand Vulnerability options button found - Failed")
            exceptions.append(
                {"Exception": "Expand Vulnerability options button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div/div/div/div[1]").click()
            print("Expand Vulnerability options button click - Passed")
            time.sleep(2)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_show_options.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)


        # click on the Health centres number button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/span/div/label/span"))
            )
        except:
            print("Health centres number button found - Failed")
            exceptions.append(
                {"Exception": "Health centres number button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/span/div/label/span").click()
            print("Health centres number button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_health_centre.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)


        # click on the domestic electricity button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[2]/div/span/div/label/span"))
            )
        except:
            print("domestic electricity button found - Failed")
            exceptions.append(
                {"Exception": "domestic electricity button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[2]/div/span/div/label/span").click()
            print("domestic electricity button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_domestic_electricity.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Piped water connection button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[3]/div/span/div/label/span"))
            )
        except:
            print("Piped water connection button found - Failed")
            exceptions.append(
                {"Exception": "Piped water connection button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[3]/div/span/div/label/span").click()
            print("Piped water connection button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_piped_water.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Households without sanitation button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[4]/div/span/div/label/span"))
            )
        except:
            print("Households without sanitation button found - Failed")
            exceptions.append(
                {"Exception": "Households without sanitation button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[4]/div/span/div/label/span").click()
            print("Households without sanitation button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_without_sanitation.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Number of schools button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[5]/div/span/div/label/span"))
            )
        except:
            print("Number of schools button found - Failed")
            exceptions.append(
                {"Exception": "Number of schools button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[5]/div/span/div/label/span").click()
            print("Number of schools button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_number_schools.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Lengths of rail in region button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[6]/div/span/div/label/span"))
            )
        except:
            print("Lengths of rail in region button found - Failed")
            exceptions.append(
                {"Exception": "Lengths of rail in region button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[6]/div/span/div/label/span").click()
            print("Lengths of rail in region button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_rail_length.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Lengths of road button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[7]/div/span/div/label/span"))
            )
        except:
            print("Lengths of road button found - Failed")
            exceptions.append(
                {"Exception": "Lengths of road button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[7]/div/span/div/label/span").click()
            print("Lengths of road button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_road_length.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Net Sown Area button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[8]/div/span/div/label/span"))
            )
        except:
            print("Net Sown Area button found - Failed")
            exceptions.append(
                {"Exception": "Net Sown Area button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[8]/div/span/div/label/span").click()
            print("Net Sown Area button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_sown_area.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Mean Sex Ratio button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[9]/div/span/div/label/span"))
            )
        except:
            print("Mean Sex Ratio button found - Failed")
            exceptions.append(
                {"Exception": "Mean Sex Ratio button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[9]/div/span/div/label/span").click()
            print("Mean Sex Ratio button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_sex_ratio.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Total population affected button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[10]/div/span/div/label/span"))
            )
        except:
            print("Total population affected button found - Failed")
            exceptions.append(
                {"Exception": "Total population affected button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[10]/div/span/div/label/span").click()
            print("Total population affected button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_population_affected.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Human Lives Lost button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[11]/div/span/div/label/span"))
            )
        except:
            print("Human Lives Lost button found - Failed")
            exceptions.append(
                {"Exception": "Total population affected button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[11]/div/span/div/label/span").click()
            print("Human Lives Lost button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_humans_life_lost.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Total Crop Area Affected button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[12]/div/span/div/label/span"))
            )
        except:
            print("Total Crop Area Affected button found - Failed")
            exceptions.append(
                {"Exception": "Total Crop Area Affected button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[12]/div/span/div/label/span").click()
            print("Total Crop Area Affected button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_crop_area_affected.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Total Number of Embankments Affected button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[13]/div/span/div/label/span"))
            )
        except:
            print("Total Number of Embankments Affected button found - Failed")
            exceptions.append(
                {"Exception": "Total Number of Embankments Affected button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[13]/div/span/div/label/span").click()
            print("Total Number of Embankments Affected button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_embankments_affected.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Total Number of Roads Damaged button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[14]/div/span/div/label/span"))
            )
        except:
            print("Total Number of Roads Damaged button found - Failed")
            exceptions.append(
                {"Exception": "Total Number of Roads Damaged button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[14]/div/span/div/label/span").click()
            print("Total Number of Roads Damaged button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_roads_damaged.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)


        # click on the Number of Bridges damaged button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[15]/div/span/div/label/span"))
            )
        except:
            print("Number of Bridges damaged button found - Failed")
            exceptions.append(
                {"Exception": "Number of Bridges damaged button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[15]/div/span/div/label/span").click()
            print("Number of Bridges damaged button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_bridges_damaged.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Number of embankments breached button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[16]/div/span/div/label/span"))
            )
        except:
            print("Number of embankments breached button found - Failed")
            exceptions.append(
                {"Exception": "Number of embankments breached button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[2]/div[16]/div/span/div/label/span").click()
            print("Number of embankments breached button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}vulnerability_embankments_breached.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Collapse Vulnerability options button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div/div/div/div[1]"))
            )
        except:
            print("Collapse Vulnerability options button found - Failed")
            exceptions.append(
                {"Exception": "Collapse Vulnerability options button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[3]/div/div/div/div[1]").click()
            print("Collapse Vulnerability options button click - Passed")
            time.sleep(2)

        # click on the expand Government Response options button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div/div/div/div[1]"))
            )
        except:
            print("Expand Government Response options button found - Failed")
            exceptions.append(
                {"Exception": "Expand Government Response options button found - Failed",
                 }
            )
        else:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(5)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div/div/div/div[1]").click()
            print("Expand Government Response options button click - Passed")
            time.sleep(2)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}govt_response_show_options.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)


        # click on the Flood Tenders button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div/span/div/label/span"))
            )
        except:
            print("Flood Tenders button found - Failed")
            exceptions.append(
                {"Exception": "Flood Tenders button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div/span/div/label/span").click()
            print("Flood Tenders button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}govt_response_flood_tenders.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)


        # click on the Flood Tenders SDRF button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[2]/div/span/div/label/span"))
            )
        except:
            print("Flood Tenders SDRF button found - Failed")
            exceptions.append(
                {"Exception": "Flood Tenders SDRF button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[2]/div/span/div/label/span").click()
            print("Flood Tenders SDRF button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}govt_response_flood_tenders_sdrf.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on Flood Tenders for Repairs and Restoration button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[3]/div/span/div/label/span"))
            )
        except:
            print("Flood Tenders for Repairs and Restoration button found - Failed")
            exceptions.append(
                {"Exception": "Flood Tenders for Repairs and Restoration button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[3]/div/span/div/label/span").click()
            print("Flood Tenders for Repairs and Restoration button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}govt_response_flood_tenders_repair_restore.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Flood Tenders for Immediate Measures button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[4]/div/span/div/label/span"))
            )
        except:
            print("Flood Tenders for Immediate Measures button found - Failed")
            exceptions.append(
                {"Exception": "Flood Tenders for Immediate Measures button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[4]/div/span/div/label/span").click()
            print("Flood Tenders for Immediate Measures button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}govt_response_flood_tenders_immediate_measures.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Flood tenders related to Others button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[5]/div/span/div/label/span"))
            )
        except:
            print("Flood tenders related to Others button found - Failed")
            exceptions.append(
                {"Exception": "Flood tenders related to Others button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[5]/div/span/div/label/span").click()
            print("Flood tenders related to Others button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}govt_response_flood_tenders_other.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Funds allocated through SDRF during SEC meetings button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[6]/div/span/div/label/span"))
            )
        except:
            print("Funds allocated through SDRF during SEC meetings button found - Failed")
            exceptions.append(
                {"Exception": "Funds allocated through SDRF during SEC meetings button found - Failed",
                 }
            )
        else:
            time.sleep(1)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div[2]/div[6]/div/span/div/label/span").click()
            print("Funds allocated through SDRF during SEC meetings button click - Passed")
            time.sleep(3)
            # Define the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f'{ss_prefix}govt_response_funds_allocated_sdrf_sec.png')

            # Capture and save the screenshot
            driver.save_screenshot(screenshot_path)

        # click on the Collapse Government Response options button.
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div/div/div/div[1]"))
            )
        except:
            print("Collapse Government Response options button found - Failed")
            exceptions.append(
                {"Exception": "Collapse Government Response options button found - Failed",
                 }
            )
        else:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(5)
            driver.find_element(By.XPATH, "/html/body/main/div/aside/div/div[1]/div[4]/div[1]/div/div[2]/div[4]/div/div/div/div[1]").click()
            print("Collapse Government Response options button click - Passed")
            time.sleep(2)
# import pytest
# import logging
# import pandas as pd
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from Contact_Us_Page.Page import ContactUsPage
# from Utils.Browser_setup import get_driver
# import os
#
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
# @pytest.fixture(scope="function")
# def driver():
#     driver = get_driver()  # Assuming this sets up your WebDriver instance
#     yield driver
#     driver.quit()
#
# @pytest.fixture(scope="function")
# def contact_us_page(driver):
#     driver.get("http://65.2.3.188/contact-us")  # Adjust URL as per your application
#     return ContactUsPage(driver)
#
# def read_test_data(file_path):
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"The file at path {file_path} does not exist.")
#     data = pd.read_excel(file_path)
#     return data
#
# def write_test_result(file_path, index, result, actual_message):
#     df = pd.read_excel(file_path)
#     df.at[index, 'Result'] = result
#     df.at[index, 'Actual_Message'] = actual_message
#     df.to_excel(file_path, index=False)
#
# @pytest.mark.parametrize("index, test_data", read_test_data("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx").iterrows())
# def test_contact_us_form(contact_us_page, index, test_data):
#     logging.info(f"Running test case {index}: {test_data}")
#
#     fullname = test_data['fullname']
#     email = test_data['email']
#     phone = str(test_data['phone']) if not pd.isnull(test_data['phone']) else ''
#     message = test_data['message']
#     expected_result = str(test_data['expected_result']).strip().lower() if not pd.isnull(test_data['expected_result']) else ''
#
#     contact_us_page.enter_fullname(fullname)
#     contact_us_page.enter_email(email)
#     contact_us_page.enter_phone(phone)
#     contact_us_page.enter_message(message)
#
#     try:
#         contact_us_page.click_submit()
#
#         if "thank you" in expected_result:
#             try:
#                 # Wait for success message to appear
#                 success_message_locator = (By.XPATH, "//h2[text()='Thank you']")
#                 success_message = WebDriverWait(contact_us_page.driver, 10).until(
#                     EC.visibility_of_element_located(success_message_locator)
#                 )
#                 actual_message = "Thank you"
#                 logging.info("Test passed. Success message found.")
#                 result = 'Pass'
#             except TimeoutException:
#                 actual_message = 'TimeoutException: Thank You message not found'
#                 logging.error("TimeoutException: Thank You message not found")
#                 result = 'Fail'
#         else:
#             # Check for validation error messages
#             error_messages = contact_us_page.get_error_messages()
#             logging.info(f"Validation Messages: {error_messages}")
#
#             if not error_messages and expected_result:
#                 # No error messages found, expected success message 'Thank You' was not received
#                 logging.error(f"Expected result '{expected_result}' not found in error messages.")
#                 result = 'Fail'
#                 actual_message = 'Thank You not found'
#                 write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, result, actual_message)
#                 pytest.fail(f"Expected result '{expected_result}' not found in error messages.")
#
#             if error_messages and expected_result:
#                 # Error messages found, check if any expected validation message exists
#                 matched = any(expected_msg.lower() in (msg.lower() for msg in error_messages) for expected_msg in expected_result.split(';') if expected_result)
#                 if not matched:
#                     logging.error(f"Expected result '{expected_result}' not found in error messages.")
#                     result = 'Fail'
#                     actual_message = '; '.join(error_messages)
#                     write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, result, actual_message)
#                     pytest.fail(f"Expected result '{expected_result}' not found in error messages.")
#                 else:
#                     result = 'Pass'
#                     actual_message = '; '.join(error_messages)
#
#         write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, result, actual_message)
#
#     except TimeoutException:
#         actual_message = 'TimeoutException: Expected result not found'
#         logging.error(f"Test failed: {actual_message}")
#         write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, 'Fail', actual_message)
#         pytest.fail(f"Expected result '{expected_result}' not found within the timeout period.")
#     except Exception as e:
#         actual_message = str(e)
#         logging.error(f"Test failed: An unexpected error occurred - {e}")
#         write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, 'Fail', actual_message)
#         pytest.fail(f"An unexpected error occurred: {e}")

import pytest
import logging
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Contact_Us_Page.Page import ContactUsPage
from Utils.Browser_setup import get_driver
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="function")
def driver():
    driver = get_driver()  # Assuming this sets up your WebDriver instance
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def contact_us_page(driver):
    driver.get("http://65.2.3.188/contact-us")  # Adjust URL as per your application
    return ContactUsPage(driver)

def read_test_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at path {file_path} does not exist.")
    data = pd.read_excel(file_path)
    return data

def write_test_result(file_path, index, result, actual_message):
    df = pd.read_excel(file_path)
    df.at[index, 'Result'] = result
    df.at[index, 'Actual_Message'] = actual_message
    df.to_excel(file_path, index=False)

@pytest.mark.parametrize("index, test_data", read_test_data("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx").iterrows())
def test_contact_us_form(contact_us_page, index, test_data):
    logging.info(f"Running test case {index}: {test_data}")

    fullname = test_data['fullname']
    email = test_data['email']
    phone = str(test_data['phone']) if not pd.isnull(test_data['phone']) else ''
    message = test_data['message']
    expected_result = str(test_data['expected_result']).strip().lower() if not pd.isnull(test_data['expected_result']) else ''

    contact_us_page.enter_fullname(fullname)
    contact_us_page.enter_email(email)
    contact_us_page.enter_phone(phone)
    contact_us_page.enter_message(message)

    try:
        contact_us_page.click_submit()

        if "thank you" in expected_result:
            try:
                # Wait for success message to appear
                success_message_locator = (By.XPATH, "//h2[text()='Thank you']")
                success_message = WebDriverWait(contact_us_page.driver, 10).until(
                    EC.visibility_of_element_located(success_message_locator)
                )
                actual_message = "Thank you"
                logging.info("Test passed. Success message found.")
                result = 'Pass'
            except TimeoutException:
                actual_message = 'TimeoutException: Thank You message not found'
                logging.error("TimeoutException: Thank You message not found")
                result = 'Fail'
        else:
            # Check for validation error messages
            error_messages = contact_us_page.get_error_messages()
            logging.info(f"Validation Messages: {error_messages}")

            if not error_messages and expected_result:
                # No error messages found, expected success message 'Thank You' was not received
                logging.error(f"Expected result '{expected_result}' not found in error messages.")
                result = 'Fail'
                actual_message = 'Form submitted successfully but expected validation message was missing'
                write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, result, actual_message)
                pytest.fail(f"Expected result '{expected_result}' not found in error messages.")

            if error_messages and expected_result:
                # Error messages found, check if any expected validation message exists
                matched = any(expected_msg.lower() in (msg.lower() for msg in error_messages) for expected_msg in expected_result.split(';') if expected_result)
                if not matched:
                    logging.error(f"Expected result '{expected_result}' not found in error messages.")
                    result = 'Fail'
                    actual_message = '; '.join(error_messages)
                    write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, result, actual_message)
                    pytest.fail(f"Expected result '{expected_result}' not found in error messages.")
                else:
                    result = 'Pass'
                    actual_message = '; '.join(error_messages)

        write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, result, actual_message)

    except TimeoutException:
        actual_message = 'TimeoutException: Expected result not found'
        logging.error(f"Test failed: {actual_message}")
        write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, 'Fail', actual_message)
        pytest.fail(f"Expected result '{expected_result}' not found within the timeout period.")
    except Exception as e:
        actual_message = str(e)
        logging.error(f"Test failed: An unexpected error occurred - {e}")
        write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, 'Fail', actual_message)
        pytest.fail(f"An unexpected error occurred: {e}")

import logging
import pytest
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
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def contact_us_page(driver):
    driver.get("http://65.2.3.188/contact-us")
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
    phone = test_data['phone']
    message = test_data['message']
    expected_result = test_data['expected_result']

    contact_us_page.enter_fullname(fullname)
    contact_us_page.enter_email(email)
    contact_us_page.enter_phone(phone)
    contact_us_page.enter_message(message)
    contact_us_page.click_submit()

    try:
        if "Thank you" in expected_result:
            success_message = WebDriverWait(contact_us_page.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[text()='Thank you']"))
            )
            logging.info("Test passed. Success message found.")
            assert "Thank you" in success_message.text
            write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, 'Pass', success_message.text)
        else:
            error_messages = contact_us_page.get_error_messages()
            logging.info(f"Test passed. Validation Messages: {error_messages}")
            matched = any(expected_msg in error_messages for expected_msg in expected_result.split(';'))
            if not matched:
                logging.error(f"Expected result '{expected_result}' not found in error messages.")
                actual_message = '; '.join(error_messages)
                write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, 'Fail', actual_message)
                pytest.fail(f"Expected result '{expected_result}' not found in error messages. Actual messages: {actual_message}")
            assert matched
            write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, 'Pass', '; '.join(error_messages))

    except TimeoutException:
        logging.error(f"Test failed: Expected result '{expected_result}' not found within the timeout period.")
        actual_message = 'TimeoutException: Expected result not found'
        write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, 'Fail', actual_message)
        pytest.fail(f"Expected result '{expected_result}' not found within the timeout period. Actual message: {actual_message}")
    except Exception as e:
        logging.error(f"Test failed: An unexpected error occurred - {e}")
        actual_message = str(e)
        write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", index, 'Fail', actual_message)
        pytest.fail(f"An unexpected error occurred: {e}")



#
# def test_submit_valid_data_different_combinations_f_e(contact_us_page):
#     # Sample valid data
#     valid_data = {
#         'fullname': "Clarke",
#         'email': "john.doe@example.in",
#         'phone': "9876543210",
#         'message': "This is a test message that is properly long.",
#         'expected_result': "Thank you"
#     }
#
#     contact_us_page.enter_fullname(valid_data['fullname'])
#     contact_us_page.enter_email(valid_data['email'])
#     contact_us_page.enter_phone(valid_data['phone'])
#     contact_us_page.enter_message(valid_data['message'])
#     contact_us_page.click_submit()
#
#     try:
#         success_message = WebDriverWait(contact_us_page.driver, 10).until(
#             EC.visibility_of_element_located((By.XPATH, "//h2[text()='Thank you']"))
#         )
#         logging.info("Test 'test_submit_valid_data_different_combinations_f_e' passed.")
#         write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", 0, 'Pass', success_message.text)
#
#     except TimeoutException:
#         logging.error("Test 'test_submit_valid_data_different_combinations_f_e' failed: Success message not found within the timeout period.")
#         write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", 0, 'Fail', 'TimeoutException: Success message not found')
#         pytest.fail("Success message not found within the timeout period.")
#     except Exception as e:
#         logging.error(f"Test 'test_submit_valid_data_different_combinations_f_e' failed: An unexpected error occurred - {e}")
#         write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", 0, 'Fail', str(e))
#         pytest.fail("An unexpected error occurred.")
#
# def test_submit_empty_fields(contact_us_page):
#     # Sample empty data
#     empty_data = {
#         'fullname': "",
#         'email': "",
#         'phone': "",
#         'message': "",
#         'expected_result': "The name field is required!; The email field is required!; The phone field is required!; The message field is required!"
#     }
#
#     contact_us_page.enter_fullname(empty_data['fullname'])
#     contact_us_page.enter_email(empty_data['email'])
#     contact_us_page.enter_phone(empty_data['phone'])
#     contact_us_page.enter_message(empty_data['message'])
#     contact_us_page.click_submit()
#
#     try:
#         error_messages = contact_us_page.get_error_messages()
#         logging.info(f"Test 'test_submit_empty_fields' passed. Error Messages: {error_messages}")
#         write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", 1, 'Pass', '; '.join(error_messages))
#         assert "The name field is required!" in error_messages
#         assert "The email field is required!" in error_messages
#         assert "The phone field is required!" in error_messages
#         assert "The message field is required!" in error_messages
#
#     except TimeoutException:
#         logging.error("Test 'test_submit_empty_fields' failed: Error message not found within the timeout period.")
#         write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", 1, 'Fail', 'TimeoutException: Error messages not found')
#         pytest.fail("Error message not found within the timeout period.")
#     except Exception as e:
#         logging.error(f"Test 'test_submit_empty_fields' failed: An unexpected error occurred - {e}")
#         write_test_result("C:/Users/Manikandan A/Documents/contact_us_test_data.xlsx", 1, 'Fail', str(e))
#         pytest.fail("An unexpected error occurred.")



# import logging
# import pytest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from logging_config import setup_logging
#
#
# from Contact_Us_Page.Page import ContactUsPage
# from Utils.Browser_setup import get_driver
#
#
#
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
# @pytest.fixture(scope="function")
# def driver():
#     driver = get_driver()
#     yield driver
#     driver.quit()
#
# @pytest.fixture(scope="function")
#
# def contact_us_page(driver):
#     driver.get("http://65.2.3.188/contact-us")
#     return ContactUsPage(driver)
#
# def test_submit_valid_data_different_combinations_f_e(contact_us_page):
#     contact_us_page.enter_fullname("Clarke")
#     contact_us_page.enter_email("john.doe@example.in")
#     contact_us_page.enter_phone("9876543210")
#     contact_us_page.enter_message("This is a test message that is properly long.")
#     contact_us_page.click_submit()
#
#     try:
#         # Waiting for the success message to appear
#         success_message = WebDriverWait(contact_us_page.driver, 10).until(
#             EC.visibility_of_element_located((By.XPATH, "//h2[text()='Thank you']"))
#         )
#         logging.info("Test 'test_submit_valid_data' passed.")
#         assert "Thank you" in success_message.text
#
#     except TimeoutException:
#         logging.error("Test 'test_submit_valid_data' failed: Success message not found within the timeout period.")
#         pytest.fail("Success message not found within the timeout period.")
#     except Exception as e:
#         logging.error(f"Test 'test_submit_valid_data' failed: An unexpected error occurred - {e}")
#         pytest.fail("An unexpected error occurred.")
#
# def test_submit_valid_data_both_first_surname(contact_us_page):
#     contact_us_page.enter_fullname("John Doe")
#     contact_us_page.enter_email("john.doe@example.com")
#     contact_us_page.enter_phone("9876543210")
#     contact_us_page.enter_message("This is a test message that is properly long.")
#     contact_us_page.click_submit()
#
#     try:
#         # Waiting for the success message to appear
#         success_message = WebDriverWait(contact_us_page.driver, 10).until(
#             EC.visibility_of_element_located((By.XPATH, "//h2[text()='Thank you']"))
#         )
#         logging.info("Test 'test_submit_valid_data' passed.")
#         assert "Thank you" in success_message.text
#
#     except TimeoutException:
#         logging.error("Test 'test_submit_valid_data' failed: Success message not found within the timeout period.")
#         pytest.fail("Success message not found within the timeout period.")
#     except Exception as e:
#         logging.error(f"Test 'test_submit_valid_data' failed: An "
#                       f"unexpected error occurred - {e}")
#         pytest.fail("An unexpected error occurred.")
#
# def test_submit_space_as_character(contact_us_page):
#     contact_us_page.enter_fullname("   ")
#     contact_us_page.enter_email("john.doe@example.com")
#     contact_us_page.enter_phone("9876543210")
#     contact_us_page.enter_message("This is a test message that is properly long.")
#     contact_us_page.click_submit()
#
#     try:
#         error_messages = contact_us_page.get_error_messages()
#         logging.info(f"Test 'test_submit_empty_fullname' passed. Validation Message: {error_messages}")
#         assert "Please enter only characters" in error_messages
#     except TimeoutException:
#         logging.error("Test 'test_submit_empty_fullname' failed: Error message not found within the timeout period.")
#         pytest.fail("Error message not found within the timeout period.")
#
# def test_submit_digits_as_name(contact_us_page):
#     contact_us_page.enter_fullname("123456")
#     contact_us_page.enter_email("john.doe@example.com")
#     contact_us_page.enter_phone("9876543210")
#     contact_us_page.enter_message("This is a test message that is properly long.")
#     contact_us_page.click_submit()
#
#     try:
#         error_messages = contact_us_page.get_error_messages()
#         logging.info(f"Test 'test_submit_empty_fullname' passed. Validation Message: {error_messages}")
#         assert "Please enter only characters" in error_messages
#     except TimeoutException:
#         logging.error("Test 'test_submit_empty_fullname' failed: Error message not found within the timeout period.")
#         pytest.fail("Error message not found within the timeout period.")
#
# def test_submit_invalid_email(contact_us_page):
#     contact_us_page.enter_fullname("John Doe")
#     contact_us_page.enter_email("john.doe@invalid")
#     contact_us_page.enter_phone("9876543210")
#     contact_us_page.enter_message("This is a test message that is properly long.")
#     contact_us_page.click_submit()
#
#     try:
#         error_messages = contact_us_page.get_error_messages()
#         logging.info(f"Test 'test_submit_invalid_email' passed. Validation Message: {error_messages}")
#         assert "Please enter a valid email address." in error_messages
#     except TimeoutException:
#         logging.error("Test 'test_submit_invalid_email' failed: Error message not found within the timeout period.")
#         pytest.fail("Error message not found within the timeout period.")
#
# def test_submit_invalid_phone(contact_us_page):
#     contact_us_page.enter_fullname("John Doe")
#     contact_us_page.enter_email("john.doe@example.com")
#     contact_us_page.enter_phone("12345abcde")
#     contact_us_page.enter_message("This is a test message that is properly long.")
#     contact_us_page.click_submit()
#
#     try:
#         error_messages = contact_us_page.get_error_messages()
#         logging.info(f"Test 'test_submit_invalid_phone' passed. Validation Message: {error_messages}")
#         assert "Please enter 10 digits" in error_messages
#     except TimeoutException:
#         logging.error("Test 'test_submit_invalid_phone' failed: Error message not found within the timeout period.")
#         pytest.fail("Error message not found within the timeout period.")
#
# def test_submit_invalid_phone(contact_us_page):
#     contact_us_page.enter_fullname("John Doe")
#     contact_us_page.enter_email("john.doe@example.com")
#     contact_us_page.enter_phone("12345abcde")
#     contact_us_page.enter_message("This is a test message that is properly long.")
#     contact_us_page.click_submit()
#
#     try:
#         error_messages = contact_us_page.get_error_messages()
#         logging.info(f"Test 'test_submit_invalid_phone' passed. Validation Message: {error_messages}")
#         assert "Please enter 10 digits" in error_messages
#     except TimeoutException:
#         logging.error("Test 'test_submit_invalid_phone' failed: Error message not found within the timeout period.")
#         pytest.fail("Error message not found within the timeout period.")
#
#
# def test_submit_short_message(contact_us_page):
#     contact_us_page.enter_fullname("John Doe")
#     contact_us_page.enter_email("john.doe@example.com")
#     contact_us_page.enter_phone("9876543210")
#     contact_us_page.enter_message("Too short")
#     contact_us_page.click_submit()
#
#     try:
#         error_messages = contact_us_page.get_error_messages()
#         logging.info(f"Test 'test_submit_short_message' passed. Validation Message: {error_messages}")
#         assert "Please enter at least 20 characters." in error_messages
#     except TimeoutException:
#         logging.error("Test 'test_submit_short_message' failed: Error message not found within the timeout period.")
#         pytest.fail("Error message not found within the timeout period.")
#
# def test_submit_long_message(contact_us_page):
#     long_message = "x" * 201
#     contact_us_page.enter_fullname("John Doe")
#     contact_us_page.enter_email("john.doe@example.com")
#     contact_us_page.enter_phone("9876543210")
#     contact_us_page.enter_message(long_message)
#     contact_us_page.click_submit()
#
#     try:
#         error_messages = contact_us_page.get_error_messages()
#         logging.info(f"Test 'test_submit_long_message' passed. Validation Message: {error_messages}")
#         assert "Please enter no more than 200 characters." in error_messages
#     except TimeoutException:
#         logging.error("Test 'test_submit_long_message' failed: Error message not found within the timeout period.")
#         pytest.fail("Error message not found within the timeout period.")
#
# def test_submit_empty_fullname(contact_us_page):
#     contact_us_page.enter_fullname("")
#     contact_us_page.enter_email("john.doe@example.com")
#     contact_us_page.enter_phone("9876543210")
#     contact_us_page.enter_message("This is a test message that is properly long.")
#     contact_us_page.click_submit()
#
#     try:
#         error_messages = contact_us_page.get_error_messages()
#         logging.info(f"Test 'test_submit_empty_fullname' passed. Validation Message: {error_messages}")
#         assert "The name field is required!" in error_messages
#     except TimeoutException:
#         logging.error("Test 'test_submit_empty_fullname' failed: Error message not found within the timeout period.")
#         pytest.fail("Error message not found within the timeout period.")
#
# # def test_submit_space_as_character(contact_us_page):
# #     contact_us_page.enter_fullname("Clarke")
# #     contact_us_page.enter_email("john.doe@example.com")
# #     contact_us_page.enter_phone("9876543210")
# #     contact_us_page.enter_message("                                          ")
# #     contact_us_page.click_submit()
# #
# #     try:
# #         error_messages = contact_us_page.get_error_messages()
# #         logging.info(f"Test 'test_submit_empty_fullname' passed. Validation Message: {error_messages}")
# #         assert "Please enter only characters" in error_messages
# #     except TimeoutException:
# #         logging.error("Test 'test_submit_empty_fullname' failed: Error message not found within the timeout period.")
# #         pytest.fail("Error message not found within the timeout period.")
#
# def test_all_fields_invalid(contact_us_page):
#     contact_us_page.enter_fullname("JD")
#     contact_us_page.enter_email("john.doe@invalid")
#     contact_us_page.enter_phone("12345abcde")
#     contact_us_page.enter_message("Too short")
#     contact_us_page.click_submit()
#
#     try:
#         error_messages = contact_us_page.get_error_messages()
#         logging.info(f"Test 'test_all_fields_invalid' passed. Error Messages: {error_messages}")
#         print("Error Messages:", error_messages)  # Print error messages for debugging
#         print("Generator expression results:", error_messages)  # Print generator expression results
#         assert any("5 characters" in msg for msg in error_messages)
#         assert "Please enter a valid email address." in error_messages
#         assert "Please enter 10 digits" in error_messages
#         assert "Please enter at least 20 characters." in error_messages
#     except TimeoutException:
#         logging.error("Test 'test_all_fields_invalid' failed: Error message not found within the timeout period.")
#         pytest.fail("Error message not found within the timeout period.")
#
# def test_submit_valid_data_different_combinations_e(contact_us_page):
#     contact_us_page.enter_fullname("Clarke")
#     contact_us_page.enter_email("john.doe@example.co.in")
#     contact_us_page.enter_phone("9876543210")
#     contact_us_page.enter_message("This is a test message that is properly long.")
#     contact_us_page.click_submit()
#
#     try:
#         # Waiting for the success message to appear
#         success_message = WebDriverWait(contact_us_page.driver, 10).until(
#             EC.visibility_of_element_located((By.XPATH, "//h2[text()='Thank you']"))
#         )
#         logging.info("Test 'test_submit_valid_data' passed.")
#         assert "Thank you" in success_message.text
#
#     except TimeoutException:
#         logging.error("Test 'test_submit_valid_data' failed: Success message not found within the timeout period.")
#         pytest.fail("Success message not found within the timeout period.")
#     except Exception as e:
#         logging.error(f"Test 'test_submit_valid_data' failed: An unexpected error occurred - {e}")
#         pytest.fail("An unexpected error occurred.")
#
#
# def test_submit_empty_fields(contact_us_page):
#     contact_us_page.enter_fullname("")
#     contact_us_page.enter_email("")
#     contact_us_page.enter_phone("")
#     contact_us_page.enter_message("")
#     contact_us_page.click_submit()
#
#     try:
#         error_messages = contact_us_page.get_error_messages()
#         logging.info(f"Test 'test_submit_empty_fields' passed. Error Messages: {error_messages}")
#         assert "The name field is required!" in error_messages
#         assert "The email field is required!" in error_messages
#         assert "The phone field is required!" in error_messages
#         assert "The message field is required!" in error_messages
#     except TimeoutException:
#         logging.error("Test 'test_submit_empty_fields' failed: Error message not found within the timeout period.")
#         pytest.fail("Error message not found within the timeout period.")

import logging
import Pytest
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
import loggin
import pytest
from Utils.Browser_setup import get_driver
from Contact_Us_Test.logging_config import setup_logging



@pytest.fixture(scope="session")
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

setup_logging()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # log test result
    if report.when == 'call':
        if report.failed:
            logging.error(f"Test {item.name} failed: {report.longrepr}")
        elif report.passed:
            logging.info(f"Test {item.name} passed")

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    logging.info("Starting test session")

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    logging.info("Ending test session")

import os

import pytest
from selenium import webdriver

from page_object.report_page import ReportPage

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session")
def chrome_driver():
    # driver = webdriver.Chrome(f"{ROOT_DIR}/driver/chromedriver")
    driver = webdriver.Chrome("{}/driver/chromedriver".format(ROOT_DIR))
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def report_page(chrome_driver):
    report_page = ReportPage(chrome_driver)
    report_page.go_to_site()
    return report_page

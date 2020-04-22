from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.base_url = "http://localhost:8888"

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                      message="Can't find element by locator {}".format(locator))

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                      message="Can't find elements by locator {}".format(locator))

    def find_elements_by_xpath(self, locator):
        return self.driver.find_elements_by_xpath(locator)

    def find_elements_count(self, locator):
        number_of_elements = len(self.find_elements_by_xpath(locator))
        print("NUMBER OF ELEMENTS ", number_of_elements)
        return number_of_elements

    def go_to_site(self):
        return self.driver.get(self.base_url)

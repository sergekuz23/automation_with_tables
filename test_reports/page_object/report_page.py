from selenium.webdriver.common.by import By
from page_object.base_page import BasePage
import re


class ReportLocators:

    ROTATIONS_LOCATOR = (By.XPATH, "//*[@id='by-day-rotation'] //*[@class='data-value']")
    ROTATIONS_VALUE_LOCATOR = (By.XPATH, "//*[@id='by-day-rotation'] //*[@class='data-value right-align']")
    REPORT_DATA = (By.XPATH, "//body/section[@id='summary']|//section[@id='groups']")

    # By Day Rotation
    ALL_ROTATIONS = (By.XPATH, "//*[@id='by-day-rotation-data']//*[@class='data-value']")
    ALL_VALUES_IN_ROTATIONS = "//*[@id='by-day-rotation-data']//*[@class='data-value right-align']"
    ALL_COLUMN_HEADERS_IN_ROTATIONS = (By.XPATH, "//section[@id='by-day-rotation']//div[contains(@class, 'column-label')]")
    ALL_CELLS_WITH_DATA_IN_TABLE = (By.XPATH, "//section[@id='by-day-rotation']//div[contains(@class, 'data-value')]")
    ALL_DATA_CELLS_BY_DAY = "//section[@id='by-day-rotation']//div[contains(@class, 'data-value')]"
    ALL_ROTATIONS_IN_BY_DAY = (By.XPATH, "//*[@id='by-day-rotation-data']//*[@class='data-value']")

    # By Creative
    CELLS_DATA_IN_BY_CREATIVE = (By.XPATH,"//div[@id='by-creative-data']/div[@class='data-value right-align']")
    ALL_COLUMN_HEADERS_IN_BY_CREATIVE = (By.XPATH, "//section[@id='by-creative']//div[contains(@class, 'column-label')]")
    CREATIVE = (By.XPATH,"//div[@id='by-creative-data']/div[@class='data-value']")
    CELLS_DATA = "//div[@id='by-creative-data']/div[@class='data-value right-align']"

    # Summary
    TOTAL_SPEND = "//section[@id='summary']/div[@id='total-spend']"
    TOTAL_VIEWS = "//section[@id='summary']/div[@id='total-views']"
    TOTAL_SPOTS = "//section[@id='summary']/div[@id='total-spots']"


class RegEx:

    ROTATION_FORMAT = r'\d\d/\d\d/\d\d\d\d\sMORNING|AFTERNOON|PRIME'
    SPEND_FORMAT = r'\d*(.\d)'
    VIEWS_FORMAT = r'\d*'
    CURRENCY_FORMAT = r'^\$([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(\.[0-9][0-9])?$'


class ReportPage(BasePage):

    def find_number_of_elements(self, locator):
        number_of_elements = len(self.find_elements(locator))
        return number_of_elements

    def verify_calculation(self, day, day_value):
        spend_value = day_value[0].text
        views_value = day_value[1].text
        cpv_value = day_value[2].text
        result_cpv = round(self.calculate_cpv(spend_value, views_value), 2)
        if float(cpv_value.replace('$', '')) != result_cpv:
            print('{} error'.format(day))
            assert float(cpv_value.replace('$', '')) == result_cpv, "{} IS NOT CORRECT. EXPECTED {}".format(cpv_value, result_cpv)

    def verify_page_has_loaded(self):
        assert len(self.find_elements(ReportLocators.REPORT_DATA)) != 0, "THE REPORT HASN'T LOADED"

    def calculate_cpv(self, spend_value, views_value):
        return float(spend_value) / float(views_value)

    def calculate(self):
        number_of_rotations = self.find_number_of_elements(ReportLocators.ROTATIONS_LOCATOR)
        rotation_days = self.find_elements(ReportLocators.ROTATIONS_LOCATOR)
        all_rotation_values = self.find_elements(ReportLocators.ROTATIONS_VALUE_LOCATOR)
        interval = int(len(all_rotation_values) / number_of_rotations)
        list_of_values = [all_rotation_values[d:d + interval] for d in range(0, len(all_rotation_values), interval)]
        for day in rotation_days:
            day_value = list_of_values[rotation_days.index(day)]
            self.verify_calculation(day, day_value)

    def verify_rotations_format(self, data_type):
        if data_type == "Rotations":
            data_format = RegEx.ROTATION_FORMAT
            days = self.find_elements(ReportLocators.ALL_ROTATIONS)
            rotations_format_date = re.compile(data_format)
            failed_elements = []
            for day in days:
                format_matching = rotations_format_date.search(day.text)
                if format_matching is not None:
                    pass
                else:
                    failed_elements.append(day.text)
                    print("THE FORMAT IS NOT CORRECT ", day.text)
            assert len(failed_elements) == 0, "{} DATA HAS WRONG FORMAT. THE CORRECT FORMAT IS MM/DD/YYYY XXXXX".format(
                failed_elements)

    def currency_format(self, table):
        lines = ''
        items = ''
        if table == "By Day - Rotation":
            lines = ReportLocators.ROTATIONS_LOCATOR
            items = ReportLocators.ROTATIONS_VALUE_LOCATOR
        if table == "By Creative":
            lines = ReportLocators.CREATIVE
            items = ReportLocators.CELLS_DATA_IN_BY_CREATIVE
        number_of_rotations = self.find_number_of_elements(lines)
        all_rotation_values = self.find_elements(items)
        interval = int(len(all_rotation_values) / number_of_rotations)
        all_spend = all_rotation_values[::interval]
        currency_format = re.compile(RegEx.CURRENCY_FORMAT)
        failed_elements = []
        for spend in all_spend:
            format_matching = currency_format.search(spend.text)
            if format_matching is not None:
                pass
            else:
                failed_elements.append(spend.text)
        assert len(failed_elements) == 0, "{} 'SPEND' COLUMN HAS WRONG FORMAT. THE CORRECT FORMAT IS '$1,000.00'".format(
            failed_elements)

    def verify_the_number_of_columns_is_correct(self, table):
        number_of_cells = ''
        number_of_headers = ''
        if table == "By Day - Rotation":
            number_of_cells = self.find_number_of_elements(ReportLocators.ALL_CELLS_WITH_DATA_IN_TABLE)
            number_of_headers = self.find_number_of_elements(ReportLocators.ALL_COLUMN_HEADERS_IN_ROTATIONS)
        elif table == "By Creative":
            number_of_cells = self.find_number_of_elements(ReportLocators.ALL_CELLS_WITH_DATA_IN_TABLE)
            number_of_headers = self.find_number_of_elements(ReportLocators.ALL_COLUMN_HEADERS_IN_BY_CREATIVE)
        assert number_of_cells % number_of_headers == 0, "THE NUMBER OF COLUMNS IN TABLE {} IS NOT CORRECT".format(table)

    def verify_total_spend(self):
        creative_1 = int(self.driver.find_element_by_xpath(ReportLocators.CELLS_DATA + '[1]').text)
        creative_2 = int(self.driver.find_element_by_xpath(ReportLocators.CELLS_DATA + '[5]').text)
        total_spend = int(self.driver.find_element_by_xpath(ReportLocators.TOTAL_SPEND).text)
        actual_spend = creative_1+creative_2
        assert total_spend == actual_spend, "{} - THE TOTAL SPEND IS NOT CORRECT. EXPECTED {}".format(total_spend, actual_spend)

    def verify_total_views(self):
        creative_1 = int(self.driver.find_element_by_xpath(ReportLocators.CELLS_DATA + '[2]').text)
        creative_2 = int(self.driver.find_element_by_xpath(ReportLocators.CELLS_DATA + '[6]').text)
        total_views = int(self.driver.find_element_by_xpath(ReportLocators.TOTAL_VIEWS).text)
        actual_views = creative_1+creative_2
        assert total_views == actual_views, "{} - THE TOTAL VIEWS IS NOT CORRECT. EXPECTED NUMBER {}".format(total_views, actual_views)

    def verify_total_spots(self):
        rotations = self.find_number_of_elements(ReportLocators.ALL_ROTATIONS_IN_BY_DAY)
        total_spots = int(self.driver.find_element_by_xpath(ReportLocators.TOTAL_VIEWS).text)
        assert rotations == total_spots, "{} - TOTAL SPOTS IS NOT CORRECT. EXPECTED NUMBER {}".format(total_spots, rotations)

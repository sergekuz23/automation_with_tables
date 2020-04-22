from logging import Logger

from page_object.report_page import ReportPage

class TestReport:
    log = Logger('TestReport')

    def test_verify_page_loads(self, report_page):
        report_page.verify_page_has_loaded()

    def test_calculate_cpv(self, report_page):
        self.log.info('Calculating CPV')
        report_page.calculate()

    def test_verify_the_number_of_columns_is_correct_by_day(self, report_page):
        self.log.info('Verifying the number of columns in By Day - Rotation table')
        report_page.verify_the_number_of_columns_is_correct("By Day - Rotation")

    def test_verify_the_number_of_columns_is_correct_by_creative(self, report_page):
        self.log.info('Verifying the number of columns in By By Creative table')
        report_page.verify_the_number_of_columns_is_correct("By Creative")

    def test_verify_rotations_format(self, report_page):
        self.log.info('Verifying data format for Rotations')
        report_page.verify_rotations_format("Rotations")

    def test_verify_total_spend(self, report_page):
        self.log.info('Verifying total spend')
        report_page.verify_total_spend()

    def test_verify_total_views(self, report_page):
        self.log.info('Verifying total views')
        report_page.verify_total_views()

    def test_verify_total_spots(self, report_page):
        self.log.info('Verifying total spots')
        report_page.verify_total_spots()

    def test_currency_format(self, report_page):
        self.log.info('Verifying currency_format')
        report_page.currency_format(table="By Day - Rotation")

    def test_currency_format(self, report_page):
        self.log.info('Verifying currency_format')
        report_page.currency_format(table="By Creative")

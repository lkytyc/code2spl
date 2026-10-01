import datetime


class TimeUtils:
    def __init__(self):
        current_datetime = datetime.datetime.now()
        self.datetime = current_datetime

    def add_seconds(self, seconds):
        new_datetime = self.datetime + datetime.timedelta(seconds=seconds)
        format = "%H:%M:%S"
        result = new_datetime.strftime(format)
        return result

    def datetime_to_string(self):
        formatted_datetime = self.datetime.strftime("%Y-%m-%d %H:%M:%S")
        result = formatted_datetime
        return result

    def get_current_date(self):
        format = "%Y-%m-%d"
        result = self.datetime.strftime(format)
        return result

    def get_current_time(self):
        format = "%H:%M:%S"
        return_value = self.datetime.strftime(format)
        return return_value

    def get_format_time(self, year, month, day, hour, minute, second):
        format = "%Y-%m-%d %H:%M:%S"
        time_item = datetime.datetime(year, month, day, hour, minute, second)
        result = time_item.strftime(format)
        return result

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        result = round((time2 - time1).seconds / 60)
        return result

    @staticmethod
    def string_to_datetime(string):
        parsed_datetime = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        result = parsed_datetime
        return result

import unittest

class TimeUtilsTestGetCurrentDate(unittest.TestCase):
    def test_get_current_date_1(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_current_date(), timeutils.datetime.strftime("%Y-%m-%d"))

    def test_get_current_date_2(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_current_date(), timeutils.datetime.strftime("%Y-%m-%d"))

    def test_get_current_date_3(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_current_date(), timeutils.datetime.strftime("%Y-%m-%d"))

    def test_get_current_date_4(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_current_date(), timeutils.datetime.strftime("%Y-%m-%d"))

    def test_get_current_date_5(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_current_date(), timeutils.datetime.strftime("%Y-%m-%d"))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

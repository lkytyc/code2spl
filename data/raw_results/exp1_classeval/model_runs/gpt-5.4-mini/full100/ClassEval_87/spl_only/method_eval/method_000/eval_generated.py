import datetime


class TimeUtils:
    def __init__(self):
        current_datetime = datetime.datetime.now()
        self.datetime = current_datetime

    def get_current_time(self):
        format = "%H:%M:%S"
        return self.datetime.strftime(format)

    def get_current_date(self):
        format = "%Y-%m-%d"
        return self.datetime.strftime(format)

    def add_seconds(self, seconds):
        new_datetime = self.datetime + datetime.timedelta(seconds=seconds)
        format = "%H:%M:%S"
        return new_datetime.strftime(format)

    def string_to_datetime(self, string):
        parsed_datetime = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        return parsed_datetime

    def datetime_to_string(self, datetime):
        formatted_datetime = datetime.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_datetime

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        return round((time2 - time1).seconds / 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        format = "%Y-%m-%d %H:%M:%S"
        time_item = datetime.datetime(year, month, day, hour, minute, second)
        return time_item.strftime(format)

import unittest

class TimeUtilsTestGetCurrentTime(unittest.TestCase):
    def test_get_current_time_1(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_current_time(), timeutils.datetime.strftime("%H:%M:%S"))

    def test_get_current_time_2(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_current_time(), timeutils.datetime.strftime("%H:%M:%S"))

    def test_get_current_time_3(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_current_time(), timeutils.datetime.strftime("%H:%M:%S"))

    def test_get_current_time_4(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_current_time(), timeutils.datetime.strftime("%H:%M:%S"))

    def test_get_current_time_5(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_current_time(), timeutils.datetime.strftime("%H:%M:%S"))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

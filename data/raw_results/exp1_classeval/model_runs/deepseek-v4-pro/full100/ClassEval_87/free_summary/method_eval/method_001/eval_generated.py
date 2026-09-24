from datetime import datetime, timedelta

class TimeUtils:
    def __init__(self):
        self.current_datetime = datetime.now()

    def get_current_time(self):
        return self.current_datetime.strftime("%H:%M:%S")

    def get_current_date(self):
        return self.current_datetime.strftime("%Y-%m-%d")

    def add_seconds(self, seconds):
        new_datetime = self.current_datetime + timedelta(seconds=seconds)
        return new_datetime.strftime("%H:%M:%S")

    def string_to_datetime(self, datetime_str):
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

    def datetime_to_string(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def difference_in_minutes(self, datetime_str1, datetime_str2):
        dt1 = self.string_to_datetime(datetime_str1)
        dt2 = self.string_to_datetime(datetime_str2)
        diff = dt2 - dt1
        return diff.total_seconds() / 60

    def format_datetime(self, year, month, day, hour, minute, second):
        dt = datetime(year, month, day, hour, minute, second)
        return self.datetime_to_string(dt)

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

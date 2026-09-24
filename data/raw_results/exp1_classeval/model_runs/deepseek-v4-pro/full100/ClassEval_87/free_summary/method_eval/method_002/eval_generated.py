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

class TimeUtilsTestAddSeconds(unittest.TestCase):
    def test_add_seconds_1(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.add_seconds(600),
                         (timeutils.datetime + datetime.timedelta(seconds=600)).strftime("%H:%M:%S"))

    def test_add_seconds_2(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.add_seconds(500),
                         (timeutils.datetime + datetime.timedelta(seconds=500)).strftime("%H:%M:%S"))

    def test_add_seconds_3(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.add_seconds(400),
                         (timeutils.datetime + datetime.timedelta(seconds=400)).strftime("%H:%M:%S"))

    def test_add_seconds_4(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.add_seconds(300),
                         (timeutils.datetime + datetime.timedelta(seconds=300)).strftime("%H:%M:%S"))

    def test_add_seconds_5(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.add_seconds(200),
                         (timeutils.datetime + datetime.timedelta(seconds=200)).strftime("%H:%M:%S"))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

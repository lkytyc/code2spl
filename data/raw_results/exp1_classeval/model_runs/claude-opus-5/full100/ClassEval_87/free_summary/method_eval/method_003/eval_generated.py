import datetime


class TimeUtils:
    def __init__(self):
        self.snapshot = datetime.datetime.now()

    def get_current_time(self):
        return self.snapshot.strftime("%H:%M:%S")

    def get_current_date(self):
        return self.snapshot.strftime("%Y-%m-%d")

    def add_seconds(self, seconds):
        result = self.snapshot + datetime.timedelta(seconds=seconds)
        return result.strftime("%H:%M:%S")

    def string_to_datetime(self, string):
        return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def datetime_to_string(self, datetime):
        return datetime.strftime("%Y-%m-%d %H:%M:%S")

    def get_minutes(self, string_time1, string_time2):
        t1 = self.string_to_datetime(string_time1)
        t2 = self.string_to_datetime(string_time2)
        delta = t2 - t1
        return round(delta.seconds / 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        dt = datetime.datetime(year, month, day, hour, minute, second)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

import unittest

class TimeUtilsTestStringToDatetime(unittest.TestCase):
    def test_string_to_datetime_1(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.string_to_datetime('2001-7-18 1:1:1'), datetime.datetime(2001, 7, 18, 1, 1, 1))

    def test_string_to_datetime_2(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.string_to_datetime('2001-7-17 1:1:1'), datetime.datetime(2001, 7, 17, 1, 1, 1))

    def test_string_to_datetime_3(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.string_to_datetime('2001-7-16 1:1:1'), datetime.datetime(2001, 7, 16, 1, 1, 1))

    def test_string_to_datetime_4(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.string_to_datetime('2001-7-15 1:1:1'), datetime.datetime(2001, 7, 15, 1, 1, 1))

    def test_string_to_datetime_5(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.string_to_datetime('2001-7-14 1:1:1'), datetime.datetime(2001, 7, 14, 1, 1, 1))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

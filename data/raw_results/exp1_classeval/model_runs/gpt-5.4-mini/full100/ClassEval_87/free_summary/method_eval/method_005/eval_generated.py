from datetime import datetime, timedelta


class TimeUtils:
    def __init__(self):
        self.datetime = datetime.now()

    def get_current_time(self):
        return self.datetime.strftime("%H:%M:%S")

    def get_current_date(self):
        return self.datetime.strftime("%Y-%m-%d")

    def add_seconds(self, seconds):
        self.datetime = self.datetime + timedelta(seconds=seconds)
        return self.datetime.strftime("%H:%M:%S")

    def string_to_datetime(self, string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def datetime_to_string(self, datetime_obj):
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

    def get_minutes(self, string_time1, string_time2):
        dt1 = self.string_to_datetime(string_time1)
        dt2 = self.string_to_datetime(string_time2)
        return round((dt2 - dt1).total_seconds() / 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        dt = datetime(year, month, day, hour, minute, second)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

import unittest

class TimeUtilsTestGetMinutes(unittest.TestCase):
    def test_get_minutes_1(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_minutes("2001-7-18 1:1:1", "2001-7-18 2:1:1"), 60)

    def test_get_minutes_2(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_minutes("2001-7-18 1:1:1", "2001-7-18 3:1:1"), 120)

    def test_get_minutes_3(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_minutes("2001-7-18 1:1:1", "2001-7-18 4:1:1"), 180)

    def test_get_minutes_4(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_minutes("2001-7-18 1:1:1", "2001-7-18 5:1:1"), 240)

    def test_get_minutes_5(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.get_minutes("2001-7-18 1:1:1", "2001-7-18 6:1:1"), 300)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

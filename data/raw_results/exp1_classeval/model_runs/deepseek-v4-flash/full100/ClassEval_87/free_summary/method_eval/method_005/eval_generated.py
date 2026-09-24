from datetime import datetime, timedelta

class TimeUtils:
    def __init__(self):
        self._snapshot = datetime.now()

    def current_time(self):
        return self._snapshot.strftime("%H:%M:%S")

    def current_date(self):
        return self._snapshot.strftime("%Y-%m-%d")

    def add_seconds(self, seconds):
        return (self._snapshot + timedelta(seconds=seconds)).strftime("%H:%M:%S")

    @staticmethod
    def datetime_to_string(dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def string_to_datetime(s):
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def minute_difference(start_time, end_time):
        start = TimeUtils.string_to_datetime(start_time)
        end = TimeUtils.string_to_datetime(end_time)
        return int(round((end - start).total_seconds() / 60))

    @staticmethod
    def make_datetime_string(year, month, day, hour, minute, second):
        return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"

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

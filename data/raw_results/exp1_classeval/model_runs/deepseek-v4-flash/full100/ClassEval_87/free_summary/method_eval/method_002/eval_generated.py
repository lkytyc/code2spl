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

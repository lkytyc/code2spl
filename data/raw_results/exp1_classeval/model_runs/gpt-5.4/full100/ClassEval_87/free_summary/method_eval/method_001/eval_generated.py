class TimeUtils:
    def __init__(self):
        from datetime import datetime
        self.time = datetime.now()

    def get_time(self):
        return self.time.strftime("%H:%M:%S")

    def get_date(self):
        return self.time.strftime("%Y-%m-%d")

    def add_seconds(self, seconds):
        from datetime import timedelta
        return (self.time + timedelta(seconds=seconds)).strftime("%H:%M:%S")

    def string_to_datetime(self, string_time):
        from datetime import datetime
        return datetime.strptime(string_time, "%Y-%m-%d %H:%M:%S")

    def datetime_to_string(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def get_minutes(self, start_time, end_time):
        start_dt = self.string_to_datetime(start_time)
        end_dt = self.string_to_datetime(end_time)
        return round((end_dt - start_dt).total_seconds() / 60)

    def get_string_datetime(self, year, month, day, hour, minute, second):
        from datetime import datetime
        return self.datetime_to_string(datetime(year, month, day, hour, minute, second))

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

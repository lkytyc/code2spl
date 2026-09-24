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

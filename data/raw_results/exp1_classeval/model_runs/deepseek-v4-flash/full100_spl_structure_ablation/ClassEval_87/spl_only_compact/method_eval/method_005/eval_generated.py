import datetime

class TimeUtils:
    def __init__(self):
        self.datetime = datetime.datetime.now()
    
    def add_seconds(self, seconds):
        base_datetime = self.datetime
        time_delta = datetime.timedelta(seconds=seconds)
        new_datetime = base_datetime + time_delta
        time_format = "%H:%M:%S"
        return new_datetime.strftime(time_format)
    
    def datetime_to_string(self, datetime):
        formatted_string = datetime.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_string
    
    def get_current_date(self):
        format = "%Y-%m-%d"
        formatted_date = self.datetime.strftime(format)
        return formatted_date
    
    def get_current_time(self):
        format = "%H:%M:%S"
        return self.datetime.strftime(format)
    
    def get_format_time(self, year, month, day, hour, minute, second):
        format = "%Y-%m-%d %H:%M:%S"
        time_item = datetime.datetime(year, month, day, hour, minute, second)
        return time_item.strftime(format)
    
    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        return round((time2 - time1).seconds / 60)
    
    def string_to_datetime(self, string):
        parsed_datetime = datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        return parsed_datetime

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

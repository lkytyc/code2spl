import datetime


class TimeUtils:
    def __init__(self):
        self.datetime = datetime.datetime.now()

    def get_current_time(self):
        format = '%H:%M:%S'
        current_time_string = self.datetime.strftime(format)
        return current_time_string

    def get_current_date(self):
        format = '%Y-%m-%d'
        formatted_date = self.datetime.strftime(format)
        return formatted_date

    def add_seconds(self, seconds):
        timedelta_value = datetime.timedelta(seconds=seconds)
        new_datetime = self.datetime + timedelta_value
        format = '%H:%M:%S'
        formatted_time = new_datetime.strftime(format)
        return formatted_time

    def string_to_datetime(self, string):
        parsed_datetime = datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        return parsed_datetime

    def datetime_to_string(self, datetime):
        formatted_string = datetime.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_string

    def get_minutes(self, string_time1, string_time2):
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        minutes = round((time2 - time1).seconds / 60)
        return minutes

    def get_format_time(self, year, month, day, hour, minute, second):
        format = '%Y-%m-%d %H:%M:%S'
        time_item = datetime.datetime(year, month, day, hour, minute, second)
        return time_item.strftime(format)

import unittest

class TimeUtilsTestDatetimeToString(unittest.TestCase):
    def test_datetime_to_string_1(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.datetime_to_string(timeutils.datetime),
                         timeutils.datetime.strftime("%Y-%m-%d %H:%M:%S"))

    def test_datetime_to_string_2(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.datetime_to_string(timeutils.datetime),
                         timeutils.datetime.strftime("%Y-%m-%d %H:%M:%S"))

    def test_datetime_to_string_3(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.datetime_to_string(timeutils.datetime),
                         timeutils.datetime.strftime("%Y-%m-%d %H:%M:%S"))

    def test_datetime_to_string_4(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.datetime_to_string(timeutils.datetime),
                         timeutils.datetime.strftime("%Y-%m-%d %H:%M:%S"))

    def test_datetime_to_string_5(self):
        timeutils = TimeUtils()
        self.assertEqual(timeutils.datetime_to_string(timeutils.datetime),
                         timeutils.datetime.strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

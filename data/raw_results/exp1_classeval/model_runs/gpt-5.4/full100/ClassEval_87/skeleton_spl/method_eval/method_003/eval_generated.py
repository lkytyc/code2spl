import datetime
import time

class TimeUtils:
    """
    This is a time util class, including getting the current time and date, adding seconds to a datetime, converting between strings and datetime objects, calculating the time difference in minutes, and formatting a datetime object.
    """


    def __init__(self):
        """
        Get the current datetime
        """
        self.datetime = datetime.datetime.now()

    def get_current_time(self):
        """
        Return the current time in the format of '%H:%M:%S'
        :return: string
        >>> timeutils = TimeUtils()
        >>> timeutils.get_current_time()
        "19:19:22"
        """
        format = "%H:%M:%S"
        return self.datetime.strftime(format)

    def get_current_date(self):
        """
        Return the current date in the format of "%Y-%m-%d"
        :return: string
        >>> timeutils.get_current_date()
        "2023-06-14"
        """
        format = "%Y-%m-%d"
        formatted_date = self.datetime.strftime(format)
        return formatted_date

    def add_seconds(self, seconds):
        """
        Add the specified number of seconds to the current time
        :param seconds: int, number of seconds to add
        :return: string, time after adding the specified number of seconds in the format '%H:%M:%S'
        >>> timeutils.add_seconds(600)
        "19:29:22"
        """
        new_datetime = self.datetime + datetime.timedelta(seconds=seconds)
        format = "%H:%M:%S"
        return new_datetime.strftime(format)

    def string_to_datetime(self, string):
        """
        Convert the time string to a datetime instance
        :param string: string, string before converting format
        :return: datetime instance
        >>> timeutils.string_to_datetime("2001-7-18 1:1:1")
        2001-07-18 01:01:01
        """
        return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def datetime_to_string(self, datetime):
        """
        Convert a datetime instance to a string
        :param datetime: the datetime instance to convert
        :return: string, converted time string
        >>> timeutils.datetime_to_string(timeutils.datetime)
        "2023-06-14 19:30:03"
        """
        formatted_datetime_string = datetime.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_datetime_string

    def get_minutes(self, string_time1, string_time2):
        """
        Calculate how many minutes have passed between two times, and round the results to the nearest
        :return: int, the number of minutes between two times, rounded off
        >>> timeutils.get_minutes("2001-7-18 1:1:1", "2001-7-18 2:1:1")
        60
        """
        time1 = self.string_to_datetime(string_time1)
        time2 = self.string_to_datetime(string_time2)
        return round((time2 - time1).seconds / 60)

    def get_format_time(self, year, month, day, hour, minute, second):
        """
        get format time
        :param year: int
        :param month: int
        :param day: int
        :param hour: int
        :param minute: int
        :param second: int
        :return: formatted time string
        >>> timeutils.get_format_time(2001, 7, 18, 1, 1, 1)
        "2001-07-18 01:01:01"
        """
        format = "%Y-%m-%d %H:%M:%S"
        time_item = datetime.datetime(year, month, day, hour, minute, second)
        return time_item.strftime(format)

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

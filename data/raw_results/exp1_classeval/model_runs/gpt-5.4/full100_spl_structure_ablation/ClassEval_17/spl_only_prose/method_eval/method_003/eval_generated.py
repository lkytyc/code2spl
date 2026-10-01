class CalendarUtil:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def get_available_slots(self):
        from datetime import datetime, timedelta

        available_slots = []
        date = datetime.now()
        start_time = datetime(date.year, date.month, date.day, 0, 0)
        end_time = datetime(date.year, date.month, date.day, 23, 59)

        while start_time < end_time:
            slot_end_time = start_time + timedelta(minutes=60)
            if self.is_available(start_time, slot_end_time):
                available_slots.append((start_time, slot_end_time))
            start_time += timedelta(minutes=60)

        return available_slots

    def get_events(self, date):
        events_on_date = []

        for event in self.events:
            if event["date"].date() == date.date():
                events_on_date.append(event)

        return events_on_date

    def get_upcoming_events(self, num_events):
        from datetime import datetime

        now = datetime.now()
        upcoming_events = []

        for event in self.events:
            if event["start_time"] >= now:
                upcoming_events.append(event)

            if len(upcoming_events) == num_events:
                break

        return upcoming_events

    def is_available(self, start_time, end_time):
        for current_event in self.events:
            has_overlap = (
                start_time < current_event["end_time"]
                and end_time > current_event["start_time"]
            )

            if has_overlap:
                return False

        return True

    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)

import unittest
from datetime import datetime

class CalendarTestIsAvailable(unittest.TestCase):
    def test_is_available(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.is_available(datetime(2023, 1, 1, 0, 0), datetime(2023, 1, 1, 1, 0)), False)

    def test_is_available_2(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.is_available(datetime(2023, 1, 1, 1, 0), datetime(2023, 1, 1, 2, 0)), True)

    def test_is_available_3(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.is_available(datetime(2023, 1, 1, 0, 0), datetime(2023, 1, 1, 0, 30)), False)

    def test_is_available_4(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.is_available(datetime(2023, 1, 1, 0, 30), datetime(2023, 1, 1, 1, 0)), False)

    def test_is_available_5(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.is_available(datetime(2023, 1, 1, 1, 0), datetime(2023, 1, 1, 1, 30)), True)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

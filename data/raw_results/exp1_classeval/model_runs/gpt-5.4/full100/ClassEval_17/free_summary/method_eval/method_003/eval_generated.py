from datetime import datetime, timedelta

class CalendarUtil:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)

    def get_events(self, date):
        target_date = date.date() if hasattr(date, "date") else date
        return [
            event
            for event in self.events
            if event["date"].date() == target_date
        ]

    def is_available(self, start_time, end_time):
        for event in self.events:
            event_start = event["start_time"]
            event_end = event["end_time"]
            if start_time < event_end and end_time > event_start:
                return False
        return True

    def get_available_slots(self, date):
        day = date.date() if hasattr(date, "date") else date
        current = datetime.combine(day, datetime.min.time())
        end_of_day = current + timedelta(days=1)
        available_slots = []

        while current + timedelta(hours=1) <= end_of_day:
            slot_start = current
            slot_end = current + timedelta(hours=1)
            if self.is_available(slot_start, slot_end):
                available_slots.append((slot_start, slot_end))
            current += timedelta(hours=1)

        return available_slots

    def get_upcoming_events(self, num_events):
        now = datetime.now()
        upcoming = []
        for event in self.events:
            if event["start_time"] >= now:
                upcoming.append(event)
                if len(upcoming) >= num_events:
                    break
        return upcoming

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

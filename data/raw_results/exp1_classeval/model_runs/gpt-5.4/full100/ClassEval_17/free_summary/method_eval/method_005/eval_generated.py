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

class CalendarTestGetUpcomingEvents(unittest.TestCase):
    def test_get_upcoming_events(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 23, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.get_upcoming_events(1), [])

    def test_get_upcoming_events_2(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 1, 0),
                            'end_time': datetime(2023, 1, 1, 2, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.get_upcoming_events(1), [])

    def test_get_upcoming_events_3(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 2, 1, 0),
                            'end_time': datetime(2023, 1, 2, 2, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.get_upcoming_events(1), [])

    def test_get_upcoming_events_4(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 2, 1, 0),
                            'end_time': datetime(2023, 1, 2, 2, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.get_upcoming_events(2), [])

    def test_get_upcoming_events_5(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 23, 0), 'description': 'New Year'},
                           {'date': datetime(2024, 1, 2, 0, 0), 'start_time': datetime(2024, 1, 2, 1, 0),
                            'end_time': datetime(2024, 1, 2, 2, 0),
                            'description': 'New Year 2'}]
        self.assertEqual(calendar.get_upcoming_events(1), [
            {'date': datetime(2024, 1, 2, 0, 0), 'start_time': datetime(2024, 1, 2, 1, 0),
             'end_time': datetime(2024, 1, 2, 2, 0), 'description': 'New Year 2'}])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

class CalendarUtil:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)

    def get_events(self, date):
        return [event for event in self.events if event.get("date") == date]

    def is_available(self, start_time, end_time):
        for event in self.events:
            event_start = event.get("start_time")
            event_end = event.get("end_time")
            if event_start is None or event_end is None:
                continue
            if start_time < event_end and end_time > event_start:
                return False
        return True

    def get_available_slots(self, date):
        from datetime import datetime, timedelta

        slots = []
        base_date = date.date() if hasattr(date, "date") and not isinstance(date, datetime) else date
        for hour in range(24):
            start_time = datetime.combine(base_date, datetime.min.time()) + timedelta(hours=hour)
            end_time = start_time + timedelta(hours=1)
            if self.is_available(start_time, end_time):
                slots.append((start_time, end_time))
        return slots

    def get_upcoming_events(self, num_events):
        from datetime import datetime

        now = datetime.now()
        upcoming = [event for event in self.events if event.get("start_time") is not None and event.get("start_time") >= now]
        return upcoming[:num_events]

import unittest
from datetime import datetime

class CalendarTestGetEvents(unittest.TestCase):
    def test_get_events(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.get_events(datetime(2023, 1, 1)), [
            {'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
             'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'}])

    def test_get_events_2(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.get_events(datetime(2023, 1, 2)), [])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

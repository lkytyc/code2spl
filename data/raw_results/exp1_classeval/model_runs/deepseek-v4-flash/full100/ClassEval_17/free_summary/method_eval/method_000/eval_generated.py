from datetime import datetime, date, time, timedelta

class CalendarUtil:
    def __init__(self):
        self.events = []

    def _normalize_date(self, value):
        if isinstance(value, datetime):
            return value.date()
        return value

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)

    def get_events(self, date):
        target = self._normalize_date(date)
        return [event for event in self.events if self._normalize_date(event["date"]) == target]

    def is_available(self, start_time, end_time):
        for event in self.events:
            if start_time < event["end_time"] and end_time > event["start_time"]:
                return False
        return True

    def get_available_slots(self, date):
        date = self._normalize_date(date)
        slots = []
        slot_start = datetime.combine(date, time(0, 0))
        for _ in range(24):
            slot_end = slot_start + timedelta(hours=1)
            if self.is_available(slot_start, slot_end):
                slots.append((slot_start, slot_end))
            slot_start = slot_end
        return slots

    def get_upcoming_events(self, num_events):
        now = datetime.now()
        upcoming = []
        for event in self.events:
            if len(upcoming) >= num_events:
                break
            if event["start_time"] >= now:
                upcoming.append(event)
        return upcoming

import unittest
from datetime import datetime

class CalendarTestAddEvent(unittest.TestCase):
    def test_add_event(self):
        calendar = CalendarUtil()
        calendar.add_event({'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'})
        self.assertEqual(calendar.events, [
            {'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
             'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'}])

    def test_add_event_2(self):
        calendar = CalendarUtil()
        calendar.add_event({'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'})
        calendar.add_event({'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'})
        self.assertEqual(calendar.events, [
            {'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
             'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'},
            {'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
             'end_time': datetime(2023, 1, 1, 1, 0), 'description': 'New Year'}])

    def test_add_event_3(self):
        calendar = CalendarUtil()
        calendar.add_event({'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 23, 0), 'description': 'New Year'})
        self.assertEqual(calendar.events, [
            {'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
             'end_time': datetime(2023, 1, 1, 23, 0), 'description': 'New Year'}])

    def test_add_event_4(self):
        calendar = CalendarUtil()
        calendar.add_event({'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 22, 0), 'description': 'New Year'})
        self.assertEqual(calendar.events, [
            {'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
             'end_time': datetime(2023, 1, 1, 22, 0), 'description': 'New Year'}])

    def test_add_event_5(self):
        calendar = CalendarUtil()
        calendar.add_event({'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 20, 0), 'description': 'New Year'})
        self.assertEqual(calendar.events, [
            {'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
             'end_time': datetime(2023, 1, 1, 20, 0), 'description': 'New Year'}])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

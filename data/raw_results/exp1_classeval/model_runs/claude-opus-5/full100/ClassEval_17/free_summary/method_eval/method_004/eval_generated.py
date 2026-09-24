from datetime import datetime, timedelta


class CalendarUtil:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        try:
            self.events.remove(event)
        except ValueError:
            pass

    def get_events(self, date):
        return [e for e in self.events if e['date'].date() == date]

    def is_available(self, start_time, end_time):
        for event in self.events:
            if start_time < event['end_time'] and end_time > event['start_time']:
                return False
        return True

    def get_available_slots(self, date):
        available_slots = []
        start_of_day = datetime(date.year, date.month, date.day, 0, 0)
        end_of_day = datetime(date.year, date.month, date.day, 23, 59)
        current_time = start_of_day
        while current_time < end_of_day:
            slot_end = current_time + timedelta(hours=1)
            if self.is_available(current_time, slot_end):
                available_slots.append((current_time, slot_end))
            current_time = slot_end
        return available_slots

    def get_upcoming_events(self, num_events):
        upcoming = []
        now = datetime.now()
        for event in self.events:
            if event['start_time'] >= now:
                upcoming.append(event)
                if len(upcoming) == num_events:
                    break
        return upcoming

import unittest
from datetime import datetime

class CalendarTestGetAvailableSlots(unittest.TestCase):
    def test_get_available_slots(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 0, 0),
                            'end_time': datetime(2023, 1, 1, 23, 0), 'description': 'New Year'}]
        self.assertEqual(calendar.get_available_slots(datetime(2023, 1, 1)),
                         [(datetime(2023, 1, 1, 23, 0), datetime(2023, 1, 2, 0, 0))])

    def test_get_available_slots_2(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 1, 1, 0),
                            'end_time': datetime(2023, 1, 1, 2, 0), 'description': 'New Year'}]
        self.assertEqual(len(calendar.get_available_slots(datetime(2023, 1, 1))), 23)

    def test_get_available_slots_3(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 2, 1, 0),
                            'end_time': datetime(2023, 1, 2, 2, 0), 'description': 'New Year'}]
        self.assertEqual(len(calendar.get_available_slots(datetime(2023, 1, 1))), 24)

    def test_get_available_slots_4(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 2, 1, 0),
                            'end_time': datetime(2023, 1, 2, 2, 0), 'description': 'New Year'}]
        self.assertEqual(len(calendar.get_available_slots(datetime(2023, 1, 1))), 24)

    def test_get_available_slots_5(self):
        calendar = CalendarUtil()
        calendar.events = [{'date': datetime(2023, 1, 1, 0, 0), 'start_time': datetime(2023, 1, 2, 1, 0),
                            'end_time': datetime(2023, 1, 2, 2, 0), 'description': 'New Year'}]
        self.assertEqual(len(calendar.get_available_slots(datetime(2023, 1, 1))), 24)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

class Hotel:
    def __init__(self, name, rooms):
        self.name = name
        self.available_rooms = rooms.copy()
        self.booked_rooms = {}

    def book_room(self, room_type, room_number, name):
        if room_type not in self.available_rooms:
            return False
        if room_number <= self.available_rooms[room_type]:
            if room_type not in self.booked_rooms:
                self.booked_rooms[room_type] = {}
            self.booked_rooms[room_type][name] = room_number
            self.available_rooms[room_type] -= room_number
            return "Success!"
        return self.available_rooms[room_type]

    def check_in(self, room_type, room_number, name):
        if room_type not in self.booked_rooms:
            return False
        if name not in self.booked_rooms[room_type]:
            return
        if room_number > self.booked_rooms[room_type][name]:
            return False
        if room_number == self.booked_rooms[room_type][name]:
            self.booked_rooms[room_type].pop(name)
        else:
            self.booked_rooms[room_type][name] -= room_number

    def check_out(self, room_type, room_number):
        if room_type in self.available_rooms:
            self.available_rooms[room_type] += room_number
        else:
            self.available_rooms[room_type] = room_number

    def get_available_rooms(self, room_type):
        return self.available_rooms[room_type]

import unittest

class HotelTestCheckIn(unittest.TestCase):
    def setUp(self):
        self.hotel = Hotel('Test Hotel', {'single': 3, 'double': 2})
        self.hotel.booked_rooms = {'single': {'guest 1': 2}, 'double': {'guest 2': 1}}

    def test_check_in_1(self):
        self.hotel.check_in('single', 1, 'guest 1')
        self.assertEqual(self.hotel.booked_rooms, {'single': {'guest 1': 1}, 'double': {'guest 2': 1}})

    def test_check_in_2(self):
        self.assertFalse(self.hotel.check_in('single', 3, 'guest 1'))
        self.assertEqual(self.hotel.booked_rooms, {'single': {'guest 1': 2}, 'double': {'guest 2': 1}})

    def test_check_in_3(self):
        self.assertFalse(self.hotel.check_in('double', 1, 'guest 1'))
        self.assertEqual(self.hotel.booked_rooms, {'single': {'guest 1': 2}, 'double': {'guest 2': 1}})

    def test_check_in_4(self):
        self.hotel.check_in('double', 1, 'guest 2')
        self.assertEqual(self.hotel.booked_rooms, {'double': {}, 'single': {'guest 1': 2}})

    def test_check_in_5(self):
        self.hotel.check_in('double', 2, 'guest 2')
        self.assertEqual(self.hotel.booked_rooms, {'double': {'guest 2': 1}, 'single': {'guest 1': 2}})

    def test_check_in_6(self):
        res = self.hotel.check_in('abc', 1, 'guest 1')
        self.assertFalse(res)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

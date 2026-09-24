class Hotel:
    def __init__(self, name, rooms):
        self.name = name
        self.available_rooms = dict(rooms)
        self.booked_rooms = {}

    def book_room(self, room_type, room_number, name):
        if room_type not in self.available_rooms:
            return False

        available = self.available_rooms[room_type]

        if available <= 0:
            return False

        if room_number > available:
            return available

        if room_type not in self.booked_rooms:
            self.booked_rooms[room_type] = {}

        self.booked_rooms[room_type][name] = self.booked_rooms[room_type].get(name, 0) + room_number
        self.available_rooms[room_type] -= room_number
        return "Success!"

    def check_in(self, room_type, room_number, name):
        if room_type not in self.booked_rooms:
            return False

        if name not in self.booked_rooms[room_type]:
            return False

        booked = self.booked_rooms[room_type][name]

        if room_number > booked:
            return False

        if room_number == booked:
            del self.booked_rooms[room_type][name]
            if not self.booked_rooms[room_type]:
                del self.booked_rooms[room_type]
        else:
            self.booked_rooms[room_type][name] -= room_number

    def check_out(self, room_type, room_number):
        if room_type not in self.available_rooms:
            self.available_rooms[room_type] = room_number
        else:
            self.available_rooms[room_type] += room_number

    def get_available_rooms(self, room_type):
        return self.available_rooms.get(room_type)

import unittest

class HotelTestBookRoom(unittest.TestCase):
    def setUp(self):
        self.hotel = Hotel('peace hotel', {'single': 3, 'double': 2})

    def test_book_room_1(self):
        result = self.hotel.book_room('single', 2, 'guest 1')
        self.assertEqual(result, 'Success!')
        self.assertEqual(self.hotel.booked_rooms, {'single': {'guest 1': 2}})
        self.assertEqual(self.hotel.available_rooms, {'single': 1, 'double': 2})

    def test_book_room_2(self):
        result = self.hotel.book_room('triple', 2, 'guest 1')
        self.assertFalse(result)
        self.assertEqual(self.hotel.booked_rooms, {})
        self.assertEqual(self.hotel.available_rooms, {'single': 3, 'double': 2})

    def test_book_room_3(self):
        self.hotel.book_room('single', 2, 'guest 1')
        result = self.hotel.book_room('single', 2, 'guest 2')
        self.assertEqual(result, 1)
        self.assertEqual(self.hotel.booked_rooms, {'single': {'guest 1': 2}})
        self.assertEqual(self.hotel.available_rooms, {'single': 1, 'double': 2})

    def test_book_room_4(self):
        self.hotel.book_room('single', 2, 'guest 1')
        result = self.hotel.book_room('single', 1, 'guest 2')
        self.assertEqual(result, 'Success!')
        self.assertEqual(self.hotel.booked_rooms, {'single': {'guest 1': 2, 'guest 2': 1}})
        self.assertEqual(self.hotel.available_rooms, {'double': 2, 'single': 0})

    def test_book_room_5(self):
        self.hotel.book_room('single', 2, 'guest 1')
        result = self.hotel.book_room('single', 3, 'guest 2')
        self.assertEqual(result, 1)
        self.assertEqual(self.hotel.booked_rooms, {'single': {'guest 1': 2}})
        self.assertEqual(self.hotel.available_rooms, {'single': 1, 'double': 2})

    def test_book_room_6(self):
        self.hotel.book_room('single', 3, 'guest 1')
        result = self.hotel.book_room('single', 100, 'guest 1')
        self.assertFalse(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

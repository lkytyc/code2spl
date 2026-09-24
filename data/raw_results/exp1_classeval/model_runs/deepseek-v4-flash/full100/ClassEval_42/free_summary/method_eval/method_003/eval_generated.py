class Hotel:
    def __init__(self, name, rooms):
        self.name = name
        self.available_rooms = dict(rooms)
        self.bookings = {}

    def book_room(self, room_type, room_number, name):
        if self.available_rooms.get(room_type, 0) <= 0:
            return False
        if room_number > self.available_rooms[room_type]:
            return self.available_rooms[room_type]

        if name not in self.bookings:
            self.bookings[name] = {}
        self.bookings[name][room_type] = self.bookings[name].get(room_type, 0) + room_number
        self.available_rooms[room_type] -= room_number
        return "Success!"

    def check_in(self, room_type, room_number, name):
        if name not in self.bookings or room_type not in self.bookings[name]:
            return False
        if room_number > self.bookings[name][room_type]:
            return False

        if room_number == self.bookings[name][room_type]:
            del self.bookings[name][room_type]
            if not self.bookings[name]:
                del self.bookings[name]
        else:
            self.bookings[name][room_type] -= room_number
        return True

    def check_out(self, room_type, room_number):
        self.available_rooms[room_type] = self.available_rooms.get(room_type, 0) + room_number

    def get_available_rooms(self, room_type):
        return self.available_rooms.get(room_type, 0)

import unittest

class HotelTestAvailableRooms(unittest.TestCase):
    def setUp(self):
        self.hotel = Hotel('Test Hotel', {'single': 3, 'double': 2, 'triple': 2})

    def test_get_available_rooms(self):
        result = self.hotel.get_available_rooms('single')
        self.assertEqual(result, 3)

    def test_get_available_rooms_2(self):
        self.hotel.book_room('single', 2, 'guest 1')
        result = self.hotel.get_available_rooms('single')
        self.assertEqual(result, 1)

    def test_get_available_rooms_3(self):
        self.hotel.book_room('single', 3, 'guest 1')
        result = self.hotel.get_available_rooms('single')
        self.assertEqual(result, 0)

    def test_get_available_rooms_4(self):
        self.hotel.book_room('single', 3, 'guest 1')
        result = self.hotel.get_available_rooms('double')
        self.assertEqual(result, 2)

    def test_get_available_rooms_5(self):
        self.hotel.book_room('single', 3, 'guest 1')
        result = self.hotel.get_available_rooms('triple')
        self.assertEqual(result, 2)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

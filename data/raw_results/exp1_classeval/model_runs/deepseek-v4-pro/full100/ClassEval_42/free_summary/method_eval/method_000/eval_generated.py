class Hotel:
    def __init__(self, name, available_rooms):
        self.name = name
        self.available_rooms = available_rooms.copy()
        self.bookings = {}

    def book_room(self, room_type, count, guest_name):
        if room_type not in self.available_rooms:
            return False
        available = self.available_rooms[room_type]
        if available >= count:
            self.available_rooms[room_type] -= count
            if guest_name not in self.bookings:
                self.bookings[guest_name] = {}
            self.bookings[guest_name][room_type] = self.bookings[guest_name].get(room_type, 0) + count
            return f"Booking confirmed for {guest_name}: {count} {room_type} room(s)."
        elif available > 0:
            return available
        else:
            return False

    def check_in(self, guest_name, room_type, count):
        if guest_name not in self.bookings:
            return False
        if room_type not in self.bookings[guest_name]:
            return False
        booked_count = self.bookings[guest_name][room_type]
        if count > booked_count:
            return False
        if count == booked_count:
            del self.bookings[guest_name][room_type]
            if not self.bookings[guest_name]:
                del self.bookings[guest_name]
        else:
            self.bookings[guest_name][room_type] -= count
        return True

    def check_out(self, room_type, count):
        if room_type in self.available_rooms:
            self.available_rooms[room_type] += count
        else:
            self.available_rooms[room_type] = count

    def get_available_rooms(self, room_type):
        return self.available_rooms.get(room_type, 0)

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

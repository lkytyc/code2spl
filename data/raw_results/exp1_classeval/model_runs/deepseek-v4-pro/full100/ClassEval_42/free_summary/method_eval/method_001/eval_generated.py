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

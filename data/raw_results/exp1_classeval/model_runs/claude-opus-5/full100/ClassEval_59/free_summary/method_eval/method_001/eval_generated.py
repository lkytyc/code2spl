import numpy as np
from datetime import datetime


class MovieBookingSystem:
    def __init__(self):
        self.movies = []

    def _parse_time(self, time_str):
        return datetime.strptime(time_str, "%H:%M")

    def add_movie(self, name, price, start_time, end_time, n):
        movie = {
            "name": name,
            "price": price,
            "start_time": self._parse_time(start_time),
            "end_time": self._parse_time(end_time),
            "seats": np.zeros((n, n), dtype=int),
        }
        self.movies.append(movie)

    def book_ticket(self, movie_name, seats):
        movie = None
        for m in self.movies:
            if m["name"] == movie_name:
                movie = m
                break

        if movie is None:
            return "Movie not found."

        for row, col in seats:
            if movie["seats"][row][col] == 1:
                return f"Seat ({row}, {col}) is already booked."
            movie["seats"][row][col] = 1

        return "Booking successful."

    def available_movies(self, start_time, end_time):
        window_start = self._parse_time(start_time)
        window_end = self._parse_time(end_time)

        result = []
        for movie in self.movies:
            if movie["start_time"] >= window_start and movie["end_time"] <= window_end:
                result.append(movie["name"])

        return result

import unittest

class MovieBookingSystemTestBookTicket(unittest.TestCase):
    def setUp(self):
        self.system = MovieBookingSystem()
        self.system.add_movie('Batman', 49.9, '17:05', '19:25', 3)

    # book successfully
    def test_book_ticket_1(self):
        result = self.system.book_ticket('Batman', [(0, 0), (1, 1), (2, 2)])
        self.assertEqual(result, 'Booking success.')
        self.assertEqual(self.system.movies[0]['seats'][0][0], 1)
        self.assertEqual(self.system.movies[0]['seats'][1][1], 1)
        self.assertEqual(self.system.movies[0]['seats'][2][2], 1)

    # seat is not available
    def test_book_ticket_2(self):
        self.system.book_ticket('Batman', [(0, 0)])
        result = self.system.book_ticket('Batman', [(0, 0)])
        self.assertEqual(result, 'Booking failed.')
        self.assertEqual(self.system.movies[0]['seats'][0][0], 1)

    def test_book_ticket_3(self):
        result = self.system.book_ticket('batman', [(0, 0)])
        self.assertEqual(result, 'Movie not found.')
        self.assertEqual(self.system.movies[0]['seats'][0][0], 0)

    def test_book_ticket_4(self):
        result = self.system.book_ticket('Batman', [(0, 0), (1, 1)])
        self.assertEqual(result, 'Booking success.')
        self.assertEqual(self.system.movies[0]['seats'][0][0], 1)
        self.assertEqual(self.system.movies[0]['seats'][1][1], 1)

    def test_book_ticket_5(self):
        result = self.system.book_ticket('Batman', [(0, 0)])
        self.assertEqual(result, 'Booking success.')
        self.assertEqual(self.system.movies[0]['seats'][0][0], 1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

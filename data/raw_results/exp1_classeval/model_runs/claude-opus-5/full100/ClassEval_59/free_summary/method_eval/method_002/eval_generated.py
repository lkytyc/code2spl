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

class MovieBookingSystemTestAvailableMovies(unittest.TestCase):
    def setUp(self):
        self.system = MovieBookingSystem()
        self.system.add_movie('Batman', 49.9, '17:05', '19:25', 3)
        self.system.add_movie('Spiderman', 59.9, '20:00', '22:30', 4)

    def test_available_movies_1(self):
        result = self.system.available_movies('16:00', '23:00')
        self.assertEqual(result, ['Batman', 'Spiderman'])

    def test_available_movies_2(self):
        result = self.system.available_movies('23:00', '23:59')
        self.assertEqual(result, [])

    def test_available_movies_3(self):
        result = self.system.available_movies('17:00', '20:00')
        self.assertEqual(result, ['Batman'])

    def test_available_movies_4(self):
        result = self.system.available_movies('10:00', '23:00')
        self.assertEqual(result, ['Batman', 'Spiderman'])

    def test_available_movies_5(self):
        result = self.system.available_movies('20:00', '23:00')
        self.assertEqual(result, ['Spiderman'])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

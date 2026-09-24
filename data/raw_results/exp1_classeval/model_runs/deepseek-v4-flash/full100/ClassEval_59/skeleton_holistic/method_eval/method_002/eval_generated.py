from datetime import datetime
import numpy as np

class MovieBookingSystem:

    def __init__(self):
        self.movies = []

    def add_movie(self, name, price, start_time, end_time, n):
        start_time = datetime.strptime(start_time, "%H:%M")
        end_time = datetime.strptime(end_time, "%H:%M")
        self.movies.append({
            "name": name,
            "price": price,
            "start_time": start_time,
            "end_time": end_time,
            "seats": np.zeros((n, n))
        })

    def book_ticket(self, name, seats_to_book):
        movie = None
        for m in self.movies:
            if m["name"] == name:
                movie = m
                break

        if movie is None:
            return "Movie not found."

        seats = movie["seats"]
        to_book = []

        for seat in seats_to_book:
            row, col = seat

            if not (0 <= row < seats.shape[0] and 0 <= col < seats.shape[1]):
                return "Booking failed."

            if seats[row, col] != 0:
                return "Booking failed."

            if (row, col) in to_book:
                return "Booking failed."

            to_book.append((row, col))

        for row, col in to_book:
            seats[row, col] = 1

        return "Booking success."

    def available_movies(self, start_time, end_time):
        start_time = datetime.strptime(start_time, "%H:%M")
        end_time = datetime.strptime(end_time, "%H:%M")

        result = []
        for movie in self.movies:
            if movie["start_time"] >= start_time and movie["end_time"] <= end_time:
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

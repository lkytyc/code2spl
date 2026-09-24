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

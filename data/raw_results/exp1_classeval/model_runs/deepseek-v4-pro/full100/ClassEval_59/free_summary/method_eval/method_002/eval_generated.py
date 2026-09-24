class MovieBookingSystem:
    def __init__(self):
        self.movies = {}

    def add_movie(self, name, price, start_time, end_time, n):
        import numpy as np
        self.movies[name] = {
            'name': name,
            'price': price,
            'start_time': start_time,
            'end_time': end_time,
            'seats': np.zeros((n, n), dtype=int)
        }

    def book_ticket(self, name, seats_to_book):
        if name not in self.movies:
            return "Movie not found."
        movie = self.movies[name]
        seats = movie['seats']
        for row, col in seats_to_book:
            if seats[row][col] == 1:
                return "Booking failed."
        for row, col in seats_to_book:
            seats[row][col] = 1
        return "Booking success."

    def available_movies(self, start_time, end_time):
        result = []
        for movie in self.movies.values():
            if start_time <= movie['start_time'] and movie['end_time'] <= end_time:
                result.append(movie['name'])
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

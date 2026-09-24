class MovieBookingSystem:
    def __init__(self):
        self.movies = []

    def add_movie(self, movie_name, price, start_time, end_time, n):
        import numpy as np
        from datetime import datetime

        movie = {
            "name": movie_name,
            "price": price,
            "start_time": datetime.strptime(start_time, "%H:%M"),
            "end_time": datetime.strptime(end_time, "%H:%M"),
            "seats": np.zeros((n, n), dtype=int),
        }
        self.movies.append(movie)

    def book_ticket(self, movie_name, seats_to_book):
        for movie in self.movies:
            if movie["name"] == movie_name:
                seats = movie["seats"]
                for row, col in seats_to_book:
                    if seats[row][col] == 0:
                        seats[row][col] = 1
                    else:
                        return "Booking failed."
                return "Booking success."
        return "Movie not found."

    def available_movies(self, start_time, end_time):
        from datetime import datetime

        start_dt = datetime.strptime(start_time, "%H:%M")
        end_dt = datetime.strptime(end_time, "%H:%M")

        available = []
        for movie in self.movies:
            if movie["start_time"] >= start_dt and movie["end_time"] <= end_dt:
                available.append(movie["name"])
        return available

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

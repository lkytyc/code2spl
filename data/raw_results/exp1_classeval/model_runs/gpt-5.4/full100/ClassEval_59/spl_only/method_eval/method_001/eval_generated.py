class MovieBookingSystem:
    def __init__(self):
        self.movies = []

    def add_movie(self, name, price, start_time, end_time, n):
        movie = {
            "name": name,
            "price": price,
            "start_time": __import__("datetime").datetime.strptime(start_time, "%H:%M"),
            "end_time": __import__("datetime").datetime.strptime(end_time, "%H:%M"),
            "seats": __import__("numpy").zeros((n, n)),
        }
        self.movies.append(movie)

    def book_ticket(self, name, seats_to_book):
        for current_movie in self.movies:
            if current_movie["name"] == name:
                for current_seat in seats_to_book:
                    if current_movie["seats"][current_seat[0]][current_seat[1]] == 0:
                        current_movie["seats"][current_seat[0]][current_seat[1]] = 1
                    else:
                        return "Booking failed."
                return "Booking success."
        return "Movie not found."

    def available_movies(self, start_time, end_time):
        start_time = __import__("datetime").datetime.strptime(start_time, "%H:%M")
        end_time = __import__("datetime").datetime.strptime(end_time, "%H:%M")
        available_movies = []
        for movie in self.movies:
            if start_time <= movie["start_time"] and movie["end_time"] <= end_time:
                available_movies.append(movie["name"])
        return available_movies

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

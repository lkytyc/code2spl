class MovieBookingSystem:
    def __init__(self):
        self.movies = {}

    def add_movie(self, title, price, start, end, n):
        self.movies[title] = {
            "price": price,
            "start": self._to_minutes(start),
            "end": self._to_minutes(end),
            "seats": [[False] * n for _ in range(n)]
        }

    def book_ticket(self, movie_name, seats):
        if movie_name not in self.movies:
            return "Movie not found."

        movie = self.movies[movie_name]
        grid = movie["seats"]
        n = len(grid)
        requested = set()

        for seat in seats:
            row, col = seat
            if (row, col) in requested:
                return "Booking failed."
            requested.add((row, col))

            if not (0 <= row < n and 0 <= col < n):
                return "Booking failed."

            if grid[row][col]:
                return "Booking failed."

        for row, col in seats:
            grid[row][col] = True

        return "Booking success."

    def get_movies_by_time(self, start, end):
        start_min = self._to_minutes(start)
        end_min = self._to_minutes(end)
        result = []

        for title, movie in self.movies.items():
            if movie["start"] >= start_min and movie["end"] <= end_min:
                result.append(title)

        return result

    @staticmethod
    def _to_minutes(time_str):
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes

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

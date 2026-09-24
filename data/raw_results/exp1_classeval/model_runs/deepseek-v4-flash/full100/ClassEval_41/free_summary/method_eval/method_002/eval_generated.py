class GomokuGame:
    def __init__(self, board_size):
        self.size = board_size
        self.board = [[None for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'X'

    def make_move(self, row, col):
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        if self.board[row][col] is not None:
            return False

        self.board[row][col] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] is None:
                    continue
                for dr, dc in directions:
                    if self._check_five_in_a_row(row, col, dr, dc):
                        return self.board[row][col]

        return None

    def _check_five_in_a_row(self, row, col, dr, dc):
        symbol = self.board[row][col]
        if symbol is None:
            return False

        for i in range(1, 5):
            r = row + dr * i
            c = col + dc * i

            if not (0 <= r < self.size and 0 <= c < self.size):
                return False
            if self.board[r][c] != symbol:
                return False

        return True

import unittest

class GomokuGameTestCheckFiveInARow(unittest.TestCase):
    def setUp(self) -> None:
        self.gomokuGame = GomokuGame(10)
        moves = [(5, 5), (0, 0), (5, 4), (0, 1), (5, 3), (0, 2), (5, 2), (0, 3), (5, 1)]
        for move in moves:
            self.gomokuGame.make_move(move[0], move[1])

    def test_check_five_in_a_row_1(self):
        self.assertEqual(True, self.gomokuGame._check_five_in_a_row(5, 5, (0, -1)))

    def test_check_five_in_a_row_2(self):
        self.assertEqual(True, self.gomokuGame._check_five_in_a_row(5, 1, (0, 1)))

    def test_check_five_in_a_row_3(self):
        self.assertEqual(False, self.gomokuGame._check_five_in_a_row(0, 0, (0, 1)))

    def test_check_five_in_a_row_4(self):
        self.assertEqual(False, self.gomokuGame._check_five_in_a_row(0, 0, (1, 0)))

    def test_check_five_in_a_row_5(self):
        self.assertEqual(False, self.gomokuGame._check_five_in_a_row(5, 5, (1, 0)))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

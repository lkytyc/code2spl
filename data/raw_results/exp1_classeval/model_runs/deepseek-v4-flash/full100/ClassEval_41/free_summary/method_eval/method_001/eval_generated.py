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

class GomokuGameTestCheckWinner(unittest.TestCase):
    def test_check_winner_1(self):
        gomokuGame = GomokuGame(10)
        self.assertEqual(None, gomokuGame.check_winner())

    def test_check_winner_2(self):
        gomokuGame = GomokuGame(10)
        moves = [(5, 5), (0, 0), (5, 4), (0, 1), (5, 3), (0, 2), (5, 2), (0, 3), (5, 1)]
        for move in moves:
            gomokuGame.make_move(move[0], move[1])
        self.assertEqual('X', gomokuGame.check_winner())

    def test_check_winner_3(self):
        gomokuGame = GomokuGame(10)
        moves = [(5, 5), (0, 0), (5, 4), (0, 1), (5, 3), (0, 2), (5, 2), (0, 3), (5, 0), (0, 4)]
        for move in moves:
            gomokuGame.make_move(move[0], move[1])
        self.assertEqual('O', gomokuGame.check_winner())

    def test_check_winner_4(self):
        gomokuGame = GomokuGame(10)
        moves = [(5, 5), (0, 0), (5, 4), (0, 1), (5, 3), (0, 2), (5, 2), (0, 3), (5, 1), (0, 4)]
        for move in moves:
            gomokuGame.make_move(move[0], move[1])
        self.assertEqual(gomokuGame.check_winner(), 'O')

    def test_check_winner_5(self):
        gomokuGame = GomokuGame(10)
        moves = [(5, 5), (0, 0), (5, 4), (0, 1), (5, 3), (0, 2), (5, 2), (0, 3), (5, 1), (0, 4), (5, 0)]
        for move in moves:
            gomokuGame.make_move(move[0], move[1])
        self.assertEqual('O', gomokuGame.check_winner())

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

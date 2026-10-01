class GomokuGame:
    def __init__(self, board_size: int):
        self.board_size = board_size
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'X'

    def _check_five_in_a_row(self, row: int, col: int, direction: tuple[int, int]) -> bool:
        dx, dy = direction
        count = 1
        symbol = self.board[row][col]
        for i in range(1, 5):
            new_row = row + dx * i
            new_col = col + dy * i
            if new_row < 0 or new_row >= self.board_size or new_col < 0 or new_col >= self.board_size:
                return False
            if self.board[new_row][new_col] != symbol:
                return False
            count += 1
        return count == 5

    def check_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == ' ':
                    continue
                for direction in directions:
                    if self._check_five_in_a_row(row, col, direction):
                        return self.board[row][col]
        return None

    def make_move(self, row: int, col: int) -> bool:
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

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

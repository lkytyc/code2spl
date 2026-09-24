class GomokuGame:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'X'

    def make_move(self, row, col):
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            return False
        if self.board[row][col] != ' ':
            return False
        self.board[row][col] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == ' ':
                    continue
                for dr, dc in directions:
                    if self._check_five_in_a_row(row, col, (dr, dc)):
                        return self.board[row][col]
        return None

    def _check_five_in_a_row(self, row, col, direction):
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False
        target = self.board[row][col]
        if target == ' ':
            return False
        dr, dc = direction
        count = 0
        r, c = row, col
        while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == target:
            count += 1
            r += dr
            c += dc
        return count >= 5

import unittest

class GomokuGameTestMakeMove(unittest.TestCase):
    def setUp(self) -> None:
        self.board_size = 10
        self.gomokuGame = GomokuGame(self.board_size)

    def test_make_move_1(self):
        board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.assertEqual(True, self.gomokuGame.make_move(0, 0))
        board[0][0] = 'X'
        self.assertEqual(board, self.gomokuGame.board)

    # same position
    def test_make_move_2(self):
        board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.assertEqual(True, self.gomokuGame.make_move(0, 0))
        self.assertEqual(False, self.gomokuGame.make_move(0, 0))
        board[0][0] = 'X'
        self.assertEqual(board, self.gomokuGame.board)

    def test_make_move_3(self):
        board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.assertEqual(True, self.gomokuGame.make_move(0, 0))
        self.assertEqual(True, self.gomokuGame.make_move(0, 1))
        board[0][0] = 'X'
        board[0][1] = 'O'
        self.assertEqual(board, self.gomokuGame.board)

    def test_make_move_4(self):
        board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.assertEqual(True, self.gomokuGame.make_move(0, 0))
        self.assertEqual(True, self.gomokuGame.make_move(0, 1))
        self.assertEqual(False, self.gomokuGame.make_move(0, 0))
        board[0][0] = 'X'
        board[0][1] = 'O'
        self.assertEqual(board, self.gomokuGame.board)

    def test_make_move_5(self):
        board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.assertEqual(True, self.gomokuGame.make_move(0, 0))
        self.assertEqual(True, self.gomokuGame.make_move(0, 1))
        self.assertEqual(False, self.gomokuGame.make_move(0, 1))
        board[0][0] = 'X'
        board[0][1] = 'O'
        self.assertEqual(board, self.gomokuGame.board)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

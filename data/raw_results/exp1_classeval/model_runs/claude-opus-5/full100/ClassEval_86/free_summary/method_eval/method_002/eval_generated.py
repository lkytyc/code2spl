class TicTacToe:
    def __init__(self, N=3):
        self.N = N
        self.board = [[' '] * N for _ in range(3)]
        self.current_player = 'X'

    def make_move(self, row, col):
        if self.board[row][col] != ' ':
            return False
        self.board[row][col] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_winner(self):
        board = self.board
        N = self.N

        for row in range(3):
            if board[row][0] != ' ' and all(board[row][c] == board[row][0] for c in range(N)):
                return board[row][0]

        for col in range(N):
            if board[0][col] != ' ' and all(board[r][col] == board[0][col] for r in range(3)):
                return board[0][col]

        if board[0][0] != ' ' and all(board[i][i] == board[0][0] for i in range(3)):
            return board[0][0]

        if board[0][N - 1] != ' ' and all(board[i][N - 1 - i] == board[0][N - 1] for i in range(3)):
            return board[0][N - 1]

        return None

    def is_board_full(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

import unittest

class TicTacToeTestIsBoardFull(unittest.TestCase):
    # not full
    def test_is_board_full_1(self):
        ttt = TicTacToe()
        self.assertFalse(ttt.is_board_full())

    # full
    def test_is_board_full_2(self):
        ttt = TicTacToe()
        moves = [(1, 1), (0, 2), (2, 2), (0, 0), (0, 1), (2, 1), (1, 0), (1, 2), (2, 0)]
        for move in moves:
            ttt.make_move(move[0], move[1])
        self.assertTrue(ttt.is_board_full())

    def test_is_board_full_3(self):
        ttt = TicTacToe()
        moves = [(0, 0), (0, 1), (1, 1), (1, 0), (2, 0)]
        for move in moves:
            ttt.make_move(move[0], move[1])
        self.assertFalse(ttt.is_board_full())

    def test_is_board_full_4(self):
        ttt = TicTacToe()
        moves = [(0, 0), (0, 1), (1, 1), (1, 0), (2, 0), (0, 2), (1, 2), (2, 1), (2, 2)]
        for move in moves:
            ttt.make_move(move[0], move[1])
        self.assertTrue(ttt.is_board_full())

    def test_is_board_full_5(self):
        ttt = TicTacToe()
        moves = [(0, 0), (0, 1), (1, 1), (1, 0), (2, 0), (0, 2), (1, 2), (2, 1)]
        for move in moves:
            ttt.make_move(move[0], move[1])
        self.assertFalse(ttt.is_board_full())

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

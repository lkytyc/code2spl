class TicTacToe:
    def __init__(self, N: int = 3):
        self.board = [[' ' for _ in range(N)] for _ in range(3)]
        self.current_player = 'X'

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        return None

    def is_board_full(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def make_move(self, row: int, col: int) -> bool:
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

import unittest

class TicTacToeTestCheckWinner(unittest.TestCase):
    # rows
    def test_check_winner_1(self):
        ttt = TicTacToe()
        moves = [(1, 0), (2, 0), (1, 1), (2, 1), (1, 2)]
        for move in moves:
            ttt.make_move(move[0], move[1])
        self.assertEqual(ttt.check_winner(), 'X')

    # columns
    def test_check_winner_2(self):
        ttt = TicTacToe()
        moves = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]
        for move in moves:
            ttt.make_move(move[0], move[1])
        self.assertEqual(ttt.check_winner(), 'X')

    # main diagonals 
    def test_check_winner_3(self):
        ttt = TicTacToe()
        moves = [(0, 0), (0, 1), (1, 1), (0, 2), (2, 2)]
        for move in moves:
            ttt.make_move(move[0], move[1])
        self.assertEqual(ttt.check_winner(), 'X')

    # secondary diagonals 
    def test_check_winner_4(self):
        ttt = TicTacToe()
        moves = [(0, 2), (0, 1), (1, 1), (1, 0), (2, 0)]
        for move in moves:
            ttt.make_move(move[0], move[1])
        self.assertEqual(ttt.check_winner(), 'X')

    def test_check_winner_5(self):
        ttt = TicTacToe()
        moves = [(0, 0), (0, 1), (1, 1), (1, 0), (2, 0)]
        for move in moves:
            ttt.make_move(move[0], move[1])
        self.assertEqual(ttt.check_winner(), None)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

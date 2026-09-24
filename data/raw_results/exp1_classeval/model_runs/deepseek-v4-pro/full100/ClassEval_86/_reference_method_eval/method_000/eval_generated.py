class TicTacToe:
    def __init__(self, N=3):
        self.board = [[' ' for _ in range(N)] for _ in range(3)]
        self.current_player = 'X'

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        else:
            return False

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

import unittest

class TicTacToeTestMakeMove(unittest.TestCase):
    def test_make_move_1(self):
        ttt = TicTacToe()
        self.assertEqual(ttt.current_player, 'X')
        self.assertTrue(ttt.make_move(0, 0))
        self.assertEqual(ttt.current_player, 'O')

    # move invalid
    def test_make_move_2(self):
        ttt = TicTacToe()
        self.assertEqual(ttt.current_player, 'X')
        self.assertTrue(ttt.make_move(0, 0))
        self.assertTrue(ttt.make_move(0, 1))
        self.assertFalse(ttt.make_move(0, 0))
        self.assertEqual(ttt.current_player, 'X')

    def test_make_move_3(self):
        ttt = TicTacToe()
        self.assertEqual(ttt.current_player, 'X')
        self.assertTrue(ttt.make_move(0, 0))
        self.assertTrue(ttt.make_move(0, 1))
        self.assertTrue(ttt.make_move(1, 1))
        self.assertEqual(ttt.current_player, 'O')

    def test_make_move_4(self):
        ttt = TicTacToe()
        self.assertEqual(ttt.current_player, 'X')
        self.assertTrue(ttt.make_move(0, 0))
        self.assertTrue(ttt.make_move(0, 1))
        self.assertTrue(ttt.make_move(1, 1))
        self.assertTrue(ttt.make_move(1, 2))
        self.assertEqual(ttt.current_player, 'X')

    def test_make_move_5(self):
        ttt = TicTacToe()
        self.assertEqual(ttt.current_player, 'X')
        self.assertTrue(ttt.make_move(0, 0))
        self.assertTrue(ttt.make_move(0, 1))
        self.assertTrue(ttt.make_move(1, 1))
        self.assertTrue(ttt.make_move(1, 2))
        self.assertTrue(ttt.make_move(2, 2))
        self.assertEqual(ttt.current_player, 'O')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

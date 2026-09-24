import random


class MinesweeperGame:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.minesweeper_map = self.generate_mine_sweeper_map()
        self.player_map = self.generate_playerMap()
        self.score = 0

    def generate_mine_sweeper_map(self):
        board = []
        for _ in range(self.n):
            row = []
            for _ in range(self.n):
                row.append(0)
            board.append(row)

        for _ in range(self.k):
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)

            board[x][y] = 'X'

            if x - 1 >= 0 and y - 1 >= 0 and board[x - 1][y - 1] != 'X':
                board[x - 1][y - 1] += 1
            if x - 1 >= 0 and board[x - 1][y] != 'X':
                board[x - 1][y] += 1
            if x - 1 >= 0 and y + 1 < self.n and board[x - 1][y + 1] != 'X':
                board[x - 1][y + 1] += 1
            if y - 1 >= 0 and board[x][y - 1] != 'X':
                board[x][y - 1] += 1
            if y + 1 < self.n and board[x][y + 1] != 'X':
                board[x][y + 1] += 1
            if x + 1 < self.n and y - 1 >= 0 and board[x + 1][y - 1] != 'X':
                board[x + 1][y - 1] += 1
            if x + 1 < self.n and board[x + 1][y] != 'X':
                board[x + 1][y] += 1
            if x + 1 < self.n and y + 1 < self.n and board[x + 1][y + 1] != 'X':
                board[x + 1][y + 1] += 1

        return board

    def generate_playerMap(self):
        board = []
        for _ in range(self.n):
            row = []
            for _ in range(self.n):
                row.append('-')
            board.append(row)
        return board

    def sweep(self, x, y):
        if self.minesweeper_map[x][y] == 'X':
            return False

        self.player_map[x][y] = self.minesweeper_map[x][y]
        self.score += 1

        if self.check_won(self.player_map):
            return True

        return self.player_map

    def check_won(self, map):
        for i in range(self.n):
            for j in range(self.n):
                if self.minesweeper_map[i][j] != 'X' and map[i][j] == '-':
                    return False
        return True

import unittest

class MinesweeperGameTestSweep(unittest.TestCase):
    def test_sweep(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.assertEqual(minesweeper_game.sweep(1,1), [['-', '-', '-'], ['-', 1, '-'], ['-', '-', '-']])
        self.assertEqual(minesweeper_game.score, 1)

    def test_sweep_2(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.assertEqual(minesweeper_game.sweep(0,0), False)
        self.assertEqual(minesweeper_game.score, 0)

    def test_sweep_3(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '0'], ['1', '1', '0'], ['0', '0', '0']]
        self.assertEqual(minesweeper_game.sweep(0,1), True)
        self.assertEqual(minesweeper_game.score, 1)

    def test_sweep_4(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '-'], ['-', '-', '0'], ['0', '0', '0']]
        self.assertEqual(minesweeper_game.sweep(0,2), [['-', '-', 0], ['-', '-', '0'], ['0', '0', '0']])
        self.assertEqual(minesweeper_game.score, 1)

    def test_sweep_5(self):
        minesweeper_game = MinesweeperGame(3, 1)
        minesweeper_game.minesweeper_map = [['X', 1, 0], [1, 1, 0], [0, 0, 0]]
        minesweeper_game.player_map = [['-', '-', '0'], ['-', '1', '0'], ['0', '0', '0']]
        self.assertEqual(minesweeper_game.sweep(1,0), [['-', '-', '0'], [1, '1', '0'], ['0', '0', '0']])
        self.assertEqual(minesweeper_game.score, 1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

import random

class MinesweeperGame:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.minesweeper_map = [['0' for _ in range(n)] for _ in range(n)]
        self.player_map = [['-' for _ in range(n)] for _ in range(n)]
        self.score = 0
        self.game_over = False

        mines_placed = 0
        while mines_placed < k:
            row = random.randint(0, n - 1)
            col = random.randint(0, n - 1)
            if self.minesweeper_map[row][col] != 'X':
                self.minesweeper_map[row][col] = 'X'
                mines_placed += 1

        for i in range(n):
            for j in range(n):
                if self.minesweeper_map[i][j] != 'X':
                    count = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < n and 0 <= nj < n and self.minesweeper_map[ni][nj] == 'X':
                                count += 1
                    self.minesweeper_map[i][j] = str(count)

    def check_won(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.minesweeper_map[i][j] != 'X' and self.player_map[i][j] == '-':
                    return False
        return True

    def sweep(self, x, y):
        if self.game_over:
            return self.player_map
        if self.minesweeper_map[x][y] == 'X':
            self.game_over = True
            return False
        if self.player_map[x][y] == '-':
            self.player_map[x][y] = self.minesweeper_map[x][y]
            self.score += 1
        if self.check_won():
            return True
        return self.player_map

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

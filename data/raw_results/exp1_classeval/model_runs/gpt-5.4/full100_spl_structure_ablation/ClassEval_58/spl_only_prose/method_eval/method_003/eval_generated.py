class MinesweeperGame:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.minesweeper_map = self.generate_mine_sweeper_map()
        self.player_map = self.generate_playerMap()
        self.score = 0

    def check_won(self, map):
        for i in range(self.n):
            for j in range(self.n):
                if map[i][j] == '-' and self.minesweeper_map[i][j] != 'X':
                    return False
        return True

    def generate_mine_sweeper_map(self):
        import random

        arr = [[0 for _ in range(self.n)] for _ in range(self.n)]

        for _ in range(self.k):
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)

            arr[y][x] = 'X'

            if (x >= 0 and x <= self.n - 2) and (y >= 0 and y <= self.n - 1):
                if arr[y][x + 1] != 'X':
                    arr[y][x + 1] += 1

            if (x >= 1 and x <= self.n - 1) and (y >= 0 and y <= self.n - 1):
                if arr[y][x - 1] != 'X':
                    arr[y][x - 1] += 1

            if (x >= 1 and x <= self.n - 1) and (y >= 1 and y <= self.n - 1):
                if arr[y - 1][x - 1] != 'X':
                    arr[y - 1][x - 1] += 1

            if (x >= 0 and x <= self.n - 2) and (y >= 1 and y <= self.n - 1):
                if arr[y - 1][x + 1] != 'X':
                    arr[y - 1][x + 1] += 1

            if (x >= 0 and x <= self.n - 1) and (y >= 1 and y <= self.n - 1):
                if arr[y - 1][x] != 'X':
                    arr[y - 1][x] += 1

            if (x >= 0 and x <= self.n - 2) and (y >= 0 and y <= self.n - 2):
                if arr[y + 1][x + 1] != 'X':
                    arr[y + 1][x + 1] += 1

            if (x >= 1 and x <= self.n - 1) and (y >= 0 and y <= self.n - 2):
                if arr[y + 1][x - 1] != 'X':
                    arr[y + 1][x - 1] += 1

            if (x >= 0 and x <= self.n - 1) and (y >= 0 and y <= self.n - 2):
                if arr[y + 1][x] != 'X':
                    arr[y + 1][x] += 1

        return arr

    def generate_playerMap(self):
        arr = [['-' for _ in range(self.n)] for _ in range(self.n)]
        return arr

    def sweep(self, x, y):
        if self.minesweeper_map[x][y] == 'X':
            return False

        self.player_map[x][y] = self.minesweeper_map[x][y]
        self.score += 1

        if self.check_won(self.player_map) == True:
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

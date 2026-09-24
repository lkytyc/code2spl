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
        arr = [[0 for _ in range(self.n)] for _ in range(self.n)]
        import random

        for _ in range(self.k):
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)
            arr[y][x] = 'X'

            if 0 <= x <= self.n - 2 and 0 <= y <= self.n - 1:
                if arr[y][x + 1] != 'X':
                    arr[y][x + 1] += 1
            if 1 <= x <= self.n - 1 and 0 <= y <= self.n - 1:
                if arr[y][x - 1] != 'X':
                    arr[y][x - 1] += 1
            if 1 <= x <= self.n - 1 and 1 <= y <= self.n - 1:
                if arr[y - 1][x - 1] != 'X':
                    arr[y - 1][x - 1] += 1
            if 0 <= x <= self.n - 2 and 1 <= y <= self.n - 1:
                if arr[y - 1][x + 1] != 'X':
                    arr[y - 1][x + 1] += 1
            if 0 <= x <= self.n - 1 and 1 <= y <= self.n - 1:
                if arr[y - 1][x] != 'X':
                    arr[y - 1][x] += 1
            if 0 <= x <= self.n - 2 and 0 <= y <= self.n - 2:
                if arr[y + 1][x + 1] != 'X':
                    arr[y + 1][x + 1] += 1
            if 1 <= x <= self.n - 1 and 0 <= y <= self.n - 2:
                if arr[y + 1][x - 1] != 'X':
                    arr[y + 1][x - 1] += 1
            if 0 <= x <= self.n - 1 and 0 <= y <= self.n - 2:
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

class MinesweeperGameTestGeneratePlayerMap(unittest.TestCase):
    def test_generate_playerMap(self):
        minesweeper_game = MinesweeperGame(3, 2)
        self.assertEqual(minesweeper_game.generate_playerMap(), [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']])

    def test_generate_playerMap_2(self):
        minesweeper_game = MinesweeperGame(3, 1)
        self.assertEqual(minesweeper_game.generate_playerMap(), [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']])

    def test_generate_playerMap_3(self):
        minesweeper_game = MinesweeperGame(4, 2)
        self.assertEqual(minesweeper_game.generate_playerMap(),[['-', '-', '-', '-'],['-', '-', '-', '-'],['-', '-', '-', '-'],['-', '-', '-', '-']])

    def test_generate_playerMap_4(self):
        minesweeper_game = MinesweeperGame(1, 4)
        self.assertEqual(minesweeper_game.generate_playerMap(), [['-']])

    def test_generate_playerMap_5(self):
        minesweeper_game = MinesweeperGame(2, 5)
        self.assertEqual(minesweeper_game.generate_playerMap(), [['-', '-'], ['-', '-']])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

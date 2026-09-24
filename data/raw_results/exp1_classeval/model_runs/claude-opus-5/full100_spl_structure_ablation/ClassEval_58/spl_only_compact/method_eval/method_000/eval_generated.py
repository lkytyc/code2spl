import random


class MinesweeperGame:
    def __init__(self, n: int, k: int):
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
        for num in range(self.k):
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)
            arr[y][x] = 'X'
            # RIGHT
            if x <= self.n - 2 and arr[y][x + 1] != 'X':
                arr[y][x + 1] += 1
            # LEFT
            if x >= 1 and arr[y][x - 1] != 'X':
                arr[y][x - 1] += 1
            # UPPER-LEFT
            if x >= 1 and y >= 1 and arr[y - 1][x - 1] != 'X':
                arr[y - 1][x - 1] += 1
            # UPPER-RIGHT
            if x <= self.n - 2 and y >= 1 and arr[y - 1][x + 1] != 'X':
                arr[y - 1][x + 1] += 1
            # UP
            if y >= 1 and arr[y - 1][x] != 'X':
                arr[y - 1][x] += 1
            # LOWER-RIGHT
            if x <= self.n - 2 and y <= self.n - 2 and arr[y + 1][x + 1] != 'X':
                arr[y + 1][x + 1] += 1
            # LOWER-LEFT
            if x >= 1 and y <= self.n - 2 and arr[y + 1][x - 1] != 'X':
                arr[y + 1][x - 1] += 1
            # DOWN
            if y <= self.n - 2 and arr[y + 1][x] != 'X':
                arr[y + 1][x] += 1
        return arr

    def generate_playerMap(self):
        arr = [['-' for _ in range(self.n)] for _ in range(self.n)]
        return arr

    def sweep(self, x: int, y: int):
        if self.minesweeper_map[x][y] == 'X':
            return False
        self.player_map[x][y] = self.minesweeper_map[x][y]
        self.score += 1
        if self.check_won(self.player_map):
            return True
        return self.player_map

import unittest

class MinesweeperGameTestGenerateMineSweeperMap(unittest.TestCase):
    def test_generate_mine_sweeper_map(self):
        minesweeper_game = MinesweeperGame(3, 2)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(3, length)
        self.assertEqual(2, mine_num)

    def test_generate_mine_sweeper_map_2(self):
        minesweeper_game = MinesweeperGame(3, 1)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(3, length)
        self.assertEqual(1, mine_num)

    def test_generate_mine_sweeper_map_3(self):
        minesweeper_game = MinesweeperGame(3, 0)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(3, length)
        self.assertEqual(0, mine_num)

    def test_generate_mine_sweeper_map_4(self):
        minesweeper_game = MinesweeperGame(5, 1)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(length,5)
        self.assertEqual(mine_num, 1)

    def test_generate_mine_sweeper_map_5(self):
        minesweeper_game = MinesweeperGame(4, 1)
        length = len(minesweeper_game.minesweeper_map)
        mine_num = 0
        for row in minesweeper_game.minesweeper_map:
            for cell in row:
                if cell == 'X':
                    mine_num += 1
        self.assertEqual(length, 4)
        self.assertEqual(mine_num, 1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
